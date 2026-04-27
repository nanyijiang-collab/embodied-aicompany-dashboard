#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速字符串相似度去重
同公司 + 同日期 + 标题相似度 > 阈值 → 重复
"""

import json
import re
from difflib import SequenceMatcher

def load_events():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def normalize_text(text):
    """标准化文本：去除标点、转小写"""
    if not text:
        return ''
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点
    return text.lower().strip()

def similarity(a, b):
    """计算两个字符串的相似度 0-1"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def get_event_key(event):
    """生成事件分组键：公司+日期（到日）"""
    return f"{event.get('company', '')}|{event.get('date', '')[:10]}"

def find_duplicates(events, threshold=0.8):
    """找重复事件"""
    # 按公司+日期分组
    groups = {}
    for e in events:
        key = get_event_key(e)
        if key not in groups:
            groups[key] = []
        groups[key].append(e)
    
    # 在每组内找相似标题
    remove_ids = []
    total_dups = 0
    
    for key, group in groups.items():
        if len(group) < 2:
            continue
        
        # 比较每对事件
        to_remove = set()
        for i in range(len(group)):
            if group[i]['id'] in to_remove:
                continue
            for j in range(i + 1, len(group)):
                if group[j]['id'] in to_remove:
                    continue
                
                title1 = normalize_text(group[i].get('title', ''))
                title2 = normalize_text(group[j].get('title', ''))
                
                sim = similarity(title1, title2)
                
                if sim >= threshold:
                    # 相似度高，保留更详细的（摘要更长的）
                    len1 = len(group[i].get('summary', ''))
                    len2 = len(group[j].get('summary', ''))
                    
                    if len1 >= len2:
                        to_remove.add(group[j]['id'])
                    else:
                        to_remove.add(group[i]['id'])
                        break
        
        if to_remove:
            total_dups += len(to_remove)
            remove_ids.extend(list(to_remove))
    
    return remove_ids, total_dups

def main():
    print("Loading events...")
    events = load_events()
    original_count = len(events)
    print(f"Total events: {original_count}")
    
    print("\nFinding duplicates (similarity >= 0.8)...")
    remove_ids, dup_count = find_duplicates(events, threshold=0.8)
    
    print(f"Found {dup_count} duplicates to remove")
    
    if not remove_ids:
        print("\n[OK] No duplicates found!")
        return
    
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
