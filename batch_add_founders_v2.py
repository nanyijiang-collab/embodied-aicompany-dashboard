#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量添加公司founders数据到company.html
从_管理层.md提取管理层信息并匹配到company.html
"""

import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_founders_from_md(md_content):
    """从_管理层.md提取管理层信息"""
    founders_data = {}

    # 公司名称映射（MD名称 -> HTML名称）
    company_aliases = {
        'NVIDIA': 'NVIDIA',
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
        '坤维科技': '坤维科技',
        '因时机器人': '因时机器人',
        '卧安机器人': '卧安机器人',
        '光轮智能': '光轮智能',
        '它石智航': '它石智航',
        '智平方': '智平方',
        '千寻智能': '千寻智能',
        '自变量机器人': '自变量机器人',
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
        '艾欧智能': '艾欧智能',
        '戴盟机器人': '戴盟机器人',
        '跨维智能': '跨维智能',
        '宇叠智能': '宇叠智能',
        '镜识科技': '镜识科技',
        '优理奇智能': '优理奇智能',
        '松延动力': '松延动力',
        '开普勒人形机器人': '开普勒人形机器人',
        '理工华汇': '理工华汇',
        '智在无界': '智在无界',
        '卓益得机器人': '卓益得机器人',
        '天链机器人': '天链机器人',
        '国地具身智能': '国地具身智能',
        '青瞳视觉': '青瞳视觉',
        '北京人形机器人创新中心': '北京人形机器人创新中心',
        '优必选': '优必选',
        'Mimic Robotics': 'Mimic Robotics',
        'Anybotics': 'Anybotics',
        '加速进化': '加速进化',
        '帕西尼感知': '帕西尼感知',
        '穹彻智能': '穹彻智能',
        '智平方机器人': '智平方',
    }

    # 从MD内容提取管理层信息
    lines = md_content.split('\n')
    current_company = None
    current_founders = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 检测公司名称行
        for md_name in company_aliases:
            if line.startswith(md_name) or f'{md_name} (' in line or f'{md_name}（' in line:
                # 保存前一个公司的数据
                if current_company and current_founders:
                    html_name = company_aliases.get(current_company, current_company)
                    if html_name not in founders_data:
                        founders_data[html_name] = current_founders

                current_company = md_name
                current_founders = []
                break

        # 提取创始人/管理层
        if current_company:
            # 创始人
            founder_match = re.search(r'创始人[：:]\s*([^（(]+?)(?:（|$)', line)
            if founder_match:
                name = founder_match.group(1).strip()
                if name and len(name) <= 20 and not name.startswith('核心'):
                    current_founders.append({'name': name, 'title': '创始人'})

            # CEO
            if 'CEO' in line and '创始人' not in line:
                ceo_match = re.search(r'([^（(（）)\s]+)[（(]\s*CEO[^）)]*?[）)]', line)
                if ceo_match:
                    name = ceo_match.group(1).strip()
                    if name and len(name) <= 10:
                        current_founders.append({'name': name, 'title': 'CEO'})

            # 联合创始人
            cofounder_match = re.search(r'联合创始人[^：:]*[：:]\s*([^（(]+?)(?:（|$)', line)
            if cofounder_match:
                name = cofounder_match.group(1).strip()
                if name and len(name) <= 20:
                    current_founders.append({'name': name, 'title': '联合创始人'})

            # 首席科学家
            if '首席科学家' in line or '首席科学官' in line:
                cs_match = re.search(r'([^（(（）)\s]+)[（(]\s*首席科学家[^）)]*?[）)]', line)
                if cs_match:
                    name = cs_match.group(1).strip()
                    if name and len(name) <= 10:
                        current_founders.append({'name': name, 'title': '首席科学家'})

            # 董事长
            if '董事长' in line:
                chairman_match = re.search(r'([^（(（）)\s]+)[（(]\s*董事长[^）)]*?[）)]', line)
                if chairman_match:
                    name = chairman_match.group(1).strip()
                    if name and len(name) <= 10:
                        current_founders.append({'name': name, 'title': '董事长'})

        i += 1

    # 保存最后一个公司
    if current_company and current_founders:
        html_name = company_aliases.get(current_company, current_company)
        if html_name not in founders_data:
            founders_data[html_name] = current_founders

    return founders_data

def add_founders_to_html(html_content, founders_data):
    """将founders数据添加到HTML中每个公司的配置中"""

    # 统计
    added = 0
    skipped = 0

    for company_name, persons in founders_data.items():
        if not persons:
            continue

        # 生成founders字符串
        founders_str = ', '.join([
            f"{{name: '{p['name']}', title: '{p['title']}'}}"
            for p in persons[:5]  # 最多5个人
        ])

        # 查找公司定义位置
        # 格式: '公司名': { ... }
        pattern = rf"('{re.escape(company_name)}':\s*\{{[^}}]*\}})"

        # 尝试找到公司定义的结束位置
        match = re.search(rf"'{re.escape(company_name)}':\s*\{{", html_content)

        if match:
            start = match.start()
            # 找到这个公司的闭合括号
            depth = 0
            pos = match.start()
            while pos < len(html_content):
                if html_content[pos] == '{':
                    depth += 1
                elif html_content[pos] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                pos += 1

            if depth == 0:
                # 在闭合括号前添加founders
                insert_pos = pos
                insert_content = f",\n                    founders: [{founders_str}]"

                # 检查是否已有founders
                existing = html_content[start:pos].find('founders:')
                if existing == -1:
                    html_content = html_content[:insert_pos] + insert_content + html_content[insert_pos:]
                    added += 1
                    print(f"  添加: {company_name} ({len(persons)}人)")
                else:
                    skipped += 1
                    print(f"  跳过(已有): {company_name}")

    return html_content, added, skipped

def main():
    print("=" * 60)
    print("批量添加公司founders数据")
    print("=" * 60)

    # 读取文件
    print("\n[1/3] 读取_管理层.md...")
    md_content = read_file('_管理层.md')
    print(f"      已读取 {len(md_content)} 字符")

    print("\n[2/3] 提取管理层信息...")
    founders_data = extract_founders_from_md(md_content)
    print(f"      提取到 {len(founders_data)} 家公司的管理层信息")

    print("\n[3/3] 添加到company.html...")
    html_content = read_file('company.html')

    html_content, added, skipped = add_founders_to_html(html_content, founders_data)

    # 保存
    write_file('company.html', html_content)

    print(f"\n完成! 添加: {added}, 跳过: {skipped}")
    print(f"总行数: {len(html_content.splitlines())}")

if __name__ == '__main__':
    main()
