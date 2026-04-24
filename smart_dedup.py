#!/usr/bin/env python3
"""
智能去重 - 同一公司+同一核心事件+同一日期 = 重复
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

# 删除暂无合作新闻
data = [e for e in data if '暂无合作' not in e.get('title', '')]
print(f"删除暂无合作后: {len(data)} 条")

def extract_core_event(company, title):
    """提取核心事件标识"""
    # 移除媒体后缀
    for suffix in [' - 新浪财经', ' - 东方财富', ' - 36氪', ' - 京报网', ' - 凤凰网',
                   ' - 新京报', ' - 证券时报', ' - 界面新闻', ' - 腾讯新闻', ' - 搜狐网',
                   ' - 网易', ' - 新华网', ' _手机新浪网', ' - eu.36kr.com', ' - MSN',
                   ' - 品玩', ' - Infoq.cn', ' - pudong.gov.cn', ' - 华声在线', ' - 中华网',
                   ' - 投中', ' - 大洋网', ' - 手机新浪网', ' - cnBeta', ' - thepaper']:
        title = title.replace(suffix, '')

    # 移除具体数字和变化部分
    title = re.sub(r'[\d.]+[亿万]+', '#N', title)
    title = re.sub(r'\d+%', '', title)
    title = re.sub(r'\d+日', '', title)
    title = re.sub(r'\d+台', '', title)
    title = re.sub(r'[\d.]+亿美元', '美元', title)

    # 标准化关键词
    keywords = []
    event_kws = ['发布', '推出', '亮相', '融资', '上市', 'IPO', '合作', '入职', '上岗',
                 '落地', '春晚', '签约', '投资', '收购', '裁员', '离职', '罢工']

    for kw in event_kws:
        if kw in title:
            keywords.append(kw)

    return ' '.join(keywords) if keywords else title[:10]

# 按 (公司, 日期, 核心事件) 分组
groups = defaultdict(list)
for e in data:
    company = e.get('company', '')
    date = e.get('date', '')[:10]  # 只取日期部分
    core = extract_core_event(company, e.get('title', ''))
    key = (company, date, core)
    groups[key].append(e)

# 去重：每个组只保留1条（保留标题最长的那个）
removed = []
kept = []

for key, events in groups.items():
    if len(events) > 1:
        # 按标题长度排序，保留最详细的
        events_sorted = sorted(events, key=lambda x: len(x.get('title', '')), reverse=True)
        kept.append(events_sorted[0])
        removed.extend(events_sorted[1:])
    else:
        kept.append(events[0])

print(f"\n=== 去重结果 ===")
print(f"发现重复组: {sum(1 for g in groups.values() if len(g) > 1)} 个")
print(f"移除: {len(removed)} 条")

# 显示被移除的新闻
if removed:
    # 按公司统计
    by_company = defaultdict(list)
    for e in removed:
        by_company[e.get('company', 'unknown')].append(e)

    print("\n被移除最多的公司:")
    for company, events in sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"  {company}: {len(events)} 条")

    print("\n被移除的新闻示例:")
    for e in removed[:20]:
        print(f"  [{e.get('date')}] {e.get('company')}: {e.get('title', '')[:60]}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)

print(f"\n最终数据: {len(kept)} 条")
