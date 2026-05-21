#!/usr/bin/env python3
"""全面修复 companyNameMap 格式问题 - 最终版"""

import re

def fix_company_html():
    with open('company.html', 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes = 0

    # 问题1: 灵心巧手等条目末尾缺少逗号
    # } 后面直接跟新条目
    content = re.sub(
        r"(founders: \[\{name: '周永', title: 'CEO/创始人'\}\])\n            \}",
        r"\1\n            },",
        content
    )
    fixes += 1
    print("Fixed: 灵心巧手 trailing comma")

    # 问题2: 无界动力格式错误
    # { name: '无界动力', nameEn: 'Wujie Dynamics' }, fundingTable:
    # 应该是: { name: '无界动力', nameEn: 'Wujie Dynamics', fundingTable:
    content = re.sub(
        r"(\{ name: '无界动力', nameEn: 'Wujie Dynamics' \}), fundingTable:",
        r"\1, fundingTable:",
        content
    )
    fixes += 1
    print("Fixed: 无界动力 format")

    # 问题3: 星海图等条目缺少逗号
    # ...}} 后面直接跟新条目
    content = re.sub(
        r"(founders: \[\{name: '高阳', title: '[^']+'\}\])\n            \}",
        r"\1\n            },",
        content
    )

    # 问题4: 傅利叶智能等条目格式问题
    # founders: [...}]}], fundingTable: -> founders: [...}], fundingTable:
    content = re.sub(
        r"(\{name: '[^']+', title: '[^']+'\}\}), fundingTable:",
        r"\1], fundingTable:",
        content
    )

    if content != original:
        with open('company.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nTotal fixes: {fixes}")
    else:
        print("\nNo changes")

if __name__ == '__main__':
    fix_company_html()
