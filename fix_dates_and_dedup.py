#!/usr/bin/env python3
"""
修复新闻日期和去重
1. 从新闻内容/标题中提取真实日期
2. 对相似新闻去重，保留最早报道
"""
import json
import re
import sys
import io
from datetime import datetime, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 加载数据
with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)
print(f"原始数据: {original_count} 条\n")

# ========== 1. 日期修复 ==========
print("=== 1. 修复新闻日期 ===")

def extract_date_from_text(text):
    """从文本中提取日期"""
    if not text:
        return None
    
    # 匹配模式：XX月XX日
    patterns = [
        r'(\d{1,2})月(\d{1,2})日',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if pattern == r'(\d{1,2})月(\d{1,2})日':
                month, day = int(match.group(1)), int(match.group(2))
                # 判断是2025还是2026年（春晚通常是农历新年）
                # 如果月份在1-2月，可能是年前的春晚，也可能是当年的
                if month <= 2:
                    return f"2026-02-{day:02d}"
                elif month >= 3:
                    return f"2026-{month:02d}-{day:02d}"
            elif pattern == r'(\d{4})年(\d{1,2})月(\d{1,2})日':
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                return f"{year}-{month:02d}-{day:02d}"
            elif pattern == r'(\d{4})-(\d{1,2})-(\d{1,2})':
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                return f"{year}-{month:02d}-{day:02d}"
    return None

# 春晚相关关键词
spring_festival_keywords = ['春晚', '马年春晚']
# 春晚通常在农历新年期间（1月底到2月中）
spring_festival_months = [1, 2]

fixed_count = 0
for e in data:
    title = e.get('title', '')
    summary = e.get('summary', '')
    current_date = e.get('date', '')
    
    # 如果是春晚新闻，尝试修复日期
    if any(kw in title for kw in spring_festival_keywords):
        extracted = extract_date_from_text(title)
        if extracted:
            # 检查是否需要修复（当前日期在3月之后但实际是春晚期间）
            current_month = int(current_date.split('-')[1]) if current_date else 0
            if current_month >= 3:
                e['date'] = extracted
                e['date_source'] = 'extracted_from_title'
                fixed_count += 1
                if fixed_count <= 10:
                    print(f"  修复: {current_date} -> {extracted}: {title[:50]}")

print(f"\n共修复 {fixed_count} 条春晚新闻日期")

# ========== 2. 去重 ==========
print("\n=== 2. 新闻去重 ===")

def normalize_text(text):
    """标准化文本用于比较"""
    if not text:
        return ""
    # 移除标点、特殊字符，统一空白
    text = re.sub(r'[，。！？、：；""''【】《》（）\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def extract_core_content(title, company):
    """提取新闻核心内容（去除媒体名称、时间、来源等）"""
    text = title.replace(company, '')
    # 移除常见媒体后缀
    suffixes = [' - 新浪财经', ' - 东方财富', ' - 36氪', ' - 京报网', ' - 凤凰网', 
               ' - 新京报', ' - 证券时报', ' - 界面新闻', ' - 腾讯新闻', ' - 搜狐网',
               ' - 网易', ' - 新华网', ' - 人民网', ' _手机新浪网', ' - eu.36kr.com',
               ' - MSN', ' - 机器之心', ' - 品玩', ' - Infoq.cn']
    for suffix in suffixes:
        text = text.replace(suffix, '')
    return text.strip()

def is_duplicate(e1, e2):
    """判断两条新闻是否重复"""
    t1, t2 = e1.get('title', ''), e2.get('title', '')
    c1, c2 = e1.get('company', ''), e2.get('company', '')
    
    # 不同公司不算重复
    if c1 != c2:
        return False
    
    # 提取核心内容
    core1 = extract_core_content(t1, c1)
    core2 = extract_core_content(t2, c2)
    
    # 完全相同
    if core1 == core2:
        return True
    
    # 标题相似度高（简单比较）
    if len(core1) > 10 and len(core2) > 10:
        # 计算公共子串长度比例
        common = set(core1.split()) & set(core2.split())
        if len(common) >= 3:
            return True
    
    return False

# 构建去重后的数据
seen = {}  # key: (company, core_content) -> earliest event
duplicates = []

for e in data:
    company = e.get('company', '')
    title = e.get('title', '')
    core = extract_core_content(title, company)
    key = (company, core)
    
    if key not in seen:
        seen[key] = e
    else:
        # 比较日期，保留最早的
        existing = seen[key]
        if e.get('date', '') < existing.get('date', ''):
            duplicates.append(existing)
            seen[key] = e
        else:
            duplicates.append(e)

deduped_count = len(duplicates)
deduped_data = list(seen.values())

print(f"发现重复新闻: {deduped_count} 条")
print(f"去重后数据: {len(deduped_data)} 条")

# 显示部分重复示例
if duplicates:
    print("\n重复新闻示例:")
    for d in duplicates[:10]:
        print(f"  [{d.get('date')}] {d.get('company')}: {d.get('title', '')[:60]}")

# 保存结果
with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(deduped_data, f, ensure_ascii=False, indent=2)

print(f"\n=== 总结 ===")
print(f"原始: {original_count} 条")
print(f"日期修复: {fixed_count} 条")
print(f"去重删除: {deduped_count} 条")
print(f"最终: {len(deduped_data)} 条")
