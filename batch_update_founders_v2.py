#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 v2
对于已有 founders 的公司，更新数据；对于没有 founders 的公司，添加 founders
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

# 读取company.html
with open('company.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

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
            founders.append(f"{{name: '{name}', title: '{title}'{bio_str}}}")
    if founders:
        return f"founders: [\n                        {', '.join(founders)}\n                    ]"
    return ""

# 更新计数器
updated_count = 0
added_count = 0

for doc_name, persons in companies_data.items():
    sys_name = name_mapping.get(doc_name, doc_name)

    if not persons:
        continue

    founders_str = generate_founders_array(persons)
    if not founders_str:
        continue

    # 情况1：公司有 founders，需要更新
    has_founders_pattern = rf"'{re.escape(sys_name)}':\s*\{{[^}}]*founders:\s*\["
    if re.search(has_founders_pattern, html_content):
        old_pattern = rf"('{re.escape(sys_name)}':\s*\{{[^}}]*?)founders:\s*\[.*?\](?:\s*\}})"
        new_str = rf"\1{founders_str}\n                    }}"
        new_content = re.sub(old_pattern, new_str, html_content, flags=re.DOTALL)
        if new_content != html_content:
            html_content = new_content
            updated_count += 1
            print(f"✅ 更新: {sys_name} ({len(persons)} 人)")
        else:
            print(f"⚠️ 匹配但未更新: {sys_name}")

    # 情况2：公司存在但没有 founders，需要添加
    else:
        company_pattern = rf"'{re.escape(sys_name)}':\s*\{{"
        if re.search(company_pattern, html_content):
            # 在公司定义中找到一个合适的位置添加 founders
            # 找到公司定义的结尾（通常是 } 后面跟下一个公司）
            # 或者在 description, tags 等字段之后添加

            # 尝试找到 description 字段的结尾，然后在它后面添加
            insert_pattern = rf"('{re.escape(sys_name)}':\s*\{{[^}}]*(?:description|tags|valuation|headquarters|founded)[^}}]*)(}})"
            insert_str = rf"\1, {founders_str}\n                    \2"

            new_content = re.sub(insert_pattern, insert_str, html_content, flags=re.DOTALL)
            if new_content != html_content:
                html_content = new_content
                added_count += 1
                print(f"➕ 添加: {sys_name} ({len(persons)} 人)")
            else:
                print(f"⚠️ 公司存在但无法添加: {sys_name}")
        else:
            print(f"❌ 公司不存在: {sys_name}")

# 保存更新后的 HTML
with open('company.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n共更新了 {updated_count} 家，新增了 {added_count} 家")
