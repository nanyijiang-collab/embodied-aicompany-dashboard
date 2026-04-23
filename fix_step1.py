# -*- coding: utf-8 -*-
"""修复crawler.py中的编码问题"""

import re

with open('scripts/crawler.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 找到并修复损坏的字符串 - 使用更宽泛的匹配
content = re.sub(r"'source': '[^']*'", lambda m: "'source': 'FIXED'" if 'source' in m.group() and len(m.group()) < 50 else m.group(), content)

# 替换整个crawl_qbitai和crawl_ithome函数中的source
content = content.replace("'source': 'FIXED'", "'source': 'QbitAI'")

# 查找并修复特定的模式
# 找两个连续出现FIXED的地方，那就是量子位和IT之家
count = content.count("'source': 'FIXED'")
print(f"Found {count} FIXED patterns")

with open('scripts/crawler.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1 done")
