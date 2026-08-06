#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能三层去重脚本
1. URL去重：相同source_url → 重复
2. 标题指纹去重：标准化标题相同（跨日期、跨来源）→ 重复
3. 模糊相似度去重：同公司±N天内标题相似度>阈值 → 重复

保留策略：最早发布 > 摘要更长 > 已有英文翻译

用法：
  python fast_dedup.py              # 执行去重
  python fast_dedup.py --dry        # 试运行，只报告不删除
  python fast_dedup.py --days 30    # 自定义时间窗口（默认14天）
  python fast_dedup.py --threshold 0.70  # 自定义相似度阈值
"""

import json
import re
import sys
import argparse
from difflib import SequenceMatcher
from datetime import datetime
from collections import defaultdict

INPUT_FILE = 'data/events.json'
OUTPUT_FILE = 'data/events.json'


# ===================== 工具函数 =====================

def load_events():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d')
    except:
        return None

def normalize_url(url):
    if not url:
        return ''
    url = re.sub(r'[?#].*$', '', url)      # 去 query / fragment
    url = url.rstrip('/')                    # 去尾部斜杠
    url = re.sub(r'https?://(www\.)?', '', url)  # 去协议和 www
    return url.lower()

def normalize_title(title):
    """标准化标题：去来源后缀、去标点、转小写、压缩空格"""
    if not title:
        return ''
    # 去来源后缀: " - Source", " | Source", "_Source", "——Source", "丨Source"
    title = re.sub(r'\s*[-–—|_丨]\s*[\w\s\.\u4e00-\u9fff]+$', '', title)
    # 去 (Published 2023) 等括号注释
    title = re.sub(r'\([^)]*(?:published|updated|review)[^)]*\)', '', title, flags=re.IGNORECASE)
    # 去标点，保留中英文和数字
    title = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', title)
    title = title.lower()
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def similarity(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def event_score(e):
    """给事件打分，分数越高越应该保留"""
    date = parse_date(e.get('date', ''))
    # 越早越好（返回负的天数，排序时小的优先）
    day_score = 0
    if date:
        day_score = -date.toordinal()
    summary_len = len(e.get('summary', '') or '')
    has_en = 1 if e.get('title_en') else 0
    return (day_score, summary_len, has_en)


# ===================== Layer 1: URL 去重 =====================

def dedup_by_url(events):
    """相同 source_url → 重复，保留最优"""
    url_map = {}   # url -> event
    remove_ids = set()

    for e in events:
        url = normalize_url(e.get('source_url', ''))
        if not url or len(url) < 10:  # 太短的不靠谱
            continue
        if url in url_map:
            existing = url_map[url]
            if event_score(e) > event_score(existing):
                remove_ids.add(existing['id'])
                url_map[url] = e
            else:
                remove_ids.add(e['id'])
        else:
            url_map[url] = e

    return remove_ids


# ===================== Layer 2: 标题指纹去重 =====================

def dedup_by_title_hash(events, exclude_ids):
    """标准化标题完全相同（跨日期、跨来源）→ 重复"""
    title_map = {}  # normalized_title -> event
    remove_ids = set()

    for e in events:
        if e['id'] in exclude_ids:
            continue
        norm = normalize_title(e.get('title', ''))
        if not norm or len(norm) < 5:  # 太短的不靠谱
            continue
        if norm in title_map:
            existing = title_map[norm]
            if event_score(e) > event_score(existing):
                remove_ids.add(existing['id'])
                title_map[norm] = e
            else:
                remove_ids.add(e['id'])
        else:
            title_map[norm] = e

    return remove_ids


# ===================== Layer 3: 模糊相似度去重 =====================

def quick_prefilter(a, b):
    """快速预过滤：token集合Jaccard相似度，O(n)，排除明显不相关的对"""
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.6:
        return False
    ta = set(a.split())
    tb = set(b.split())
    if not ta or not tb:
        return False
    overlap = len(ta & tb) / len(ta | tb)
    return overlap >= 0.3

def dedup_by_fuzzy(events, exclude_ids, days_window=14, threshold=0.75):
    """同公司 ±N 天内标题相似度 > 阈值 → 重复
    使用滑动窗口 + 快速预过滤，大幅减少 SequenceMatcher 调用
    """
    # 按公司分组
    by_company = defaultdict(list)
    for e in events:
        if e['id'] not in exclude_ids:
            by_company[e.get('company', '')].append(e)

    remove_ids = set()
    comparisons = 0
    prefilter_pass = 0
    companies_done = 0
    total_companies = len(by_company)

    for company, group in by_company.items():
        companies_done += 1
        if len(group) > 50:
            print(f"  [{companies_done}/{total_companies}] {company}: {len(group)} events...", flush=True)
        if len(group) < 2:
            continue

        # 按日期排序
        group.sort(key=lambda x: x.get('date', ''))

        # 预计算标准化标题和日期
        norms = [normalize_title(e.get('title', '')) for e in group]
        dates = [parse_date(e.get('date', '')) for e in group]

        for i in range(len(group)):
            if group[i]['id'] in remove_ids:
                continue
            if not dates[i] or not norms[i] or len(norms[i]) < 5:
                continue

            for j in range(i + 1, len(group)):
                if group[j]['id'] in remove_ids:
                    continue
                if not dates[j] or not norms[j] or len(norms[j]) < 5:
                    continue

                # 滑动窗口：超过时间范围就 break（已排序）
                delta = abs((dates[j] - dates[i]).days)
                if delta > days_window:
                    break

                comparisons += 1

                # 快速预过滤
                if not quick_prefilter(norms[i], norms[j]):
                    continue
                prefilter_pass += 1

                sim = similarity(norms[i], norms[j])

                if sim >= threshold:
                    if event_score(group[i]) >= event_score(group[j]):
                        remove_ids.add(group[j]['id'])
                    else:
                        remove_ids.add(group[i]['id'])
                        break  # i 被删除，不再以 i 为基准比较

    print(f"  Comparisons: {comparisons} (prefilter passed: {prefilter_pass})", flush=True)
    return remove_ids, comparisons


# ===================== Layer 4: 跨语言去重 =====================

def dedup_cross_language(events, exclude_ids, days_window=21, threshold=0.70):
    """用 title_en 字段跨语言去重
    中文新闻被翻译成 title_en 后，与英文原标题比较
    同公司 ±N 天内 title_en 相似度 > 阈值 → 重复
    """
    by_company = defaultdict(list)
    for e in events:
        if e['id'] not in exclude_ids:
            by_company[e.get('company', '')].append(e)

    remove_ids = set()
    comparisons = 0

    for company, group in by_company.items():
        if len(group) < 2:
            continue

        group.sort(key=lambda x: x.get('date', ''))

        # 预计算 title_en 标准化 + 日期，只保留有 title_en 的
        norms = []
        dates = []
        for e in group:
            en = e.get('title_en', '')
            norm = normalize_title(en) if en else ''
            norms.append(norm)
            dates.append(parse_date(e.get('date', '')))

        for i in range(len(group)):
            if group[i]['id'] in remove_ids:
                continue
            if not dates[i] or not norms[i] or len(norms[i]) < 5:
                continue

            for j in range(i + 1, len(group)):
                if group[j]['id'] in remove_ids:
                    continue
                if not dates[j] or not norms[j] or len(norms[j]) < 5:
                    continue

                delta = abs((dates[j] - dates[i]).days)
                if delta > days_window:
                    break

                comparisons += 1

                if not quick_prefilter(norms[i], norms[j]):
                    continue

                sim = similarity(norms[i], norms[j])

                if sim >= threshold:
                    if event_score(group[i]) >= event_score(group[j]):
                        remove_ids.add(group[j]['id'])
                    else:
                        remove_ids.add(group[i]['id'])
                        break

    print(f"  Cross-lang comparisons: {comparisons}", flush=True)
    return remove_ids, comparisons


# ===================== 主流程 =====================

def main():
    parser = argparse.ArgumentParser(description='智能四层去重')
    parser.add_argument('--dry', action='store_true', help='试运行，不保存')
    parser.add_argument('--days', type=int, default=14, help='模糊去重时间窗口（默认14天）')
    parser.add_argument('--threshold', type=float, default=0.75, help='模糊去重相似度阈值（默认0.75）')
    args = parser.parse_args()

    print("Loading events...")
    events = load_events()
    original_count = len(events)
    print(f"Total events: {original_count}")

    all_remove = set()

    # Layer 1: URL 去重
    print("\n--- Layer 1: URL dedup ---")
    url_dups = dedup_by_url(events)
    print(f"  URL duplicates: {len(url_dups)}")
    all_remove |= url_dups

    # Layer 2: 标题指纹去重
    print("\n--- Layer 2: Title hash dedup (cross-date) ---")
    hash_dups = dedup_by_title_hash(events, all_remove)
    print(f"  Title hash duplicates: {len(hash_dups)}")
    all_remove |= hash_dups

    # Layer 3: 模糊相似度去重
    print(f"\n--- Layer 3: Fuzzy similarity dedup (±{args.days} days, sim>={args.threshold}) ---")
    fuzzy_dups, comparisons = dedup_by_fuzzy(events, all_remove, args.days, args.threshold)
    print(f"  Comparisons made: {comparisons}")
    print(f"  Fuzzy duplicates: {len(fuzzy_dups)}")
    all_remove |= fuzzy_dups

    # Layer 4: 跨语言去重
    print(f"\n--- Layer 4: Cross-language dedup (title_en, ±21 days, sim>=0.70) ---")
    cross_dups, cross_cmp = dedup_cross_language(events, all_remove, days_window=21, threshold=0.70)
    print(f"  Cross-language duplicates: {len(cross_dups)}")
    all_remove |= cross_dups

    # 汇总
    print(f"\n=== Summary ===")
    print(f"  Total events:       {original_count}")
    print(f"  Layer 1 (URL):      {len(url_dups)}")
    print(f"  Layer 2 (Title):    {len(hash_dups)}")
    print(f"  Layer 3 (Fuzzy):    {len(fuzzy_dups)}")
    print(f"  Layer 4 (X-Lang):   {len(cross_dups)}")
    print(f"  Total to remove:    {len(all_remove)}")
    print(f"  After dedup:        {original_count - len(all_remove)}")

    if not all_remove:
        print("\n[OK] No duplicates found!")
        return

    if args.dry:
        print("\n[DRY RUN] No changes saved. Run without --dry to apply.")
        return

    # 执行删除
    new_events = [e for e in events if e.get('id') not in all_remove]
    save_events(new_events)
    print(f"\n[OK] Dedup completed! Removed {len(all_remove)} duplicates.")


if __name__ == '__main__':
    main()
