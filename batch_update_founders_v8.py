#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 v2
直接在 companies.html 的 allCompanies 数组中添加 founders 字段
"""

import re

# 读取 _管理层.md 数据
with open('_管理层.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 解析公司管理层数据
companies_data = {}
current_company = None

def is_company_header(line):
    if re.match(r'^\d+\.\s+.+', line):
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

lines = content.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    
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

print(f"从 _管理层.md 提取到 {len(companies_data)} 家公司")

# 读取 companies.html
with open('companies.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 公司名映射
name_map = {
    'NVIDIA': 'NVIDIA (英伟达)',
    'Tesla Optimus': 'Tesla Optimus (特斯拉)',
    'Figure AI': 'Figure AI',
    '1X Technologies': '1X Technologies',
    'Hexagon': 'Hexagon (海克斯康)',
    'Skild AI': 'Skild AI',
    'Physical Intelligence': 'Physical Intelligence',
    '智元机器人': '智元机器人 (Agibot)',
    '宇树科技': '宇树科技 (Unitree)',
    '星尘智能': '星尘智能 (Stardust)',
    '银河通用': '银河通用 (Galbot)',
    '苏度科技': '苏度科技 (Sudo)',
    '星海图': '星海图 (Galaxea)',
    '至简动力': '至简动力 (Simple)',
    '逐际动力': '逐际动力 (LimX)',
    '普渡机器人': '普渡机器人 (Pudu)',
    '灵心巧手': '灵心巧手 (Linkhou)',
    '优必选': '优必选 (UBTECH)',
    '卧安机器人': '卧安机器人 (Woan)',
    '光轮智能': '光轮智能 (Lucid)',
    '它石智航': '它石智航 (T-Robot)',
    '智平方': '智平方 (SmartSquare)',
    '千寻智能': '千寻智能 (Seeker)',
    '自变量机器人': '自变量机器人',
    'Mimic Robotics': 'Mimic Robotics',
    'Anybotics': 'Anybotics',
    '加速进化': '加速进化 (RobotEra)',
    '帕西尼感知': '帕西尼感知 (PaXini)',
    '穹彻智能': '穹彻智能 (Omni)',
    '北京人形机器人创新中心': '北京人形机器人创新中心',
    '魔法原子': '魔法原子 (Magic Atom)',
    '乐聚机器人': '乐聚机器人 (Leju)',
    'Sunday Robotics': 'Sunday Robotics',
    '傅利叶智能': '傅利叶智能 (Fourier)',
    'Agility Robotics': 'Agility Robotics',
    'Boston Dynamics': 'Boston Dynamics',
    '思灵机器人': '思灵机器人 (Flexiv)',
    '小鹏鹏行': '小鹏鹏行 (Xpeng)',
    '自然意志': '自然意志 (NatureWill)',
    'Field AI': 'Field AI',
    '梅卡曼德': '梅卡曼德 (Mech-Mind)',
    'Sanctuary AI': 'Sanctuary AI',
    'Skydio': 'Skydio',
    'Apptronik': 'Apptronik',
    '灵御智能': '灵御智能',
    '无界动力': '无界动力',
    '墨奇智能': '墨奇智能',
    '星动纪元': '星动纪元',
    '钛虎机器人': '钛虎机器人',
    '超维动力': '超维动力',
    '星源智机器人': '星源智机器人',
    '诺亦腾': '诺亦腾',
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

def make_founders_str(persons):
    """生成 founders 数组的字符串"""
    if not persons:
        return ''
    
    entries = []
    for p in persons:
        name, title, bio = parse_person(p)
        if name:
            name_esc = name.replace("'", "\\'")
            title_esc = title.replace("'", "\\'")
            bio_esc = bio.replace("'", "\\'") if bio else ''
            
            if bio_esc:
                entry = f"            {{name: '{name_esc}', title: '{title_esc}', bio: '{bio_esc}'}}"
            else:
                entry = f"            {{name: '{name_esc}', title: '{title_esc}'}}"
            entries.append(entry)
    
    if entries:
        return ",\n        founders: [\n" + ',\n'.join(entries) + "\n        ]"
    return ''

# 统计
updated = 0
added = 0
not_found = []

for doc_name, persons in companies_data.items():
    sys_name = name_map.get(doc_name, doc_name)
    if not persons:
        continue
    
    founders_str = make_founders_str(persons)
    if not founders_str:
        continue
    
    # 在 allCompanies 数组中查找公司
    search = f'name:"{sys_name}"'
    pos = html.find(search)
    
    if pos < 0:
        not_found.append((doc_name, sys_name))
        continue
    
    # 找到这个公司的闭合括号 } 或 },  (对象结束)
    # 从 name:"xxx" 位置开始往后找
    # 首先找到 { 的位置
    brace_start = html.rfind('{', 0, pos)
    
    # 从 brace_start 开始，找到第一个 }, (表示对象结束)
    # 需要处理嵌套的 } 情况
    depth = 0
    i = brace_start
    found_end = False
    while i < len(html):
        if html[i] == '{':
            depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                # 找到了对象结束
                brace_end = i
                found_end = True
                # 检查后面是 , 还是 ]
                next_char = html[i+1] if i+1 < len(html) else ''
                break
        i += 1
    
    if not found_end:
        print(f"❌ 解析错误: {sys_name}")
        continue
    
    old_obj = html[brace_start:brace_end+1]
    
    # 检查是否已有 founders
    if 'founders' in old_obj:
        print(f"⏭️ 已有: {sys_name}")
        continue
    
    # 在 positioning 后添加 founders
    # positioning 字段格式: positioning:"..."
    pos_match = re.search(r'(positioning:"[^"]*")', old_obj)
    if pos_match:
        pos_end = brace_start + pos_match.end()
        new_obj = old_obj[:pos_end] + founders_str + old_obj[pos_end:]
    else:
        # 如果没有 positioning，就在 } 前添加
        new_obj = old_obj[:-1] + founders_str + "\n    " + old_obj[-1:]
    
    # 替换
    html = html[:brace_start] + new_obj + html[brace_end+1:]
    added += 1
    print(f"✅ 添加: {sys_name} ({len(persons)}人)")

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n📊 结果:")
print(f"   添加 {added} 家")
print(f"   未找到 {len(not_found)} 家:")
for doc, sys in not_found:
    print(f"      - {doc} -> {sys}")
