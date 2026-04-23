# -*- coding: utf-8 -*-
"""修复crawler.py中的编码问题"""

# 读取原始文件
with open('scripts/crawler.py', 'rb') as f:
    content = f.read()

# 检查是否包含乱码
print("Checking for corrupted bytes...")
if b'\xe8\xaf\xbb\xe6\x95\x99\xe7\xbd\xae' in content:
    print("Found corrupted quantum bit AI text")
    content = content.replace(b'\xe8\xaf\xbb\xe6\x95\x99\xe7\xbd\xae', b'QbitAI')

if b'\xe5\x8d\x95\xe6\x95\x99\xe5\xae\xb6' in content:
    print("Found corrupted IT home text")
    content = content.replace(b'\xe5\x8d\x95\xe6\x95\x99\xe5\xae\xb6', b'ITHOME')

# 保存
with open('scripts/crawler.py', 'wb') as f:
    f.write(content)

print("Fixed!")
