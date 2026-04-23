# -*- coding: utf-8 -*-
"""修复第690行"""

with open('scripts/crawler.py', 'rb') as f:
    content = f.read()

# 查找并替换损坏的 media_sources 行
# 被截断的量子位编码
bad_bytes = b"'media_sources': ['\xe9\x96\xb2\xe5\xbf\x93\xe7\x93\x99\xe6\xb5\xa3?]"
good_bytes = b"'media_sources': ['QbitAI']"

if bad_bytes in content:
    content = content.replace(bad_bytes, good_bytes)
    print("Fixed line 690")
else:
    print("Pattern not found, trying alternate...")
    # 尝试另一种模式
    import re
    pattern = rb"'media_sources': \['[\x80-\xff]+\?"
    content = re.sub(pattern, b"'media_sources': ['QbitAI']", content)
    print("Fixed with regex")

with open('scripts/crawler.py', 'wb') as f:
    f.write(content)

# 验证
with open('scripts/crawler.py', 'rb') as f:
    lines = f.readlines()
    print(f"Line 690: {lines[689]}")
