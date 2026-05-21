#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充添加14家公司的founders数据
"""

import re

def parse_md_for_company(md_content, company_keyword):
    """从_管理层.md中提取指定公司的管理层信息"""
    lines = md_content.split('\n')
    results = []
    in_target = False
    current_company = ""

    for i, line in enumerate(lines):
        stripped = line.strip()
        # 检测公司标题
        if stripped and not stripped.startswith('#') and not stripped.startswith('说明'):
            # 检查是否包含关键词
            if any(kw in stripped for kw in company_keyword.split(',')):
                in_target = True
                current_company = stripped
                continue
            elif in_target and stripped.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.')):
                # 遇到新公司标题，停止
                in_target = False
        elif in_target:
            # 解析管理层行
            if '创始人' in stripped or 'CEO' in stripped or 'CTO' in stripped or 'COO' in stripped or '联合创始人' in stripped or '首席' in stripped or '总经' in stripped or '董事' in stripped or '负责人' in stripped or '非执行' in stripped or '监事' in stripped:
                # 提取姓名和职位
                match = re.match(r'([^：:]+)[:：](.+)', stripped)
                if match:
                    name_part = match.group(1).strip()
                    title_part = match.group(2).strip()
                    # 提取姓名（去掉"前XX"等前缀）
                    name = re.sub(r'^(原创|现任|前|原|新任|联)', '', name_part).strip()
                    if name and len(name) >= 2:
                        results.append({'name': name, 'title': title_part})

    return results

def make_founders_str(persons):
    """生成founders字符串"""
    if not persons:
        return ''
    entries = []
    for p in persons:
        name = p['name'].replace("'", "\\'")
        title = p['title'].replace("'", "\\'")
        bio_match = re.search(r'[(（]([^)）]+)[)）]', title)
        bio = ''
        if bio_match:
            bio = bio_match.group(1).strip()
            title = re.sub(r'[(（][^)）]+[)）]', '', title).strip()
        if bio:
            entries.append(f"{{name: '{name}', title: '{title}', bio: '{bio}'}}")
        else:
            entries.append(f"{{name: '{name}', title: '{title}'}}")
    if entries:
        return f", founders: [{', '.join(entries)}]"
    return ''

# 读取文件
with open('companies.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

with open('_管理层.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 定义14家公司的映射关系
# md中的关键词 -> html中的目标名称
company_mapping = [
    ('因时机器人', '坤维科技 / 因时'),
    ('破壳机器人', '破壳机器人 (Poke)'),
    ('灵初智能', '灵初智能 (PsiBot)'),
    ('珞石机器人', '珞石机器人 (Ruoshi)'),
    ('地瓜机器人', '地瓜机器人 (Horizon)'),
    ('觅蜂科技', '觅蜂科技 (Meef)'),
    ('大晓机器人', '大晓机器人 (Daxiao)'),
    ('七腾机器人', '七腾机器人 (Qiteng)'),
    ('云深处', '云深处 (DeepRobotics)'),
    ('艾欧智能', '艾欧 (Io)'),
    ('戴盟机器人', '戴盟 (Daimeng)'),
    ('跨维智能', '跨维智能 (Kuavi)'),
    ('宇叠智能', '宇叠 (Yudie)'),
    ('镜识科技', '镜识科技 (In-Sight)'),
]

print("=== 补充添加14家公司的founders数据 ===\n")
updated_count = 0

for md_keyword, html_name in company_mapping:
    # 从_管理层.md提取数据
    persons = parse_md_for_company(md_content, md_keyword)

    if not persons:
        print(f"[跳过] {md_keyword}: 未找到管理层数据")
        continue

    # 生成founders字符串
    founders_str = make_founders_str(persons)

    if not founders_str:
        print(f"[跳过] {md_keyword}: 生成founders失败")
        continue

    # 在HTML中找到对应公司
    # 查找模式: name:"公司名"
    pattern = rf'(name:"{re.escape(html_name)}",?\s*founders:)'
    if re.search(pattern, html_content):
        print(f"[跳过] {html_name}: 已存在founders")
        continue

    # 查找公司行
    pattern = rf'(name:"{re.escape(html_name)}"[\s\S]{{0,50}})'

    # 更精确的查找：找到公司对象
    # name:"公司名", 后面紧跟overseas或其他字段
    pattern = rf'(name:"{re.escape(html_name)}"(?:,|\s))([^{{]+)'
    match = re.search(pattern, html_content)

    if match:
        before = match.group(1)  # name:"公司名",
        after = match.group(2)   # overseas:false, brain:"..."

        # 检查是否已经有founders
        if 'founders' in after:
            print(f"[跳过] {html_name}: 已存在founders")
            continue

        # 在公司字段开始处插入founders
        new_text = before + founders_str + ', ' + after

        html_content = html_content[:match.start()] + new_text + html_content[match.end():]
        print(f"[添加] {html_name}: {len(persons)}位创始人")
        updated_count += 1
    else:
        print(f"[未找到] {html_name} 在HTML中")

print(f"\n=== 完成：成功添加 {updated_count} 家公司 ===")

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("已保存到 companies.html")
