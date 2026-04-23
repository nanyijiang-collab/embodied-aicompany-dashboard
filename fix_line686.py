# -*- coding: utf-8 -*-
"""修复第686行的问题"""

with open('scripts/crawler.py', 'rb') as f:
    content = f.read()

# 找到损坏的行并修复
# 损坏的行: 'source': 'QbitAI'source_url': link,
# 正确的行: 'source': 'QbitAI',
#          'source_url': link,
content = content.replace(
    b"'source': 'QbitAI'source_url': link,",
    b"'source': 'QbitAI',\n                    'source_url': link,"
)

with open('scripts/crawler.py', 'wb') as f:
    f.write(content)

print('Fixed line 686')

# 验证
with open('scripts/crawler.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 686: {lines[685]}")
    print(f"Line 687: {lines[686]}")
