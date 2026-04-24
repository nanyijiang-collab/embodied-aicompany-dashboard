#!/usr/bin/env python3
"""
激进去重 - 基于关键词匹配去重
"""
import json
import re
import sys
import io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)
print(f"原始数据: {original_count} 条\n")

# 定义去重规则：同一公司 + 同一核心事件关键词
dedup_patterns = [
    # 银河通用
    (['银河通用', 'Galbot'], ['便利店', '入职', '上岗']),
    (['银河通用', 'Galbot'], ['春晚', '亮相']),
    (['魔法原子'], ['春晚', '机器人']),
    # 更多模式...
]

def get_event_key(company, title):
    """生成事件标识"""
    # 移除媒体后缀
    for suffix in [' - 新浪财经', ' - 东方财富', ' - 36氪', ' - 京报网', ' - 凤凰网',
                   ' - 新京报', ' - 证券时报', ' - 界面新闻', ' - 腾讯新闻', ' - 搜狐网',
                   ' - 网易', ' - 新华网', ' _手机新浪网', ' - eu.36kr.com', ' - MSN',
                   ' - 品玩', ' - Infoq.cn', ' - pudong.gov.cn', ' - 华声在线', ' - 中华网',
                   ' - 投中', ' - 大洋网', ' - 手机新浪网']:
        title = title.replace(suffix, '')
    return f"{company}:{title[:30]}"

# 按公司分组
company_events = defaultdict(list)
for e in data:
    company = e.get('company', '')
    title = e.get('title', '')
    company_events[company].append(e)

# 去重
removed = []
for company, events in company_events.items():
    # 按日期排序
    events_sorted = sorted(events, key=lambda x: x.get('date', ''))
    
    # 找出需要保留的（每个事件最早的那条）
    to_keep = []
    seen_events = set()
    
    for e in events_sorted:
        title = e.get('title', '')
        # 生成简化的事件标识
        event_id = title
        # 移除数字、时间等变化部分
        event_id = re.sub(r'\d+', '#', event_id)
        event_id = re.sub(r'[\d.]+[亿万]?[元人台个]?', '#N', event_id)
        event_id = event_id.lower()
        
        if event_id not in seen_events:
            to_keep.append(e)
            seen_events.add(event_id)
        else:
            removed.append(e)

# 统计移除情况
print(f"=== 去重结果 ===")
print(f"移除: {len(removed)} 条")

# 显示被移除的新闻
if removed:
    print("\n被移除的新闻示例:")
    for e in removed[:20]:
        print(f"  [{e.get('date')}] {e.get('company')}: {e.get('title', '')[:60]}")

# 创建新的数据列表
kept = [e for e in data if e not in removed]

# 保存
with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)

print(f"\n最终数据: {len(kept)} 条")
