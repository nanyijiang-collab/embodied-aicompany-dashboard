#!/usr/bin/env python3
"""检查日期问题"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', encoding='utf-8') as f:
    data = json.load(f)

# 检查4月24日新闻的原始日期
print('=== April 24 News - Original Date Check ===')
count = 0
for e in data:
    if e.get('date') == '2026-04-24' and count < 10:
        print(f"Title: {e.get('title', '')[:50]}")
        print(f"  crawled_at: {e.get('crawled_at', 'N/A')}")
        print(f"  source_date: {e.get('source_date', 'N/A')}")
        print(f"  summary: {str(e.get('summary', ''))[:100]}")
        print()
        count += 1

# 检查魔法原子的春晚新闻
print('\n=== MagicLab Spring Festival News ===')
for e in data:
    if 'MagicLab' in str(e.get('company', '')) and 'Spring Festival' in str(e.get('title', '')):
        print(f"Date: {e.get('date')}")
        print(f"  crawled_at: {e.get('crawled_at', 'N/A')}")
        print(f"  Title: {e.get('title', '')[:80]}")
        print()

# 统计日期分布
print('\n=== Date Distribution ===')
dates = {}
for e in data:
    d = e.get('date', 'unknown')
    dates[d] = dates.get(d, 0) + 1

for d, c in sorted(dates.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"  {d}: {c}")
