#!/usr/bin/env python3
"""
批量添加融资数据到 company.html
"""
import re
import sys

# 读取生成的数据
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/generated_funding.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 generated_funding 字典
exec(content.replace('#!/usr/bin/env python3', '').replace('# -*- coding: utf-8 -*-', '').replace('"""Generated funding data"""', ''))
generated_funding = eval(content.split(' = ')[1])

print(f"已加载 {len(generated_funding)} 家公司融资数据")

# 读取 company.html
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/company.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 统计结果
added = []
not_found = []

for company, funding_code in generated_funding.items():
    # 查找公司定义的位置
    # 匹配模式: '公司名': { ... milestones: [...]
    pattern = rf"'{re.escape(company)}':\s*\{{[^}}]*milestones:\s*\[(.*?)\]"
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        # 找到里程碑数组的结束位置
        milestones_end = match.end()
        
        # 找到下一个 ] 后面紧跟的 , 或 }
        after_milestones = html_content[milestones_end:]
        # 找到 milestones 数组结束
        bracket_count = 0
        found_end = False
        for i, c in enumerate(after_milestones):
            if c == '[':
                bracket_count += 1
            elif c == ']':
                if bracket_count == 0:
                    # 找到结束
                    end_pos = milestones_end + i + 1
                    # 检查下一个字符是否是 , 或 }
                    next_char = html_content[end_pos:end_pos+1].strip()
                    if next_char in [',', '']:
                        # 在这里插入 fundingTable
                        insert_pos = end_pos
                        
                        # 构建要插入的代码
                        insert_code = ',\n' + funding_code + '\n'
                        
                        # 检查是否已经存在 fundingTable
                        before = html_content[end_pos-200:end_pos]
                        if 'fundingTable' in before:
                            print(f"⏭️ {company}: 已存在融资数据，跳过")
                            continue
                        
                        # 插入代码
                        html_content = html_content[:insert_pos] + insert_code + html_content[insert_pos:]
                        added.append(company)
                        print(f"✅ {company}: 已添加融资数据")
                        break
                else:
                    bracket_count -= 1
    else:
        not_found.append(company)
        print(f"⚠️ {company}: 在HTML中未找到")

# 保存修改后的文件
with open('c:/Users/ZhuanZ/WorkBuddy/20260422102414/company.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print()
print("=" * 60)
print("批量添加完成")
print("=" * 60)
print(f"✅ 成功添加: {len(added)} 家")
print(f"⚠️ 未找到: {len(not_found)} 家")
if not_found:
    print("\n未找到的公司:")
    for c in not_found:
        print(f"  - {c}")
