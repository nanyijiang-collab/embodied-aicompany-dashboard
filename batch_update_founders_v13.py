#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充添加14家公司的founders数据 - v13
"""

import re

# 从_管理层.md中提取的数据
founders_data = {
    "坤维科技 / 因时": [
        {"name": "蔡颖鹏", "title": "创始人兼CEO", "bio": "北京科技大学2004级校友，微型伺服运动控制领域"}
    ],
    "破壳机器人 (Poke)": [
        {"name": "许华哲", "title": "创始人", "bio": "清华大学交叉信息研究院助理教授，具身智能实验室负责人"}
    ],
    "灵初智能 (PsiBot)": [
        {"name": "王启斌", "title": "创始人兼CEO", "bio": "前黑莓、Sonos及云迹科技高管"},
        {"name": "陈源培", "title": "联合创始人", "bio": "00后创业先锋，斯坦福大学访问学者，师从李飞飞"},
        {"name": "杨耀东", "title": "首席科学家", "bio": "北京大学人工智能研究院助理教授"}
    ],
    "珞石机器人 (Ruoshi)": [
        {"name": "庹华", "title": "创始人兼CEO", "bio": "北京大学电子与通信工程硕士"},
        {"name": "曹华", "title": "联合创始人兼CTO", "bio": "法国鲁昂高等电子工程学院毕业"}
    ],
    "地瓜机器人 (Horizon)": [
        {"name": "余凯", "title": "法定代表人", "bio": "地平线创始人兼CEO"},
        {"name": "王丛", "title": "CEO", "bio": "2018年加入地平线，2020年接手AIoT团队"}
    ],
    "觅蜂科技 (Meef)": [
        {"name": "姚卯青", "title": "创始人", "bio": "智元机器人合伙人，高盛业务部总裁，清华+南加州大学背景"},
        {"name": "况旭", "title": "法定代表人"}
    ],
    "大晓机器人 (Daxiao)": [
        {"name": "王晓刚", "title": "CEO", "bio": "商汤科技联合创始人、执行董事，香港中文大学教授"},
        {"name": "陶大程", "title": "首席科学家", "bio": "澳大利亚科学院院士，前优必选首席科学家"},
        {"name": "刘春晓", "title": "法定代表人"}
    ],
    "七腾机器人 (Qiteng)": [
        {"name": "朱冬", "title": "创始人、董事长兼经理", "bio": "1989年出生，重庆邮电大学毕业，连续创业者"}
    ],
    "云深处 (DeepRobotics)": [
        {"name": "朱秋国", "title": "创始人兼CEO", "bio": "浙江大学副教授、博士生导师"},
        {"name": "李超", "title": "联合创始人兼CTO", "bio": "浙江大学博士，15年以上机器人研发经验"}
    ],
    "艾欧 (Io)": [
        {"name": "陈相羽", "title": "创始人兼CEO", "bio": "东京大学博士，机器人领域专家"},
        {"name": "高飙", "title": "联合创始人兼CTO", "bio": "北京大学博士，前百度萝卜快跑资深算法工程师"},
        {"name": "罗欣欣", "title": "联合创始人", "bio": "前腾讯15年行业资深专家"},
        {"name": "丁哲章", "title": "联合创始人", "bio": "北京大学硕士，前柯力传感机器人事业部负责人"}
    ],
    "戴盟 (Daimeng)": [
        {"name": "段江哗", "title": "创始人兼CEO", "bio": "中国科学院本硕博，香港科技大学博士后"},
        {"name": "王煜", "title": "联合创始人兼首席科学家", "bio": "大湾区大学讲席教授，香港科技大学机器人研究院创始院长"}
    ],
    "跨维智能 (Kuavi)": [
        {"name": "贾奎", "title": "董事长"},
        {"name": "贾俊", "title": "法定代表人、经理"}
    ],
    "宇叠 (Yudie)": [
        {"name": "王鑫", "title": "董事长、经理"}
    ],
    "镜识科技 (In-Sight)": [
        {"name": "王宏涛", "title": "联合创始人", "bio": "浙江大学求是特聘教授，交叉力学中心执行主任"},
        {"name": "金永斌", "title": "联合创始人", "bio": "浙江大学博士，师从杨卫院士，高速足式机器人专家"}
    ]
}

def make_founders_str(persons):
    """生成founders字符串"""
    entries = []
    for p in persons:
        name = p['name'].replace("'", "\\'")
        title = p['title'].replace("'", "\\'")
        bio = p.get('bio', '').replace("'", "\\'") if p.get('bio') else ''
        if bio:
            entries.append(f"{{name: '{name}', title: '{title}', bio: '{bio}'}}")
        else:
            entries.append(f"{{name: '{name}', title: '{title}'}}")
    if entries:
        return f", founders: [{', '.join(entries)}]"
    return ''

# 读取HTML文件
with open('companies.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("=== 补充添加14家公司的founders数据 ===\n")
updated_count = 0

for company_name, persons in founders_data.items():
    founders_str = make_founders_str(persons)

    # 查找公司对象
    # 模式: name:"公司名" 后紧跟其他字段
    pattern = rf'(name:"{re.escape(company_name)}"(?:,|\s)(?:overseas|brains|brain|training))'
    match = re.search(pattern, html_content)

    if not match:
        # 尝试另一种模式
        pattern = rf'(name:"{re.escape(company_name)}"(?:,|\s)(?:[a-z_]+:))'
        match = re.search(pattern, html_content)

    if match:
        # 检查是否已有founders
        # 找到这一行的结束位置
        start_pos = match.start()
        # 找下一个换行或对象结束
        line_end = html_content.find('\n', start_pos)
        if line_end == -1:
            line_end = len(html_content)

        # 检查这行或后面是否已有founders
        snippet = html_content[start_pos:line_end+50]
        if 'founders:' in snippet:
            print(f"[跳过] {company_name}: 已存在founders")
            continue

        # 在第一个字段前插入founders
        # name:"公司名",  -> name:"公司名", founders: [...], 
        insert_pos = match.end() - 1  # 在最后一个逗号前
        html_content = html_content[:insert_pos] + founders_str + ', ' + html_content[insert_pos:]
        print(f"[添加] {company_name}: {len(persons)}位创始人")
        updated_count += 1
    else:
        print(f"[未找到] {company_name} 在HTML中")

print(f"\n=== 完成：成功添加 {updated_count} 家公司 ===")

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("已保存到 companies.html")
