#!/usr/bin/env python3
"""正确添加 founders 数据到 companyNameMap"""

# founders 数据映射 - 基于 _管理层.md
FOUNDERS_DATA = {
    'Figure AI': [{'name': 'Brett Adcock', 'title': '创始人'}],
    'Physical Intelligence': [
        {'name': 'Karol Hausman', 'title': 'CEO/创始人'},
        {'name': 'Chelsea Finn', 'title': '联合创始人'}
    ],
    '1X Technologies': [{'name': 'Bernt Øyvind Børnich', 'title': 'CEO/创始人'}],
    'Skild AI': [
        {'name': 'Abhinav Gupta', 'title': '创始人'},
        {'name': 'Deepak Pathak', 'title': 'CEO/创始人'}
    ],
    'Agility Robotics': [{'name': 'Jonathan Hurst', 'title': 'CTO/联合创始人'}],
    'Sunday Robotics': [{'name': '赵子豪', 'title': 'CEO/联合创始人'}],
    'Field AI': [{'name': 'Ali Agha', 'title': 'CEO/创始人'}],
    'Mimic Robotics': [{'name': 'Stefan Weirich', 'title': 'CEO/联合创始人'}],
    'Anybotics': [{'name': 'Péter Fankhauser', 'title': 'CEO/联合创始人'}],
    'Hexagon': [{'name': '奥洛夫·埃克斯特伦', 'title': '创始人'}],
    'Boston Dynamics': [{'name': 'Marc Raibert', 'title': '创始人'}],
    'Tesla Optimus': [{'name': 'Elon Musk', 'title': '主导负责人'}],
    '宇树科技': [{'name': '王兴兴', 'title': '创始人/CEO/CTO'}],
    '灵心巧手': [{'name': '周永', 'title': 'CEO/创始人'}],
    '银河通用': [
        {'name': '王鹤', 'title': '创始人/CTO'},
        {'name': '姚腾洲', 'title': '联合创始人/董事长'}
    ],
    '它石智航': [
        {'name': '陈亦伦', 'title': 'CEO/创始人'},
        {'name': '李震宇', 'title': '董事长'}
    ],
    '星海图': [{'name': '高阳', 'title': 'CEO/创始人'}],
    '星动纪元': [],  # 待补充
    '智元机器人': [
        {'name': '彭志辉', 'title': 'CTO/创始人'},
        {'name': '邓泰华', 'title': '董事长/CEO'},
        {'name': '罗剑岚', 'title': '首席科学家'}
    ],
    '傅利叶智能': [{'name': '顾捷', 'title': 'CEO/创始人'}],
    '至简动力': [
        {'name': '贾鹏', 'title': 'CEO/创始人'},
        {'name': '王凯', 'title': '董事长'}
    ],
    '光轮智能': [{'name': '谢晨', 'title': '创始人/董事长'}],
    '逐际动力': [
        {'name': '张巍', 'title': '创始人'},
        {'name': '庞博', 'title': '董事长'},
        {'name': '潘佳', 'title': '首席科学家'}
    ],
    '无界动力': [],  # 待补充
    '智平方': [{'name': '郭彦东', 'title': 'CEO/创始人'}],
    '千寻智能': [
        {'name': '韩峰涛', 'title': 'CEO/创始人'},
        {'name': '高阳', 'title': '首席科学家'}
    ],
    '自变量机器人': [
        {'name': '王潜', 'title': 'CEO/创始人'},
        {'name': '王昊', 'title': 'CTO/联合创始人'}
    ],
    '帕西尼感知': [{'name': '许晋诚', 'title': 'CEO/创始人'}],
    '普渡机器人': [{'name': '张涛', 'title': 'CEO/创始人'}],
    '魔法原子': [
        {'name': '陈春玉', 'title': 'CTO/联合创始人'},
        {'name': '李翔', 'title': '首席科学家'}
    ],
    '乐聚机器人': [
        {'name': '冷晓琨', 'title': '董事长/CTO'},
        {'name': '常琳', 'title': 'CEO'}
    ],
    '加速进化': [{'name': '程昊', 'title': 'CEO/创始人'}],
    '梅卡曼德': [{'name': '邵天兰', 'title': 'CEO/创始人'}],
    '灵初智能': [
        {'name': '王启斌', 'title': 'CEO/创始人'},
        {'name': '陈源培', 'title': '联合创始人'}
    ],
    '思灵机器人': [{'name': '陈兆芃', 'title': '法定代表人'}],
    '穹彻智能': [
        {'name': '王世全', 'title': '董事长/联合创始人'},
        {'name': '卢策吾', 'title': '联合创始人'}
    ],
    '破壳机器人': [{'name': '许华哲', 'title': '创始人'}],
    '大晓机器人': [
        {'name': '王晓刚', 'title': 'CEO'},
        {'name': '陶大程', 'title': '首席科学家'}
    ],
    '七腾机器人': [{'name': '朱冬', 'title': '创始人/董事长'}],
    '灵御智能': [{'name': '金戈', 'title': 'CEO/创始人'}],
    '觅蜂科技': [{'name': '姚卯青', 'title': '创始人'}],
    '跨维智能': [],  # 待补充
    '星尘智能': [
        {'name': '来杰', 'title': 'CEO/创始人'},
        {'name': '戴媛', 'title': '联合创始人'}
    ],
    '因时机器人': [],  # 待补充
    '珞石机器人': [],  # 待补充
    '地瓜机器人': [],  # 待补充
    '戴盟机器人': [],  # 待补充
    '宇叠智能': [],  # 待补充
    '镜识科技': [],  # 待补充
}

