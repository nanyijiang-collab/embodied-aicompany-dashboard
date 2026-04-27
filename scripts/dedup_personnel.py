#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人事动态去重脚本
基于 company + person_name + date + action 四元组去重
"""

import json
from collections import defaultdict

def load_events():
    with open('data/events.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def dedup_personnel():
    events = load_events()
    
    # 分离人事事件和非人事事件
    personnel = [e for e in events if e.get('type') == 'personnel']
    others = [e for e in events if e.get('type') != 'personnel']
    
    print(f"人事事件: {len(personnel)} 条")
    print(f"其他事件: {len(others)} 条")
    
    # 按 company + person_name + date + action 分组
    seen = defaultdict(list)
    for e in personnel:
        key = (e.get('company'), e.get('person_name'), e.get('date'), e.get('action'))
        seen[key].append(e)
    
    # 找出重复
    duplicates = {k: v for k, v in seen.items() if len(v) > 1}
    
    if not duplicates:
        print("\n[OK] 没有重复事件")
        return
    
    print(f"\n找到 {len(duplicates)} 组重复:")
    ids_to_remove = []
    
    for key in duplicates:
        items = duplicates[key]
        print(f"\n{key[0]} - {key[1]} {key[3]} ({key[2]})")
        for i, item in enumerate(items):
            marker = "[KEEP]" if i == 0 else "[REMOVE]"
            print(f"  {marker} {item.get('id')} - {item.get('title', '')[:60]}")
            if i > 0:
                ids_to_remove.append(item['id'])
    
    # 去重：保留每组第一条
    new_personnel = []
    for key in seen:
        new_personnel.append(seen[key][0])  # 只保留第一条
    
    print(f"\n去重后人事事件: {len(new_personnel)} 条")
    print(f"删除: {len(ids_to_remove)} 条重复")
    
    # 合并并保存
    new_events = others + new_personnel
    save_events(new_events)
    
    print(f"\n[OK] 总事件数: {len(new_events)}")

if __name__ == '__main__':
    dedup_personnel()
