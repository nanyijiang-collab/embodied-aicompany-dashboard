#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 v9 - 精确版
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

# 公司名映射 (文档名 -> HTML中的name)
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
                entry = f"        {{name: '{name_esc}', title: '{title_esc}', bio: '{bio_esc}'}}"
            else:
                entry = f"        {{name: '{name_esc}', title: '{title_esc}'}}"
            entries.append(entry)
    
    if entries:
        return ",\n        founders: [\n" + ',\n'.join(entries) + "\n        ]"
    return ''

# 找到 allCompanies 数组的位置
arr_start = html.find('const allCompanies = [')
arr_content_start = html.find('[', arr_start) + 1
arr_end = html.find('];', arr_start) + 2

print(f"allCompanies 数组: {arr_content_start} - {arr_end}")

# 逐行处理
lines_html = html[arr_content_start:arr_end].split('\n')
new_lines = []
skip_until_brace_close = False
skipped_positions = []  # 记录跳过的位置，用于后续添加

for i, line in enumerate(lines_html):
    # 检查这行是否包含公司定义
    matched = False
    for doc_name, persons in companies_data.items():
        sys_name = name_map.get(doc_name, doc_name)
        if not persons:
            continue
        
        founders_str = make_founders_str(persons)
        if not founders_str:
            continue
        
        search = f'name:"{sys_name}"'
        if search in line:
            # 找到公司行，准备处理
            matched = True
            
            # 将当前行加入（公司定义）
            new_lines.append(line.rstrip())
            
            # 找到这行的闭合括号 } 或 }, 
            # 方法：在后续行中查找
            brace_count = line.count('{') - line.count('}')
            j = i + 1
            while j < len(lines_html) and brace_count > 0:
                brace_count += lines_html[j].count('{') - lines_html[j].count('}')
                j += 1
            
            # 如果 brace_count == 0，表示找到了闭合
            # 但实际上我们需要等闭合后再添加 founders
            # 所以先跳过这个对象，等闭合后再处理
            
            # 记录需要添加 founders 的位置（闭合括号后）
            skipped_positions.append({
                'at': len(new_lines) + j - 1,  # 将在 new_lines 的这个位置后添加
                'founders': founders_str,
                'name': sys_name
            })
            
            # 跳过后续行直到闭合
            for k in range(i + 1, j):
                new_lines.append(lines_html[k])
            
            break
    
    if not matched and not skip_until_brace_close:
        new_lines.append(line)

# 现在需要把 founders 添加到正确位置
# 由于跳过了闭合括号 } 或 }, 我们需要在那里插入

print(f"需要处理 {len(skipped_positions)} 家公司")

# 重新构建数组内容
new_arr_content = '\n'.join(new_lines)

# 对于每家需要添加的公司，找到其闭合位置并插入 founders
for item in skipped_positions:
    sys_name = item['name']
    founders_str = item['founders']
    
    # 找到 "name:"XXX"" 的位置
    search = f'name:"{sys_name}"'
    pos = new_arr_content.find(search)
    if pos < 0:
        print(f"❌ 找不到: {sys_name}")
        continue
    
    # 找到从该位置开始的第一个 }, 或 }
    end_pos = new_arr_content.find('}', pos)
    next_char = new_arr_content[end_pos + 1] if end_pos + 1 < len(new_arr_content) else ''
    
    if next_char == ',':
        # 对象以 }, 结束
        insert_pos = end_pos + 1
    else:
        # 对象以 } 结束（最后一个）
        insert_pos = end_pos
    
    new_arr_content = new_arr_content[:insert_pos] + founders_str + '\n    ' + new_arr_content[insert_pos:]
    print(f"✅ 添加: {sys_name}")

# 重建完整 HTML
new_html = html[:arr_content_start] + '\n' + new_arr_content + '\n' + html[arr_end:]

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\n✅ 完成！已更新 {len(skipped_positions)} 家公司")