def add_founders_to_companynamemap():
    """添加 founders 数据到 companyNameMap"""
    with open('company.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到 companyNameMap 的起始和结束位置
    start_marker = "const companyNameMap = {"
    end_marker = "};"  # companyNameMap 结束的位置

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Error: companyNameMap not found")
        return

    # 找到 companyNameMap 对象的结束位置
    # 需要正确匹配嵌套的 { }
    brace_count = 0
    map_start = start_idx + len(start_marker)
    i = map_start
    in_string = False
    string_char = None

    while i < len(content):
        c = content[i]

        # 处理字符串
        if c in ('"', "'") and (i == 0 or content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = c
            elif c == string_char:
                in_string = False
                string_char = None

        if not in_string:
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    # 找到 companyNameMap 结束
                    map_end = i + 1
                    break
        i += 1

    print(f"Found companyNameMap at {start_idx} to {map_end}")

    # 提取 companyNameMap 内容
    old_map_content = content[map_start:map_end]
    new_map_lines = []
    changed = 0

    for line in old_map_content.split('\n'):
        new_line = line

        # 检查每行是否是一个条目
        # 格式: '公司名': { name: '公司名', nameEn: 'English Name' },
        import re
        match = re.match(r"\s+'([^']+)':\s*\{", line)
        if match:
            company_name = match.group(1)
            if company_name in FOUNDERS_DATA and FOUNDERS_DATA[company_name]:
                founders = FOUNDERS_DATA[company_name]
                # 将 founders 数据添加到条目中
                # 找到这一行中 } 之前的位置插入
                if line.rstrip().endswith('}'):
                    # 单行条目，需要扩展为多行
                    # 去掉末尾的 }
                    base_line = line.rstrip()[:-1]  # 去掉 }

                    # 构建 founders 数组字符串
                    founders_str = ', '.join([f"{{name: '{f['name']}', title: '{f['title']}'}}" for f in founders])
                    new_line = base_line + f"\n                    founders: [{founders_str}]\n            }}"
                    changed += 1
                    print(f"Added founders to: {company_name}")

        new_map_lines.append(new_line)

    new_map_content = '\n'.join(new_map_lines)
    new_content = content[:start_idx] + start_marker + '\n' + new_map_content + content[map_end:]

    with open('company.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nTotal companies modified: {changed}")

if __name__ == '__main__':
    add_founders_to_companynamemap()
