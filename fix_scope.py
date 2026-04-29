#!/usr/bin/env python3
"""把 stripEmoji/normName 提升到函数顶部，并修正 fallback 代码"""

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 在函数头部插入 stripEmoji 和 normName
old_head = "function getCompanyInfo(name) {\n            // 公司完整信息库（可扩展）\n            const companies = {"
new_head = (
    "function getCompanyInfo(name) {\n"
    "            // 名称标准化函数（提升到函数级，供所有路径共用）\n"
    "            const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');\n"
    "            const normName = (s) => stripEmoji(s).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
new_c = c.replace(old_head, new_head, 1)
print(f"函数头部插入: +{len(new_c)-len(c)} chars")

# 2. 去掉 fuzzy match 里的重复 stripEmoji/normName 定义
old_fuzzy = (
    "// 模糊匹配（支持 emoji 前缀和括号后缀）\n"
    "const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');\n"
    "for (const [key, info] of Object.entries(companies)) {\n"
    "    const normKey = stripEmoji(key);\n"
    "    const normName = stripEmoji(name);\n"
    "    if (normName === normKey || normName.includes(normKey) || normKey.includes(normName)) return info;\n"
    "}"
)
new_fuzzy = (
    "// 模糊匹配（支持 emoji 前缀和括号后缀）\n"
    "for (const [key, info] of Object.entries(companies)) {\n"
    "    const normKey = normName(key);\n"
    "    const nn = normName(name);\n"
    "    if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "}"
)
new_c2 = new_c.replace(old_fuzzy, new_fuzzy, 1)
print(f"fuzzy match 修正: {len(new_c2)-len(new_c):+d} chars")

# 3. 修正 fallback 里的 normName 引用（改掉 stripEmoji 调用）
new_c3 = new_c2.replace(
    "const normN = stripEmoji(name).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();",
    "const normN = normName(name);"
)
new_c4 = new_c3.replace(
    "const rn = stripEmoji(item.company).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();",
    "const rn = normName(item.company);"
)
new_c5 = new_c4.replace(
    "const k = stripEmoji(k).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim() === normN",
    "const k = normName(k) === normN"
)
print(f"fallback normName 修正: {len(new_c5)-len(new_c4):+d} chars")

# 4. 验证函数结构
gi_pos = new_c5.find("function getCompanyInfo(name)")
depth = 0; i = gi_pos
while i < len(new_c5):
    if new_c5[i] == '{': depth += 1
    elif new_c5[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
func = new_c5[gi_pos:i+1]
opens = func.count('{'); closes = func.count('}')
print(f"\n函数括号配对: {opens} open / {closes} close {'✓' if opens==closes else '✗ ERROR'}")
print(f"函数长度: {len(func)} chars (原12007)")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(new_c5)
print("company.html 已写入 ✓")
