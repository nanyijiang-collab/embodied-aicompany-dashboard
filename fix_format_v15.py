#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复companies.html中的格式问题（双逗号）
"""

# 读取HTML文件
with open('companies.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 修复双逗号问题: ",, founders:" -> ", founders:"
html_content = html_content.replace(',, founders:', ', founders:')

# 修复 founders 后缺少逗号的问题: "}]  overseas:" -> "}], overseas:"
import re
# 匹配 founders数组结束后到下一个字段之间没有逗号的情况
# 模式: }] SPACE+ FIELD
html_content = re.sub(r'\}\]\s+(\w+:)', r'}], \1', html_content)

# 保存
with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("已修复格式问题并保存")
