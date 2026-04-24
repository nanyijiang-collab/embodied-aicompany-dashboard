#!/usr/bin/env python3
"""修复数据问题"""
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)
print(f"Original: {original_count} events")

# 1. 删除暂无合作新闻
no_coop = [e for e in data if '暂无合作' in e.get('title', '') or '没有合作意向' in e.get('title', '')]
print(f"\n=== Remove No-Cooperation News ({len(no_coop)}) ===")
for e in no_coop:
    print(f"  REMOVE: {e.get('title', '')[:60]}")

data = [e for e in data if '暂无合作' not in e.get('title', '') and '没有合作意向' not in e.get('title', '')]

# 2. 修复春晚新闻日期
print(f"\n=== Fix Spring Festival News Dates ===")
spring_festival_keywords = ['春晚', '马年春晚', '龙年春晚', '蛇年春晚']
for e in data:
    title = e.get('title', '')
    date = e.get('date', '')
    # 春晚通常在1月底到2月中旬
    if any(kw in title for kw in spring_festival_keywords):
        # 提取标题中的真实日期（如果有的话）
        # 马年春晚通常是2月左右
        if date > '2026-03-01':
            print(f"  {date} -> need to fix: {title[:50]}")
            # 尝试从标题中提取年份和月份
            # 对于春晚新闻，如果日期在3月之后，需要检查
            pass

# 3. 找出可能日期错误的新闻（比如4月24日但实际是旧新闻）
print(f"\n=== Check Suspicious April 24 News ===")
suspicious = []
for e in data:
    if e.get('date') == '2026-04-24':
        title = e.get('title', '')
        # 检查标题中是否包含旧日期
        import re
        # 查找标题中的日期模式
        date_patterns = re.findall(r'(\d{1,2})月(\d{1,2})日', title)
        if date_patterns:
            for m, d in date_patterns:
                month, day = int(m), int(d)
                if month <= 3:  # 1-3月的新闻不应该在4月24日
                    suspicious.append((e, f"{month}月{day}日"))

print(f"Suspicious April 24 news with earlier dates in title: {len(suspicious)}")
for e, date_str in suspicious[:10]:
    print(f"  {date_str}: {e.get('title', '')[:60]}")

# 4. 删除与具身智能无关的新闻
print(f"\n=== Check Irrelevant News ===")
# 一些明显不相关的关键词
irrelevant_patterns = ['瑞幸', '咖啡', 'ES9', 'L80', '瓶装咖啡']
irrelevant = []
for e in data:
    title = e.get('title', '')
    company = e.get('company', '')
    # 如果新闻既不涉及具身智能公司，也没有具身智能关键词
    if any(p in title for p in irrelevant_patterns):
        irrelevant.append(e)

print(f"Potentially irrelevant news: {len(irrelevant)}")
for e in irrelevant[:10]:
    print(f"  [{e.get('company')}] {e.get('title', '')[:60]}")

# 询问用户是否删除
print(f"\n--- Summary ---")
print(f"After removing no-cooperation: {len(data)} events")
print(f"Suspicious (date mismatch): {len(suspicious)}")
print(f"Irrelevant: {len(irrelevant)}")

# Save cleaned data
with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved cleaned data: {len(data)} events")
