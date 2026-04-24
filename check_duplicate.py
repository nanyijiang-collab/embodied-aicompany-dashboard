#!/usr/bin/env python3
"""检查新闻重复和来源"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查银河通用便利店入职新闻
print("=== Galbot Convenience Store News ===")
for e in data:
    if 'Galbot' in str(e.get('company', '')) and ('便利店' in e.get('title', '') or '入职' in e.get('title', '')):
        print(f"Date: {e.get('date')}")
        print(f"  Source: {e.get('source', '')}")
        print(f"  URL: {e.get('source_url', '')[:80]}")
        print(f"  Title: {e.get('title', '')[:80]}")
        print()

# 检查4月24日新闻的来源
print("\n=== April 24 News Sources ===")
apr24_sources = {}
for e in data:
    if e.get('date') == '2026-04-24':
        src = e.get('source', 'unknown')
        apr24_sources[src] = apr24_sources.get(src, 0) + 1

for src, count in sorted(apr24_sources.items(), key=lambda x: x[1], reverse=True):
    print(f"  {src}: {count}")

# 看看这些新闻是不是都是同一天爬的
print("\n=== Check Crawl Timestamp ===")
sample = [e for e in data if e.get('date') == '2026-04-24'][0]
print(f"Sample news date: {sample.get('date')}")
print(f"Sample source: {sample.get('source', '')}")
print(f"Sample title: {sample.get('title', '')[:80]}")
# 检查有没有原始日期字段
for key in sample.keys():
    if 'date' in key.lower() or 'time' in key.lower() or 'crawl' in key.lower():
        print(f"  {key}: {sample.get(key)}")
