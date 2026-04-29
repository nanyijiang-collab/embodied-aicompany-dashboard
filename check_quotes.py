# -*- coding: utf-8 -*-
# 检查 companies.html 中是否还有未转义的双引号
with open('companies.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找所有 positioning 行的内容
import re
matches = re.findall(r'positioning:"([^"]*")', content)
for m in matches[:10]:
    print(repr(m))
