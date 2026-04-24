#!/usr/bin/env python3
"""检查不相关新闻"""
import json

with open('data/events.json', encoding='utf-8') as f:
    data = json.load(f)

# 找出明显不相关的新闻
irrelevant = []
for e in data:
    title = e.get('title', '')
    company = e.get('company', '')

    # 明显不相关的模式
    if any(k in title for k in ['RTX 4090', '显卡', '公版PCB', '显存', '成像仪', '故障', 'OpenAI Codex', '编程工具']) or \
       '英伟达' in title and not any(k in title for k in ['机器人', '具身', 'GR00T', 'Isaac', '人形', 'Digit', 'Atlas', 'Figure']):
        irrelevant.append({
            'company': company,
            'title': title,
            'date': e.get('date')
        })

print(f'明显不相关新闻数量: {len(irrelevant)}')
print('\n示例:')
for item in irrelevant[:20]:
    print(f"  [{item['company']}] {item['title'][:60]}")
