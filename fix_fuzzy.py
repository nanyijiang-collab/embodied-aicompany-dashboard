#!/usr/bin/env python3
"""清理 fuzzy match 块里的残留 const"""

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 直接找第二个 stripEmoji 定义并删除
first = c.find('const stripEmoji')
second = c.find('const stripEmoji', first + 1)
print(f"第一个 const stripEmoji: {first}")
print(f"第二个 const stripEmoji: {second}")
print(f"第二个上下文: {repr(c[second-5:second+150])}")

# 删除第二个 stripEmoji 定义（从 const stripEmoji 开始到 for 循环前的换行）
# 找第二个 stripEmoji 开始
s2 = second
# 找紧跟的 for 循环
for_pos = c.find('for (const [key, info]', s2)
print(f"for 循环位置: {for_pos}")
print(f"for 前内容: {repr(c[s2:for_pos])}")

# 删除 stripEmoji 那行
old_block = c[s2-0:for_pos]
new_block = ''  # 删除那行
c2 = c.replace(old_block, new_block, 1)

# 同时去掉残留的 const normKey = stripEmoji(key) 和 const normName = stripEmoji(name)
old1 = '    const normKey = stripEmoji(key);\n    const normName = stripEmoji(name);'
new1 = '    const normKey = normName(key);\n    const nn = normName(name);'
c3 = c2.replace(old1, new1, 1)
print(f"删除 stripEmoji 行: {len(c3)-len(c2):+d}")
print(f"修正 normKey/normName: {len(c3)-len(c2):+d}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c3)

# 验证
gi = c3.find('function getCompanyInfo')
depth = 0; i = gi
while i < len(c3):
    if c3[i]=='{': depth+=1
    elif c3[i]=='}':
        depth-=1
        if depth==0: break
    i+=1
func = c3[gi:i+1]
opens = func.count('{'); closes = func.count('}')
print(f"括号: {opens}/{closes} {'OK ✓' if opens==closes else 'ERROR'}")

# fuzzy match 块
fm = func.find('模糊匹配')
print("fuzzy match 块:")
print(func[fm:fm+250])

# 检查是否还有 stripEmoji
remaining = [i for i in range(len(func)) if func[i:i+12] == 'stripEmoji']
print(f"剩余 stripEmoji 引用: {len(remaining)} 处")
if remaining:
    for i in remaining:
        print(f"  {repr(func[max(0,i-10):i+40])}")
