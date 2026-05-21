#!/usr/bin/env python3
"""
更新 company.html，添加融资表格数据
"""

import re
from docx import Document

# 读取 Word 文档
doc = Document('C:/Users/ZhuanZ/Desktop/公司的融资轮次.docx')

# 提取所有表格数据
tables_data = []
for table in doc.tables:
    rows = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        rows.append(cells)
    tables_data.append(rows)

# 公司名与表格索引的映射（从 Word 文档顺序）
company_table_mapping = {
    'Figure AI': 0,           # 表格1
    '1X Technologies': 1,       # 表格2
    'Skild AI': 2,            # 表格3
    'Physical Intelligence': 3,  # 表格4
    '智元机器人': 4,           # 表格5
    '宇树科技': 5,             # 表格6
    '星尘智能': 6,             # 表格7
    '银河通用': 7,             # 表格8
    '苏度科技': 8,             # 表格9
    '星海图': 9,               # 表格10
    '至简动力': 10,             # 表格11
    '智平方': 11,               # 表格12
    '千寻智能': 12,             # 表格13
    '自变量机器人': 13,         # 表格14
    '魔法原子': 14,             # 表格15
    '乐聚机器人': 15,           # 表格16
    '优必选': 16,               # 表格17
    '它石智航': 17,              # 表格18
    '普渡机器人': 18,           # 表格19
    '灵御智能': 19,             # 表格20
    '穹彻智能': 20,             # 表格21
    '加速进化': 21,             # 表格22
    '帕西尼感知': 22,           # 表格23
    '简智机器人': 23,           # 表格24
    '艾欧': 24,                 # 表格25
    '戴盟机器人': 25,           # 表格26
    '思灵机器人': 26,           # 表格27
    '小鹏鹏行': 27,             # 表格28
    # 以下公司可能是新出现的
    'Boston Dynamics': 32,      # 表格33
    'Sunday Robotics': 31,     # 表格32
    'Field AI': 30,            # 表格31
    'Mimic Robotics': 29,      # 表格30
    'Agility Robotics': 33,    # 表格34
    'Anybotics': 18,           # 需要确认
    'Apptronik': 19,           # 需要确认
    'Sanctuary AI': 20,        # 需要确认
}

def table_to_js_format(table_rows):
    """将表格数据转换为 JavaScript fundingTable 格式"""
    if not table_rows or len(table_rows) < 2:
        return None

    # 第一行是表头，跳过
    header = table_rows[0]
    data_rows = table_rows[1:]

    funding_table = []
    for row in data_rows:
        if len(row) >= 5:
            entry = {
                'round': row[0] if row[0] else '—',
                'date': row[1] if row[1] else '—',
                'amount': row[2] if row[2] else '—',
                'valuation': row[3] if row[3] else '—',
                'investors': row[4] if row[4] else '—',
            }
            funding_table.append(entry)

    return funding_table

def escape_js_string(s):
    """转义 JavaScript 字符串"""
    if s is None:
        return '—'
    # 转义单引号和反斜杠
    s = s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    return s if s else '—'

# 读取 company.html
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 处理每个公司的融资数据
updates = []

for company_name, table_idx in company_table_mapping.items():
    if table_idx < len(tables_data):
        funding_table = table_to_js_format(tables_data[table_idx])
        if funding_table:
            # 构造 fundingTable JavaScript 代码
            table_lines = []
            for entry in funding_table:
                line = f"        {{ round: '{escape_js_string(entry['round'])}', date: '{escape_js_string(entry['date'])}', amount: '{escape_js_string(entry['amount'])}', valuation: '{escape_js_string(entry['valuation'])}', investors: '{escape_js_string(entry['investors'])}' }}"
                table_lines.append(line)
            funding_table_str = ",\n".join(table_lines)

            # 查找该公司的 milestones 数据
            pattern = rf"('{company_name}':\s*\{{[^}}]*?milestones:\s*\[.*?\]\s*,)"
            # 简化处理：找到 milestones 的位置并替换
            milestones_pattern = rf"(\.milestones\s*=\s*\[)(.*?)(\],\s*fundingNote)"

            match = re.search(rf"'{'" + company_name + r"'\}:\s*\{{[^}}]+milestones:\s*\[(.*?)\],\s*fundingNote:", content, re.DOTALL)
            if match:
                # 找到了 milestones 数据，需要替换
                old_milestones = match.group(1)

                # 构建新的 fundingTable
                new_funding_table = f"""        fundingTable: [
{chr(10).join([f"            {{ round: '{escape_js_string(e['round'])}', date: '{escape_js_string(e['date'])}', amount: '{escape_js_string(e['amount'])}', valuation: '{escape_js_string(e['valuation'])}', investors: '{escape_js_string(e['investors'])}' }}" for e in funding_table])}
        ],"""

                # 替换
                old_pattern = rf"milestones:\s*\[(.*?)\],\s*fundingNote"
                new_replacement = f"fundingTable: [\n" + "\n".join([f"            {{ round: '{escape_js_string(e['round'])}', date: '{escape_js_string(e['date'])}', amount: '{escape_js_string(e['amount'])}', valuation: '{escape_js_string(e['valuation'])}', investors: '{escape_js_string(e['investors'])}' }}" for e in funding_table]) + "\n        ],\n        fundingNote"

                new_content = re.sub(old_pattern, new_replacement, content, count=1, flags=re.DOTALL)

                if new_content != content:
                    updates.append(company_name)
                    content = new_content
                    print(f"✓ Updated {company_name}")
                else:
                    print(f"✗ Failed to update {company_name}")
            else:
                print(f"⚠ No milestones found for {company_name}")
        else:
            print(f"⚠ No valid data for {company_name} (table {table_idx})")
    else:
        print(f"⚠ Table index {table_idx} out of range for {company_name}")

# 写回文件
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/company.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n完成！共更新 {len(updates)} 家公司:")
for name in updates:
    print(f"  - {name}")
