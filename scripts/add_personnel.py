#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加人事动态事件到 events.json

数据来源：data/personnel.json（独立维护的人事动态数据库）
用法：
  python scripts/add_personnel.py          # 从 personnel.json 读取并添加到 events.json
  python scripts/add_personnel.py --check  # 仅检查新增条目，不写入
"""

import json
import os
import re
import sys
from datetime import datetime
from difflib import SequenceMatcher

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def load_events():
    path = os.path.join(PROJECT_DIR, 'data', 'events.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    path = os.path.join(PROJECT_DIR, 'data', 'events.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def load_personnel():
    """从 data/personnel.json 读取人事动态数据"""
    path = os.path.join(PROJECT_DIR, 'data', 'personnel.json')
    if not os.path.exists(path):
        print(f"[WARN] {path} not found, no personnel data to add")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_id(company, date, idx=0):
    """生成唯一ID"""
    prefix = company[:2]
    date_part = date.replace('-', '')[:6]
    return f"{prefix}{date_part}{idx:02d}"

def normalize_text(text):
    """标准化文本"""
    if not text:
        return ''
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().strip()

def similarity(a, b):
    """计算相似度"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def deduplicate_events(events):
    """三层去重"""
    seen = {}  # key: (company, date, title) -> event
    unique = []
    removed = 0
    
    for e in events:
        company = e.get('company', '')
        date = e.get('date', '')[:10]
        title = normalize_text(e.get('title', ''))
        event_id = e.get('id', '')
        
        key = (company, date, title)
        
        if key in seen:
            removed += 1
            continue
        
        # 相似度检查
        is_dup = False
        for existing_key in list(seen.keys()):
            ec, ed, et = existing_key
            if ec == company and ed == date and similarity(title, et) >= 0.8:
                is_dup = True
                removed += 1
                break
        
        if not is_dup:
            seen[key] = e
            unique.append(e)
    
    if removed > 0:
        print(f"  [Dedup] Removed {removed} duplicates")
    return unique

def is_personnel_exists(events, pe):
    """检查人事事件是否已存在于事件库中"""
    company = pe['company']
    date = pe['date']
    person_name = pe['person_name']
    action = pe['action']
    title_norm = normalize_text(pe['title'])
    for e in events:
        if e.get('company') != company:
            continue
        if e.get('date', '')[:10] != date:
            continue
        if e.get('person_name', '') == person_name and e.get('action', '') == action:
            return True
        # 标题相似度兜底
        if e.get('type') == 'personnel' and similarity(title_norm, normalize_text(e.get('title', ''))) >= 0.8:
            return True
    return False

def main():
    check_only = '--check' in sys.argv
    
    # 加载人事动态数据
    personnel_events = load_personnel()
    if not personnel_events:
        print("[INFO] No personnel data to process")
        return
    
    # 加载现有事件
    events = load_events()
    existing_ids = {e.get('id') for e in events}
    
    # 生成新事件（插入前去重检查）
    new_count = 0
    skipped = 0
    for pe in personnel_events:
        # 先检查是否已存在
        if is_personnel_exists(events, pe):
            skipped += 1
            continue
        
        event_id = generate_id(pe['company'], pe['date'])
        idx = 0
        while event_id in existing_ids:
            idx += 1
            event_id = generate_id(pe['company'], pe['date'], idx)
        existing_ids.add(event_id)
        
        event = {
            "id": event_id,
            "company": pe['company'],
            "type": "personnel",
            "title": pe['title'],
            "title_en": pe.get('title_en', ''),
            "summary": pe.get('summary', ''),
            "source": pe['source'],
            "source_url": pe['source_url'],
            "date": pe['date'],
            "created_at": datetime.now().isoformat(),
            "media_sources": [pe['source']],
            # 人事动态特有字段
            "person_name": pe['person_name'],
            "action": pe['action'],
            "old_role": pe.get('old_role', ''),
            "new_role": pe.get('new_role', '')
        }
        events.append(event)
        new_count += 1
        print(f"+ {pe['company']} - {pe['person_name']} {pe['action']} ({pe['date']})")
    
    if skipped > 0:
        print(f"\n[Skip] {skipped} existing personnel events skipped")
    
    if check_only:
        print(f"\n[CHECK] Would add {new_count} new personnel events (dry run)")
        return
    
    # 最终安全去重（防御性）
    print("\n[Dedup] Running deduplication...")
    events = deduplicate_events(events)
    
    # 保存
    save_events(events)
    print(f"[OK] Added {new_count} new personnel events")
    print(f"[Total] Current events: {len(events)}")

if __name__ == '__main__':
    main()
