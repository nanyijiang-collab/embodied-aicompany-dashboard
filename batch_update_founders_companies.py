#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新公司管理层信息
直接在 companies.html 的 allCompanies 数组中添加 founders 字段
"""

import re
import os

# 读取 _管理层.md 数据
with open('_管理层.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 解析公司管理层数据
companies_data = {}
current_company = None

def is_company_header(line):
    """判断是否是公司标题行"""
    # 格式: 1. 公司名 (英文名) 或 1. 公司名
    if re.match(r'^\d+\.\s+.+', line):
        return True
    return False

def is_person_line(line):
    """判断是否是人员信息行"""
    # 中文名（职位）或 英文名（职位）
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
        # 提取公司名
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

# 公司名映射：文档名 -> allCompanies中的name
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
    '因时机器人': '因时机器人',
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
    '破壳机器人': '破壳机器人 (Poke)',
    '灵初智能': '灵初智能',
    '珞石机器人': '珞石机器人 (Rokae)',
    '地瓜机器人': '地瓜机器人 (Digua)',
    '觅蜂科技': '觅蜂科技 (Meef)',
    '大晓机器人': '大晓机器人 (Daxiao)',
    '七腾机器人': '七腾机器人 (Qiteng)',
    '云深处': '云深处 (DeepCloud)',
    '简智机器人': '简智机器人 (Jianzhi)',
    '跨维智能': '跨维智能 (Kuawe)',
    '优理奇智能': '优理奇智能 (YouLiQi)',
    '智平方机器人': '智平方机器人 (SmartSquare)',
    '松延动力': '松延动力 (Songyan)',
    '开普勒人形机器人': '开普勒人形机器人 (Kepler)',
    '理工华汇': '理工华汇 (Beijing Robot)',
    '天链机器人': '天链机器人 (Tianlian)',
    '国地具身智能': '国地具身智能 (国地中心)',
    '青瞳视觉': '青瞳视觉 (Qingtong)',
}

def parse_person(text):
    """解析人员信息，提取姓名、职位、简介"""
    m = re.match(r'([^\（]+?)[\（(]([^\）)]+)[\)）]?', text)
    if m:
        name = m.group(1).strip()
        rest = m.group(2).strip()
        parts = rest.split('，')
        title = parts[0].strip()
        bio = '，'.join(parts[1:]).strip() if len(parts) > 1 else ''
        return name, title, bio
    return text, '', ''

def make_founders_entry(persons):
    """生成 founders 字段的代码"""
    if not persons:
        return ''
    
    entries = []
    for p in persons:
        name, title, bio = parse_person(p)
        if name:
            # 转义单引号
            name_escaped = name.replace("'", "\\'")
            title_escaped = title.replace("'", "\\'")
            bio_escaped = bio.replace("'", "\\'") if bio else ''
            
            if bio_escaped:
                entry = f"        {{name: '{name_escaped}', title: '{title_escaped}', bio: '{bio_escaped}'}}"
            else:
                entry = f"        {{name: '{name_escaped}', title: '{title_escaped}'}}"
            entries.append(entry)
    
    if entries:
        return ",\n        founders: [\n" + ',\n'.join(entries) + "\n        ]"
    return ''

# 查找 allCompanies 数组的开始和结束位置
arr_start = html.find('const allCompanies = [')
arr_end = html.find('];', arr_start) + 2

print(f"allCompanies 数组位置: {arr_start} - {arr_end}")

# 统计
updated = 0
added = 0
not_found = []

for doc_name, persons in companies_data.items():
    sys_name = name_map.get(doc_name, doc_name)
    if not persons:
        continue
    
    founders_entry = make_founders_entry(persons)
    if not founders_entry:
        continue
    
    # 查找公司在 allCompanies 数组中的位置
    # 格式: { name:"公司名", ...
    search_pattern = f'name:"{sys_name}"'
    pos = html.find(search_pattern, arr_start, arr_end)
    
    if pos < 0:
        not_found.append(sys_name)
        print(f"❌ 未找到: {sys_name}")
        continue
    
    # 查找这个公司对象的结束位置（在下一个公司对象之前）
    # 找到 {name:"xxx"} 后的内容，直到下一个 { name: 或数组结束
    obj_start = html.rfind('{', 0, pos)
    
    # 找到这个对象的结束位置
    # 方法：从找到的位置往后，找 }, 或 }];
    # 简化处理：找下一个公司的 name:" 模式之前的位置
    next_company = html.find('name:"', pos + 10)
    
    if next_company < 0:
        # 可能是最后一个
        obj_end = arr_end - 1
    else:
        # 找前一个 } 的位置
        obj_end = html.rfind('}', 0, next_company)
    
    # 检查是否已有 founders
    old_obj = html[obj_start:obj_end+1]
    
    if 'founders' in old_obj:
        # 更新已有的 founders
        old_founders_start = old_obj.find('founders:')
        old_founders_end = old_obj.find(']', old_founders_start) + 1
        
        old_before = old_obj[:old_founders_start]
        # 找前一个逗号
        last_comma = old_before.rfind(',')
        if last_comma > 0:
            new_obj = old_before[:last_comma+1] + founders_entry + '\n' + old_obj[old_founders_end:]
        else:
            new_obj = old_before + founders_entry + '\n' + old_obj[old_founders_end:]
        
        html = html[:obj_start] + new_obj + html[obj_start + len(old_obj):]
        updated += 1
        print(f"✅ 更新: {sys_name} ({len(persons)}人)")
    else:
        # 添加 founders（在最后一个字段后）
        # 找到 positioning 字段的结束
        positioning_pos = old_obj.find("positioning:")
        if positioning_pos > 0:
            # 找到 positioning 值后的引号
            val_start = old_obj.find("'", positioning_pos) + 1
            val_end = old_obj.find("'", val_start)
            
            # 在 positioning 后添加 founders
            new_obj = old_obj[:val_end+1] + founders_entry + '\n' + old_obj[val_end+1:]
            
            # 调整总长度
            html = html[:obj_start] + new_obj + html[obj_start + len(old_obj):]
            added += 1
            print(f"➕ 添加: {sys_name} ({len(persons)}人)")
        else:
            print(f"⚠️ 无positioning字段: {sys_name}")

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n📊 结果:")
print(f"   更新 {updated} 家")
print(f"   添加 {added} 家")
print(f"   未找到 {len(not_found)} 家: {not_found[:5]}{'...' if len(not_found) > 5 else ''}")
