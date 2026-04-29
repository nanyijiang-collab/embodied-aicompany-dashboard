# -*- coding: utf-8 -*-
import re

with open('companies.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有 positioning 字段的值，用正则替换内嵌的双引号
# 匹配: "positioning":"...中间可能有"引号...": 格式
# 替换策略：把所有双引号替换为 \" 转义

# 方法：定位 "positioning":"....": 模式，提取内容，替换内部引号
def fix_positioning(m):
    prefix = m.group(1)  # "positioning":"
    value = m.group(2)    # 实际内容
    # 把内部的双引号（不在开头或结尾的）转义
    # 先把两端的引号去掉
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1]
    else:
        inner = value
    # 把内部的双引号转义
    inner_escaped = inner.replace('"', '\\"')
    return prefix + '"' + inner_escaped + '":'

# 匹配 "positioning":"...内容...",

# 实际上更简单：找到 "positioning":" 开头到下一个 ", 结尾的内容
# 但这样可能跨行，不好处理
# 简单方案：找到所有带 positioning 的行，逐行处理

lines = content.split('\n')
fixed_lines = []
for line in lines:
    if '"positioning"' in line:
        # 找到第一个 "positioning":" 后面的内容到倒数第二个 "（因为行尾是 "} 或 ",）
        # 提取冒号后面的字符串部分
        idx = line.index('"positioning":"') + len('"positioning":"')
        rest = line[idx:]
        # rest 格式: 内容... (结尾是 "} 或 ",)
        # 找到最后一个 " 在前面部分
        # 实际上，rest 以 "} 或 ", 结尾
        # 提取真正的文本内容（去掉开头的引号和结尾的 "} 或 ",）
        # 找第一个 " 后面到倒数第二个 " 之前
        # 这个方法太复杂，直接用正则

        # 策略：把内容中除了行尾的 ", 或 "} 之外的所有 " 转义
        # 行末尾: "...",  或  "...}
        # 所以去掉末尾的 ", 或 "} 然后把其余 " 转义再加回去
        suffix_match = re.search(r'("+)\s*[,}?]$', rest)
        if suffix_match:
            suffix = suffix_match.group(0)
            inner = rest[:suffix_match.start()]
            # 转义 inner 中的所有双引号
            inner_fixed = inner.replace('"', '\\"')
            line = line[:idx] + inner_fixed + suffix
        else:
            # 直接转义所有内部引号
            line = line.replace('"', '\\"')
    fixed_lines.append(line)

fixed_content = '\n'.join(fixed_lines)

with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print('Done! Lines with positioning:', sum(1 for l in lines if '"positioning"' in l))
