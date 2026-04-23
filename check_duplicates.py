# -*- coding: utf-8 -*-
import json
from collections import Counter

d = json.load(open('data/events.json', encoding='utf-8'))

sogou_links = [e for e in d if 'weixin.sogou.com' in e.get('source_url', '')]

# 统计重复的跳转链接
url_counts = Counter([e.get('source_url', '') for e in sogou_links])

print(f'搜狗跳转链接总数: {len(sogou_links)}')
print(f'唯一跳转链接数: {len(url_counts)}')
print(f'重复率: {(1 - len(url_counts)/len(sogou_links))*100:.1f}%')

print('\n=== 最常见的10个跳转链接 ===')
for url, count in url_counts.most_common(10):
    # 找出这些重复链接对应的新闻
    examples = [e.get('title', '')[:40] for e in sogou_links if e.get('source_url', '') == url][:3]
    print(f"\n链接 ({count}次使用): {url[:60]}...")
    for ex in examples:
        print(f"  - {ex}")
