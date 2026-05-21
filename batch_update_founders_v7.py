#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 v7
直接在 companies 对象中更新 founders
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

print(f"从文档提取到 {len(companies_data)} 家公司")

# 读取HTML
with open('company.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 公司名映射
name_map = {
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

def parse_person(text):
    m = re.match(r'([^\（]+?)[\（(]([^\）)]+)[\)）]?', text)
    if m:
        name = m.group(1).strip()
        rest = m.group(2).strip()
        parts = rest.split('，')
        title = parts[0].strip()
        bio = '，'.join(parts[1:]).strip() if len(parts) > 1 else ''
        return name, title, bio
    return text, '', ''

def make_founders(persons):
    parts = []
    for p in persons:
        name, title, bio = parse_person(p)
        if name:
            b = f", bio: '{bio}'" if bio else ""
            parts.append(f"        {{name: '{name}', title: '{title}'{b}}}")
    if parts:
        return "    founders: [\n" + ',\n'.join(parts) + "\n    ]"
    return ""

updated = 0
added = 0

for doc_name, persons in companies_data.items():
    sys_name = name_map.get(doc_name, doc_name)
    if not persons:
        continue

    founders_str = make_founders(persons)
    if not founders_str:
        continue

    # 找公司（在 getCompanyInfo 函数的 companies 对象中）
    # 格式：'公司名': {
    key = f"'{sys_name}':"
    pos = html.find(key)
    if pos < 0:
        print(f"❌ 不存在: {sys_name}")
        continue

    # 只在公司对象的合理范围内搜索
    # 从当前位置往后取 2000 字符
    snippet = html[pos:pos+2000]

    # 检查是否已有 founders
    has_founders = 'founders: [' in snippet[:1000]

    if has_founders:
        # 替换现有 founders
        fs_start = snippet.find('founders:')
        # 找 founders 块的结束 ]
        bracket_count = 0
        started = False
        fs_end = fs_start + 8
        for i in range(fs_start + 8, len(snippet)):
            c = snippet[i]
            if c == '[':
                started = True
                bracket_count += 1
            elif c == ']':
                bracket_count -= 1
                if started and bracket_count == 0:
                    fs_end = pos + i + 1
                    break

        old_len = fs_end - (pos + fs_start)
        new_html = html[:pos + fs_start] + founders_str + html[pos + fs_end:]
        html = new_html
        updated += 1
        print(f"✅ 更新: {sys_name} ({len(persons)}人)")
    else:
        # 添加 founders（在 scene 字段后）
        # 注意：scene 后面用的是单引号
        scene_pos = snippet.find("scene: '")
        if scene_pos > 0:
            # 找到 scene 字段值的结束（找单引号后逗号）
            scene_end = scene_pos + 8  # 跳过 "scene: '"
            for i in range(scene_pos + 8, len(snippet)):
                if snippet[i] == "'":
                    scene_end = pos + i + 1
                    break

            new_html = html[:scene_end] + ",\n" + founders_str + "\n" + html[scene_end:]
            html = new_html
            added += 1
            print(f"➕ 添加: {sys_name} ({len(persons)}人)")
        else:
            print(f"⚠️ 无scene字段: {sys_name}")

# 保存
with open('company.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n更新 {updated} 家，添加 {added} 家")