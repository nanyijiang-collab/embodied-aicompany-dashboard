#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 v3
直接在1263行之后的区域更新或添加 founders
"""

from docx import Document
import re

# 读取docx文档
doc = Document(r'C:/Users/ZhuanZ/Desktop/公司管理层中文docx.docx')
lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# 解析公司管理层数据
companies_data = {}
current_company = None

def is_company_header(line):
    if re.match(r'^\d+\.\s*.+\s*[\(（]', line):
        return True
    return False

def is_person_line(line):
    if re.match(r'^[\u4e00-\u9fa5·]+[（(]', line):
        return True
    if re.match(r'^[A-Z][a-zA-Z]+ [A-Z][a-z]+[（(]', line):
        return True
    if re.match(r'^[A-Z][a-zA-Z]+ [A-Z][a-z]+ [A-Z][a-z]+[（(]', line):
        return True
    return False

# 解析
for line in lines:
    if is_company_header(line):
        m = re.match(r'^\d+\.\s*([^\s（(]+)\s*[\(（]([^\n）)]+)[\)）]?', line)
        if m:
            current_company = m.group(1)
            if current_company not in companies_data:
                companies_data[current_company] = []
    elif current_company and is_person_line(line):
        person = line.rstrip('。')
        if person and len(person) > 2:
            companies_data[current_company].append(person)

print(f"从文档提取到 {len(companies_data)} 家公司的管理层数据")

# 读取company.html
with open('company.html', 'r', encoding='utf-8') as f:
    lines_html = f.readlines()

# 找到1263行开始的位置
start_idx = None
for i, line in enumerate(lines_html):
    if '// === 以下为由Word文档数据更新的公司' in line:
        start_idx = i
        break

if start_idx is None:
    print("❌ 未找到更新区域起始位置")
    exit(1)

print(f"更新区域从第 {start_idx+1} 行开始")

# 公司名映射（文档名 -> 系统名）
name_mapping = {
    'NVIDIA': '英伟达 (NVIDIA)',
    'Tesla Optimus': 'Tesla Optimus',
    'Figure AI': 'Figure AI',
    '1X Technologies': '1X Technologies',
    'Hexagon': 'Hexagon',
    'Skild AI': 'Skild AI',
    'Physical Intelligence': 'Physical Intelligence',
    '智元机器人': '智元机器人',
    '宇树科技': '宇树科技',
    '星尘智能': '星尘智能',
    '银河通用': '银河通用',
    '苏度科技': '苏度科技',
    '星海图': '星海图',
    '至简动力': '至简动力',
    '逐际动力': '逐际动力',
    '普渡机器人': '普渡机器人',
    '灵心巧手': '灵心巧手',
    '优必选': '优必选',
    '因时机器人': '因时机器人',
    '卧安机器人': '卧安机器人',
    '光轮智能': '光轮智能',
    '它石智航': '它石智航',
    '智平方': '智平方',
    '千寻智能': '千寻智能',
    '自变量机器人': '自变量机器人',
    'Mimic Robotics': 'Mimic Robotics',
    'Anybotics': 'Anybotics',
    '加速进化': '加速进化',
    '帕西尼感知': '帕西尼感知',
    '穹彻智能': '穹彻智能',
    '魔法原子': '魔法原子',
    '乐聚机器人': '乐聚机器人',
    'Sunday Robotics': 'Sunday Robotics',
    '傅利叶智能': '傅利叶智能',
    'Agility Robotics': 'Agility Robotics',
    'Boston Dynamics': 'Boston Dynamics',
    '思灵机器人': '思灵机器人',
    '小鹏鹏行': '小鹏鹏行',
    '自然意志': '自然意志',
    'Field AI': 'Field AI',
    '梅卡曼德': '梅卡曼德',
    '破壳机器人': '破壳机器人',
    '灵初智能': '灵初智能',
    '珞石机器人': '珞石机器人',
    '地瓜机器人': '地瓜机器人',
    '觅蜂科技': '觅蜂科技',
    '大晓机器人': '大晓机器人',
    '七腾机器人': '七腾机器人',
    '云深处': '云深处',
    '简智机器人': '简智机器人',
    '戴盟机器人': '戴盟机器人',
    '跨维智能': '跨维智能',
    '优理奇智能': '优理奇智能',
    '智平方机器人': '智平方机器人',
    '松延动力': '松延动力',
    '开普勒人形机器人': '开普勒人形机器人',
    '理工华汇': '理工华汇',
    '卓益得机器人': '卓益得机器人',
    '天链机器人': '天链机器人',
    '国地具身智能': '国地具身智能',
    '青瞳视觉': '青瞳视觉',
}

# 解析人员信息
def parse_person_info(text):
    match = re.match(r'([^\（]+?)[\（(]([^\）)]+)[\)）]?', text)
    if match:
        name = match.group(1).strip()
        rest = match.group(2).strip()
        parts = rest.split('，')
        if len(parts) >= 1:
            title = parts[0].strip()
            bio = '，'.join(parts[1:]).strip() if len(parts) > 1 else ''
            return name, title, bio
    return text, '', ''

# 生成 founders 数组
def generate_founders_array(persons):
    founders = []
    for p in persons:
        name, title, bio = parse_person_info(p)
        if name:
            bio_str = f", bio: '{bio}'" if bio else ""
            founders.append(f"        {{name: '{name}', title: '{title}'{bio_str}}}")
    if founders:
        return f"    founders: [\n{', '.join(founders)}\n    ]"
    return ""

# 逐行处理，找到每个公司并添加/更新 founders
html_content = ''.join(lines_html)
updated_count = 0
added_count = 0

for doc_name, persons in companies_data.items():
    sys_name = name_mapping.get(doc_name, doc_name)

    if not persons:
        continue

    founders_str = generate_founders_array(persons)
    if not founders_str:
        continue

    # 在更新区域查找公司
    pattern = rf"'{re.escape(sys_name)}':\s*{{"
    match = re.search(pattern, html_content[start_idx:])

    if match:
        # 公司存在，检查是否已有 founders
        pos = start_idx + match.start()
        # 找这个公司的结束位置（下一个公司或文件结束）
        # 在 pos 位置找 }，确保在 founders 之后

        # 检查是否已有 founders 块
        founders_pattern = rf"'\{re.escape(sys_name)\}':\s*\{{[^}}]*?founders:\s*\[(.*?)\]"
        existing_match = re.search(founders_pattern, html_content[pos:pos+2000], re.DOTALL)

        if existing_match:
            # 已有 founders，替换
            old_founders = rf"founders:\s*\[(.*?)\]"
            new_block = f"founders: [\n{chr(10).join([l.strip() for l in founders_str.split(chr(10))])}\n    ]"
            # 使用精确替换
            old_start = pos + existing_match.start(0) + existing_match.group(0).find('founders:')
            old_end = old_start + len(existing_match.group(0)) - len(existing_match.group(1)) - 2

            html_content = html_content[:old_start] + new_block + html_content[old_end:]
            updated_count += 1
            print(f"✅ 更新: {sys_name} ({len(persons)} 人)")
        else:
            # 没有 founders，需要添加
            # 在公司定义的 } 之前添加 founders
            # 找到公司的结束位置
            insert_pos = html_content.find('}', pos + len(f"'{sys_name}': {"))
            if insert_pos > 0:
                # 找到安全的插入点（在 scene 或其他字段之后）
                # 尝试在最后一个字段后插入
                scene_pattern = rf"'\{re.escape(sys_name)\}':\s*\{{[^}}]*?scene:\s*'[^']*'"
                scene_match = re.search(scene_pattern, html_content[pos:pos+1000], re.DOTALL)
                if scene_match:
                    insert_pos = pos + scene_match.end(0)
                    # 在 scene 后面加逗号和 founders
                    html_content = html_content[:insert_pos] + ',\n' + founders_str + '\n' + html_content[insert_pos:]
                    added_count += 1
                    print(f"➕ 添加: {sys_name} ({len(persons)} 人)")
                else:
                    print(f"⚠️ 无法找到插入点: {sys_name}")
    else:
        # 公司不在更新区域，检查是否在旧区域
        old_pos = html_content.find(f"'{sys_name}': {{")
        if old_pos >= 0 and old_pos < start_idx:
            print(f"⚠️ 公司在旧区域: {sys_name}")
        else:
            print(f"❌ 公司不存在: {sys_name}")

# 保存更新后的 HTML
with open('company.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n共更新了 {updated_count} 家，新增了 {added_count} 家")