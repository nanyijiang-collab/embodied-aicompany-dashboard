# -*- coding: utf-8 -*-
"""检查和修复损坏的字节"""

with open('scripts/crawler.py', 'rb') as f:
    content = f.read()

# 查找问题字符串 - 查找单引号开始，后面跟着非ASCII字符，然后是逗号的模式
import re

# 找所有 source': 'xxx' 的模式
pattern = rb"'source': '([^']*?)'"
matches = re.findall(pattern, content)

print("Found source patterns:")
for m in matches:
    print(f"  {m}")

# 检查是否有损坏的UTF-8
print("\nChecking for invalid UTF-8...")
try:
    content.decode('utf-8')
    print("File is valid UTF-8")
except UnicodeDecodeError as e:
    print(f"Invalid at position {e.start}")
