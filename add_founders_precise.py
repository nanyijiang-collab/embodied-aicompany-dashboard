#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确添加公司founders数据
直接使用硬编码的公司名-创始人映射
"""

import re

def add_founders_precise(html_content):
    """精确添加founders数据"""

    # 公司名 -> founders列表的映射
    founders_map = {
        # 国外公司
        'NVIDIA': [
            {'name': 'Jensen Huang', 'title': '创始人/CEO'},
        ],
        'Tesla Optimus': [
            {'name': 'Elon Musk', 'title': '主导负责人'},
        ],
        'Figure AI': [
            {'name': 'Brett Adcock', 'title': '创始人'},
        ],
        '1X Technologies': [
            {'name': 'Bernt Øyvind Børnich', 'title': 'CEO/创始人'},
        ],
        'Hexagon': [
            {'name': '奥洛夫·埃克斯特伦', 'title': '创始人'},
        ],
        'Skild AI': [
            {'name': 'Abhinav Gupta', 'title': '创始人'},
            {'name': 'Deepak Pathak', 'title': 'CEO/创始人'},
        ],
        'Physical Intelligence': [
            {'name': 'Karol Hausman', 'title': 'CEO/创始人'},
            {'name': 'Chelsea Finn', 'title': '联合创始人'},
        ],
        # 国内公司
        '智元机器人': [
            {'name': '彭志辉', 'title': 'CTO/创始人'},
            {'name': '邓泰华', 'title': '董事长/CEO'},
            {'name': '罗剑岚', 'title': '首席科学家'},
        ],
        '宇树科技': [
            {'name': '王兴兴', 'title': '创始人/CEO/CTO'},
        ],
        '星尘智能': [
            {'name': '来杰', 'title': 'CEO/创始人'},
        ],
        '银河通用': [
            {'name': '王鹤', 'title': '创始人/CTO'},
            {'name': '姚腾洲', 'title': '联合创始人/董事长'},
        ],
        '苏度科技': [
            {'name': '郑杨杰', 'title': 'CEO/创始人'},
        ],
        '星海图': [
            {'name': '高阳', 'title': 'CEO/创始人'},
        ],
        '至简动力': [
            {'name': '贾鹏', 'title': 'CEO/创始人'},
            {'name': '王凯', 'title': '董事长'},
        ],
        '逐际动力': [
            {'name': '张巍', 'title': '创始人'},
            {'name': '庞博', 'title': '董事长'},
            {'name': '潘佳', 'title': '首席科学家'},
        ],
        '普渡机器人': [
            {'name': '张涛', 'title': 'CEO/创始人'},
        ],
        '灵心巧手': [
            {'name': '周永', 'title': 'CEO/创始人'},
        ],
        '北京人形机器人创新中心': [
            {'name': '熊友军', 'title': '总经理/CEO'},
        ],
        '优必选': [
            {'name': '周剑', 'title': '创始人/CEO'},
        ],
        '它石智航': [
            {'name': '陈亦伦', 'title': 'CEO/创始人'},
            {'name': '李震宇', 'title': '董事长'},
        ],
        '智平方': [
            {'name': '郭彦东', 'title': 'CEO/创始人'},
        ],
        '千寻智能': [
            {'name': '韩峰涛', 'title': 'CEO/创始人'},
            {'name': '高阳', 'title': '首席科学家'},
        ],
        '自变量机器人': [
            {'name': '王潜', 'title': 'CEO/创始人'},
            {'name': '王昊', 'title': 'CTO/联合创始人'},
        ],
        '魔法原子': [
            {'name': '陈春玉', 'title': 'CTO/联合创始人'},
            {'name': '李翔', 'title': '首席科学家'},
        ],
        '乐聚机器人': [
            {'name': '冷晓琨', 'title': '董事长/CTO'},
            {'name': '常琳', 'title': 'CEO'},
        ],
        'Sunday Robotics': [
            {'name': '赵子豪', 'title': 'CEO/联合创始人'},
        ],
        '傅利叶智能': [
            {'name': '顾捷', 'title': 'CEO/创始人'},
        ],
        'Agility Robotics': [
            {'name': 'Jonathan Hurst', 'title': 'CTO/联合创始人'},
        ],
        'Boston Dynamics': [
            {'name': 'Marc Raibert', 'title': '创始人'},
        ],
        'Mimic Robotics': [
            {'name': 'Stefan Weirich', 'title': 'CEO/联合创始人'},
        ],
        'Anybotics': [
            {'name': 'Péter Fankhauser', 'title': 'CEO/联合创始人'},
        ],
        '加速进化': [
            {'name': '程昊', 'title': 'CEO/创始人'},
        ],
        '帕西尼感知': [
            {'name': '许晋诚', 'title': 'CEO/创始人'},
        ],
        '穹彻智能': [
            {'name': '王世全', 'title': '董事长/联合创始人'},
            {'name': '卢策吾', 'title': '联合创始人'},
        ],
        '思灵机器人': [
            {'name': '陈兆芃', 'title': '法定代表人'},
        ],
        '小鹏鹏行': [
            {'name': '韩键', 'title': '总经理/法定代表人'},
        ],
        '自然意志': [
            {'name': '丁宁', 'title': '创始人'},
        ],
        'Field AI': [
            {'name': 'Ali Agha', 'title': 'CEO/创始人'},
        ],
        '梅卡曼德': [
            {'name': '邵天兰', 'title': 'CEO/创始人'},
        ],
        '破壳机器人': [
            {'name': '许华哲', 'title': '创始人'},
        ],
        '灵初智能': [
            {'name': '王启斌', 'title': 'CEO/创始人'},
            {'name': '陈源培', 'title': '联合创始人'},
        ],
        '珞石机器人': [
            {'name': '庹华', 'title': 'CEO/创始人'},
        ],
        '地瓜机器人': [
            {'name': '王丛', 'title': 'CEO'},
        ],
        '觅蜂科技': [
            {'name': '姚卯青', 'title': '创始人'},
        ],
        '大晓机器人': [
            {'name': '王晓刚', 'title': 'CEO'},
            {'name': '陶大程', 'title': '首席科学家'},
        ],
        '七腾机器人': [
            {'name': '朱冬', 'title': '创始人/董事长'},
        ],
        '云深处': [
            {'name': '朱秋国', 'title': 'CEO/创始人'},
        ],
        '简智机器人': [
            {'name': '陈建兴', 'title': '创始人'},
        ],
        '艾欧智能': [
            {'name': '陈相羽', 'title': 'CEO/创始人'},
        ],
        '戴盟机器人': [
            {'name': '段江哗', 'title': 'CEO/创始人'},
        ],
        '跨维智能': [
            {'name': '贾奎', 'title': '董事长'},
        ],
        '宇叠智能': [
            {'name': '王鑫', 'title': '董事长/经理'},
        ],
        '镜识科技': [
            {'name': '王宏涛', 'title': '联合创始人'},
        ],
        '优理奇智能': [
            {'name': '杨丰瑜', 'title': 'CEO/创始人'},
            {'name': '王贺升', 'title': '首席科学家'},
        ],
        '松延动力': [
            {'name': '姜哲源', 'title': '创始人/董事长/CTO'},
        ],
        '开普勒人形机器人': [
            {'name': '杨华', 'title': '创始人'},
            {'name': '胡德波', 'title': 'CEO/联合创始人'},
        ],
        '理工华汇': [
            {'name': '黄强', 'title': '核心创始人'},
        ],
        '智在无界': [
            {'name': '卢宗青', 'title': '创始人'},
        ],
        '卓益得机器人': [
            {'name': '李清都', 'title': '创始人/法定代表人'},
        ],
        '天链机器人': [
            {'name': '胡天链', 'title': '法定代表人'},
        ],
        '国地具身智能': [
            {'name': '许彬', 'title': '总经理'},
        ],
        '光轮智能': [
            {'name': '谢晨', 'title': '创始人/董事长'},
        ],
        # 简化名称版本
        '艾欧': [
            {'name': '陈相羽', 'title': 'CEO/创始人'},
        ],
        '戴盟': [
            {'name': '段江哗', 'title': 'CEO/创始人'},
        ],
        '宇叠': [
            {'name': '王鑫', 'title': '董事长/经理'},
        ],
    }

    added = 0
    skipped = 0
    not_found = []

    for company_name, persons in founders_map.items():
        if not persons:
            continue

        # 生成founders字符串
        founders_str = ', '.join([
            f"{{name: '{p['name']}', title: '{p['title']}'}}"
            for p in persons
        ])

        # 查找公司定义位置
        pattern = rf"'{re.escape(company_name)}':\s*\{{"

        match = re.search(pattern, html_content)
        if not match:
            not_found.append(company_name)
            continue

        start = match.start()

        # 找到这个公司的闭合括号（需要平衡括号）
        depth = 0
        pos = match.start()
        in_string = False
        string_char = None

        while pos < len(html_content):
            char = html_content[pos]

            # 处理字符串
            if char in ('"', "'") and (pos == 0 or html_content[pos-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None

            # 只有不在字符串内时才计数括号
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        break

            pos += 1

        if depth != 0:
            print(f"  错误: 无法找到 {company_name} 的闭合括号")
            continue

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

    return html_content, added, skipped, not_found

def main():
    print("=" * 60)
    print("精确添加公司founders数据")
    print("=" * 60)

    with open('company.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"\n开始添加founders数据...")
    html_content, added, skipped, not_found = add_founders_precise(html_content)

    # 保存
    with open('company.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n完成!")
    print(f"  添加: {added}")
    print(f"  跳过(已有): {skipped}")
    print(f"  未找到: {len(not_found)} - {not_found}")
    print(f"  总行数: {len(html_content.splitlines())}")

if __name__ == '__main__':
    main()
