#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息 - 正则替换版
使用正则精确匹配每个公司对象
"""

import re

# ========== 1. 解析 _管理层.md ==========
with open('_管理层.md', 'r', encoding='utf-8') as f:
    content = f.read()

companies_data = {}
current_company = None

for line in content.split('\n'):
    line = line.strip()
    if not line:
        continue
    
    # 公司标题
    m = re.match(r'^\d+\.\s*([^\s（(]+)\s*[\(（]([^\n）)]+)[\)）]?', line)
    if m:
        current_company = m.group(1)
        if current_company not in companies_data:
            companies_data[current_company] = []
        continue
    
    # 人员行
    if current_company:
        pm = re.match(r'^([\u4e00-\u9fa5·A-Za-z\s]+?)[（(](.+?)[)）]?\.?$', line)
        if pm:
            person = line.rstrip('。')
            if len(person) > 2:
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
            ne = name.replace("'", "\\'")
            te = title.replace("'", "\\'")
            be = bio.replace("'", "\\'") if bio else ''
            if be:
                entries.append(f"        {{name: '{ne}', title: '{te}', bio: '{be}'}}")
            else:
                entries.append(f"        {{name: '{ne}', title: '{te}'}}")
    if entries:
        return ",\n        founders: [\n" + ',\n'.join(entries) + "\n        ]"
    return ''

# ========== 4. 读取HTML ==========
with open('companies.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ========== 5. 查找并替换每个公司 ==========
added = 0
for doc_name, persons in companies_data.items():
    sys_name = name_map.get(doc_name, doc_name)
    fs_str = make_founders(persons)
    if not fs_str:
        continue
    
    # 查找公司对象：name:"公司名"
    # 匹配整个对象 { name:"xxx", ... }
    escaped_name = re.escape(sys_name)
    pattern = rf'(name:"{escaped_name}"[^}}]+?)(}},'
    
    # 检查是否已有 founders
    if f'name:"{sys_name}"' in html:
        # 找到这个公司在html中的位置
        pos = html.find(f'name:"{sys_name}"')
        if pos < 0:
            print(f"❌ 未找到: {sys_name}")
            continue
        
        # 从该位置往后找到 }, 结束
        end = html.find('}', pos)
        while end > pos:
            next_c = html[end + 1] if end + 1 < len(html) else ''
            if next_c == ',':
                break
            end = html.find('}', end + 1)
        
        if end < 0:
            print(f"❌ 解析错误: {sys_name}")
            continue
        
        # 检查是否已有 founders
        obj = html[pos:end+1]
        if 'founders' in obj:
            print(f"⏭️ 已有: {sys_name}")
            continue
        
        # 在 }, 前插入 founders
        insert_pos = end
        new_obj = obj[:-2] + fs_str + '\n    ' + obj[-2:]
        
        html = html[:pos] + new_obj + html[end+1:]
        added += 1
        print(f"✅ {sys_name} ({len(persons)}人)")

# ========== 6. 保存 ==========
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n📊 完成！添加了 {added} 家公司")
