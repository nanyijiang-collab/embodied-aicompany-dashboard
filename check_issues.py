#!/usr/bin/env python3
"""检查数据问题"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total: {len(data)}\n")

# Find issues and save to file
issues = []

print("=== Spring Festival/Panda News ===")
for e in data:
    title = e.get('title', '')
    if '春晚' in title or '熊猫' in title:
        line = f"Date: {e.get('date')}, Company: {e.get('company')}\n  Title: {title[:80]}"
        print(line)
        issues.append(('spring_festival', e))

print("\n=== No Cooperation News ===")
for e in data:
    title = e.get('title', '')
    if '暂无合作' in title or '无合作' in title or '没有合作' in title:
        line = f"Date: {e.get('date')}, Company: {e.get('company')}\n  Title: {title[:80]}"
        print(line)
        issues.append(('no_coop', e))

print("\n=== April 24 News ===")
count = 0
apr24 = []
for e in data:
    if e.get('date', '').startswith('2026-04-24'):
        apr24.append(e)
        count += 1
print(f"Total: {count}")
for e in apr24[:10]:
    print(f"  {e.get('company')}: {e.get('title', '')[:60]}")
if count > 10:
    print(f"  ... and {count-10} more")

# Save issue indices to fix later
with open('data/issues.json', 'w', encoding='utf-8') as f:
    json.dump([{'type': t, 'index': data.index(e)} for t, e in issues], f, ensure_ascii=False)
print(f"\nSaved {len(issues)} issues to data/issues.json")
