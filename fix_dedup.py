# -*- coding: utf-8 -*-
"""对现有 events.json 按标题去重（保留第一条）"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 来源优先级（越高越优先保留）
SOURCE_PRIORITY = {
    'Google News': 1,
    '36Kr': 2,
    '量子位': 3,
    '虎嗅': 4,
    'IT之家': 4,
    'Bing News': 5,
    '晚点LatePost': 6,
    '甲子光年': 7,
    '腾讯新闻': 8,
    '新浪财经': 9,
    '搜狐': 10,
    '21世纪经济报道': 11,
    '中国日报': 12,
    '投中网': 13,
    '每日经济新闻': 14,
    '界面新闻': 15,
    '人民日报海外版': 16,
    'TechCrunch': 17,
}


def normalize_title(title):
    """标题规范化"""
    if not title:
        return ''
    return title.strip().lower()


def source_priority(source):
    """来源优先级，越小越优先"""
    return SOURCE_PRIORITY.get(source, 99)


def main():
    events_file = 'data/events.json'

    with open(events_file, 'r', encoding='utf-8') as f:
        events = json.load(f)

    print('Before dedup:', len(events), 'events')

    # 按标题分组，保留最优先来源的那一条
    seen_titles = {}  # normalized_title -> best_event
    dupes_removed = 0

    for e in events:
        norm = normalize_title(e.get('title', ''))
        if not norm:
            continue

        if norm not in seen_titles:
            # 第一条，直接保留
            seen_titles[norm] = e
        else:
            # 重复，比较来源优先级
            existing = seen_titles[norm]
            if source_priority(e.get('source', '')) < source_priority(existing.get('source', '')):
                seen_titles[norm] = e
                dupes_removed += 1
            else:
                dupes_removed += 1

    deduped = list(seen_titles.values())
    # 按日期倒序
    deduped.sort(key=lambda x: x.get('date', ''), reverse=True)

    print('After dedup:', len(deduped), 'events')
    print('Duplicates removed:', dupes_removed)

    # 统计来源分布
    sources = {}
    for e in deduped:
        s = e.get('source', 'unknown')
        sources[s] = sources.get(s, 0) + 1
    print('\nTop sources:')
    for s, c in sorted(sources.items(), key=lambda x: -x[1])[:15]:
        print(f'  {s}: {c}')

    # 保存
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print('\nSaved to', events_file)


if __name__ == '__main__':
    main()
