#!/usr/bin/env python3
"""最终清理 company.html 中的残留代码"""

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 去掉 fuzzy match 里残留的 stripEmoji/normName 定义
old1 = (
    "// 模糊匹配（支持 emoji 前缀和括号后缀）\n"
    "const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');\n"
    "for (const [key, info] of Object.entries(companies)) {\n"
    "    const normKey = stripEmoji(key);\n"
    "    const normName = stripEmoji(name);\n"
    "    if (normName === normKey || normName.includes(normKey) || normKey.includes(normName)) return info;\n"
    "}"
)
new1 = (
    "// 模糊匹配（支持 emoji 前缀和括号后缀）\n"
    "for (const [key, info] of Object.entries(companies)) {\n"
    "    const normKey = normName(key);\n"
    "    const nn = normName(name);\n"
    "    if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "}"
)
c2 = c.replace(old1, new1, 1)
print(f"fuzzy match 清理: {len(c2)-len(c):+d}")

# 2. 修正 tagEntry 里的 stripEmoji(k) -> normName(k)
old2 = "stripEmoji(k).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim() === normN"
new2 = "normName(k) === normN"
c3 = c2.replace(old2, new2)
print(f"tagEntry 修正: {len(c3)-len(c2):+d}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c3)
print("已写入")

# 验证
gi = c3.find('function getCompanyInfo(name)')
depth = 0; i = gi
while i < len(c3):
    if c3[i] == '{': depth += 1
    elif c3[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
func = c3[gi:i+1]
opens = func.count('{'); closes = func.count('}')
print(f"函数长度: {len(func)}, 括号配对: {opens}/{closes} {'OK' if opens==closes else 'ERROR'}")

lines = func.split('\n')
print("\n=== 关键行 ===")
for j, l in enumerate(lines):
    s = l.strip()
    if any(x in s for x in ['normName', 'stripEmoji', 'rankingInfo', 'tagEntry', 'brain:', 'training:', 'scene:']):
        print(f"  {j:3d}: {s[:90]}")
