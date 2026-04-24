#!/usr/bin/env python3
"""
关键词匹配去重 - 更激进的去重策略
"""
import json
import re
import sys
import io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)
print(f"原始数据: {original_count} 条\n")

def extract_event_keywords(company, title):
    """提取事件关键词"""
    # 移除媒体后缀
    for suffix in [' - 新浪财经', ' - 东方财富', ' - 36氪', ' - 京报网', ' - 凤凰网',
                   ' - 新京报', ' - 证券时报', ' - 界面新闻', ' - 腾讯新闻', ' - 搜狐网',
                   ' - 网易', ' - 新华网', ' _手机新浪网', ' - eu.36kr.com', ' - MSN',
                   ' - 品玩', ' - Infoq.cn', ' - pudong.gov.cn', ' - 华声在线', ' - 中华网',
                   ' - 投中', ' - 大洋网', ' - 手机新浪网']:
        title = title.replace(suffix, '')

    # 移除具体数字
    title = re.sub(r'[\d.]+[亿万]?[元人台个]?', '', title)
    title = re.sub(r'\d+%', '', title)

    # 提取核心词
    keywords = []
    # 常见企业简称
    company_aliases = {
        '银河通用': ['银河通用', 'Galbot', '盖博特'],
        '魔法原子': ['魔法原子', 'MagicLab'],
        '智元机器人': ['智元', 'AgiBot', 'Agibot'],
        '宇树科技': ['宇树', 'Unitree'],
    }

    # 获取公司关键词
    company_kws = company_aliases.get(company, [company])
    for kw in company_kws:
        if kw in title:
            keywords.append(kw)

    # 提取事件关键词
    event_patterns = [
        r'(发布|推出|亮相|入职|上岗|落地|合作)',
        r'(上市|IPO)',
        r'(春晚)',
    ]

    for pattern in event_patterns:
        match = re.search(pattern, title)
        if match:
            keywords.append(match.group(0))

    return ' '.join(keywords) if keywords else title[:20]

# 按公司分组
company_events = defaultdict(list)
for e in data:
    company = e.get('company', '')
    title = e.get('title', '')
    keywords = extract_event_keywords(company, title)
    company_events[company].append({
        'event': e,
        'keywords': keywords,
        'date': e.get('date', ''),
        'title': title
    })

# 去重
removed = []
kept_events = []

for company, events in company_events.items():
    events_sorted = sorted(events, key=lambda x: x['date'])
    seen_keywords = {}
    for item in events_sorted:
        e = item['event']
        kw = item['keywords']
        if kw not in seen_keywords:
            seen_keywords[kw] = e
            kept_events.append(e)
        else:
            existing = seen_keywords[kw]
            if e.get('date', '') < existing.get('date', ''):
                removed.append(existing)
                seen_keywords[kw] = e
                if existing in kept_events:
                    kept_events.remove(existing)
            else:
                removed.append(e)

print(f"=== 去重结果 ===")
print(f"移除: {len(removed)} 条")

by_company = defaultdict(list)
for e in removed:
    by_company[e.get('company', 'unknown')].append(e)

print("\n被移除最多的公司:")
for company, events in sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    print(f"  {company}: {len(events)} 条")

print("\n被移除的新闻示例:")
for e in removed[:30]:
    print(f"  [{e.get('date')}] {e.get('company')}: {e.get('title', '')[:60]}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(kept_events, f, ensure_ascii=False, indent=2)

print(f"\n最终数据: {len(kept_events)} 条")
