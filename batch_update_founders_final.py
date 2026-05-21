#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 - 简洁版
按顺序逐行处理allCompanies数组
"""

import re

# ========== 1. 解析 _管理层.md ==========
with open('_管理层.md', 'r', encoding='utf-8') as f:
    content = f.read()

companies_data = {}
current_company = None

def is_company_header(line):
    return bool(re.match(r'^\d+\.\s+.+', line))

def is_person_line(line):
    return bool(re.match(r'^[\u4e00-\u9fa5·]+[（(]', line) or 
                 re.match(r'^[A-Z][a-zA-Z]+ [A-Z][a-z]+[（(]', line) or
                 re.match(r'^[A-Z][a-zA-Z]+ [A-Z][a-z]+ [A-Z][a-z]+[（(]', line))

for line in content.split('\n'):
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

print(f"解析到 {len(companies_data)} 家公司")

# ========== 2. 公司名映射 ==========
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
    '智平方机器人': '智平方机器人',
    '简智机器人': '简智机器人',
    '优理奇智能': '优理奇智能',
    '松延动力': '松延动力',
    '开普勒人形机器人': '开普勒人形机器人',
    '理工华汇': '理工华汇',
    '卓益得机器人': '卓益得机器人',
    '天链机器人': '天链机器人',
    '国地具身智能': '国地具身智能',
}

# ========== 3. 解析人员 ==========
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
    if not persons:
        return ''
    entries = []
    for p in persons:
        name, title, bio = parse_person(p)
        if name:
            ne, te, be = name.replace("'", "\\'"), title.replace("'", "\\'"), bio.replace("'", "\\'") if bio else ''
            if be:
                entries.append(f"            {{name: '{ne}', title: '{te}', bio: '{be}'}}")
            else:
                entries.append(f"            {{name: '{ne}', title: '{te}'}}")
    if entries:
        return ",\n        founders: [\n" + ',\n'.join(entries) + "\n        ]"
    return ''

# ========== 4. 读取HTML ==========
with open('companies.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ========== 5. 构建公司名->founders的查找表 ==========
founders_lookup = {}
for doc_name, persons in companies_data.items():
    sys_name = name_map.get(doc_name, doc_name)
    fs = make_founders(persons)
    if fs:
        founders_lookup[sys_name] = fs

# ========== 6. 逐行处理allCompanies数组 ==========
# 找到数组开始和结束
arr_start = html.find('const allCompanies = [')
arr_content_start = html.find('[', arr_start) + 1
arr_end = html.find('];', arr_start) + 2

# 取出数组内容
arr_content = html[arr_content_start:arr_end]

# 逐行处理
lines = arr_content.split('\n')
new_lines = []
i = 0
added = 0

while i < len(lines):
    line = lines[i]
    
    # 检查是否包含公司定义
    found = False
    for sys_name, fs_str in founders_lookup.items():
        if f'name:"{sys_name}"' in line:
            # 添加当前行
            new_lines.append(line.rstrip())
            
            # 收集后续行直到找到闭合括号
            obj_lines = [line]
            j = i + 1
            depth = line.count('{') - line.count('}')
            
            while j < len(lines) and depth > 0:
                obj_lines.append(lines[j])
                depth += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            # 检查是否已有 founders
            obj_text = '\n'.join(obj_lines)
            if 'founders' not in obj_text:
                # 在闭合括号前插入 founders
                closing_brace_idx = len(obj_text) - obj_text[::-1].find('}')
                closing_brace_idx = len(obj_text) - obj_text[::-1].index('}')
                
                # 找到 }, 或 } 的位置
                if obj_text.rstrip().endswith('},'):
                    insert_pos = len(obj_text) - 2
                else:
                    insert_pos = len(obj_text) - 1
                
                # 在闭合括号前插入 founders
                new_obj = obj_text[:insert_pos] + fs_str + '\n    ' + obj_text[insert_pos:]
                new_lines.extend(new_obj.split('\n'))
                added += 1
                print(f"✅ {sys_name}")
            else:
                new_lines.extend(obj_lines)
                print(f"⏭️ 已有: {sys_name}")
            
            # 跳过已处理的行
            i = j
            found = True
            break
    
    if not found:
        new_lines.append(line)
        i += 1

# ========== 7. 重建HTML ==========
new_arr_content = '\n'.join(new_lines)
new_html = html[:arr_content_start] + '\n' + new_arr_content + '\n' + html[arr_end:]

# ========== 8. 保存 ==========
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\n📊 完成！添加了 {added} 家公司")
