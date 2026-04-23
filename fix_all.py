# -*- coding: utf-8 -*-
"""修复所有损坏的行"""

with open('scripts/crawler.py', 'rb') as f:
    content = f.read()

# 修复第690行 - media_sources: ['量子位?] -> ['QbitAI']
content = content.replace(
    b"'media_sources': ['\xe9\x87\x8f\xe5\xad\x90\xe4\xbd\x8d?]",
    b"'media_sources': ['QbitAI']"
)

# 检查其他可能损坏的 quantum bit AI 相关字符串
# 查找并替换所有包含 'xxx?' 格式的行
import re

# 匹配 ['量子?], ['IT之家?] 等模式
pattern = rb"\['[\x80-\xff]+'?\](?!\])"
matches = re.findall(pattern, content)
print(f"Found {len(matches)} damaged media_sources patterns")
for m in set(matches):
    print(f"  {m}")

# 简单替换所有 ['...?] 为 ['FIXED']
content = re.sub(rb"\['[\x80-\xff]+'?\](?!\])", b"['FIXED']", content)
content = content.replace(b"['FIXED']", b"['QbitAI']", 1)  # 第一个是量子位
content = content.replace(b"['FIXED']", b"['ITHOME']")  # 第二个是IT之家

with open('scripts/crawler.py', 'wb') as f:
    f.write(content)

print("Fixed!")
