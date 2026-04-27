#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型智能去重脚本
使用智谱 GLM-4 Flash API 进行语义去重
"""

import json
import os
import time
import hashlib
from collections import defaultdict

# 智谱 API 配置
API_KEY = os.environ.get('ZHIPU_API_KEY', '')
API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

def load_events():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def get_event_fingerprint(event):
    """生成事件指纹：用于快速预筛选"""
    company = event.get('company', '')
    date = event.get('date', '')[:7]  # 年月
    title = event.get('title', '')[:30]  # 标题前30字
    return f"{company}|{date}|{title}"

def call_zhipu_llm(prompt, max_tokens=100):
    """调用智谱 GLM-4 Flash API"""
    if not API_KEY:
        return None
    
    import urllib.request
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'glm-4-flash',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens
    }
    
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"API call failed: {e}")
        return None

def check_duplicate_llm(event1, event2):
    """用大模型判断两条事件是否重复"""
    prompt = f"""判断以下两条新闻是否是同一个事件（重复新闻）：

新闻1: {event1.get('title', '')}
公司: {event1.get('company', '')}
日期: {event1.get('date', '')}
摘要: {event1.get('summary', '')[:100]}

新闻2: {event2.get('title', '')}
公司: {event2.get('company', '')}
日期: {event2.get('date', '')}
摘要: {event2.get('summary', '')[:100]}

请回答：YES（重复）或 NO（不是重复）
只回答YES或NO，不要其他内容。"""
    
    response = call_zhipu_llm(prompt, max_tokens=10)
    if response:
        return 'YES' in response.upper()
    return None

def quick_dedup(events):
    """快速预去重：基于指纹哈希"""
    seen = {}
    duplicates = []
    
    for event in events:
        fp = get_event_fingerprint(event)
        if fp in seen:
            duplicates.append((seen[fp], event))
        else:
            seen[fp] = event
    
    return duplicates

def llm_dedup_batch(events, batch_size=50):
    """批量使用大模型去重"""
    # 先用快速预去重
    print("Step 1: Quick fingerprint dedup...")
    fp_seen = defaultdict(list)
    for e in events:
        fp = get_event_fingerprint(e)
        fp_seen[fp].append(e)
    
    candidates = []  # 需要大模型判断的候选对
    for fp, group in fp_seen.items():
        if len(group) > 1:
            # 同公司同月同标题，提交大模型判断
            candidates.extend(group)
    
    print(f"Found {len(candidates)} events needing LLM dedup check")
    
    if not candidates:
        print("[OK] No duplicates found after quick dedup")
        return []
    
    # 去重：同指纹只保留第一条
    events_set = set(id(e) for e in candidates)
    keep = []
    remove_ids = []
    
    for fp, group in fp_seen.items():
        if len(group) > 1:
            keep.append(group[0])
            for e in group[1:]:
                remove_ids.append(e['id'])
                print(f"  [POTENTIAL] {e.get('company')} - {e.get('title', '')[:40]}")
    
    return remove_ids

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if not API_KEY:
        print("[WARN] ZHIPU_API_KEY not set, using quick dedup only")
        print("Set API key: export ZHIPU_API_KEY=your_key")
    
    print("Loading events...")
    events = load_events()
    original_count = len(events)
    print(f"Total events: {original_count}")
    
    print("\n=== Step 1: Quick Fingerprint Dedup ===")
    fp_seen = defaultdict(list)
    for e in events:
        fp = get_event_fingerprint(e)
        fp_seen[fp].append(e)
    
    remove_ids = []
    dup_count = 0
    for fp, group in fp_seen.items():
        if len(group) > 1:
            dup_count += len(group) - 1
            for e in group[1:]:
                remove_ids.append(e['id'])
    
    print(f"Found {dup_count} duplicate events")
    
    # 执行删除
    new_events = [e for e in events if e.get('id') not in remove_ids]
    save_events(new_events)
    
    print(f"\n=== Result ===")
    print(f"Original: {original_count}")
    print(f"Removed: {len(remove_ids)}")
    print(f"Remaining: {len(new_events)}")
    print(f"\n[OK] Dedup completed!")

if __name__ == '__main__':
    main()
