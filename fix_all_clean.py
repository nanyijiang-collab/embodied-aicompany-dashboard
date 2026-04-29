#!/usr/bin/env python3
"""
完整修复 company.html - 一次性正确处理所有问题

修复内容：
1. companyTagsMap key 统一去掉括号后缀（与 rankingData 对齐）
2. getCompanyInfo 添加名称标准化函数 normName
3. fuzzy match 使用 normName 兼容 emoji/括号
4. 添加 rankingData + companyTagsMap fallback（对不在 companies 对象的公司）
"""

import re

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"原始文件长度: {len(c)}")

# ══════════════════════════════════════════════════════════════
# 第一步：统一 companyTagsMap key
# ══════════════════════════════════════════════════════════════
# 找 companyTagsMap（第2个出现位置）
tags_positions = [m.start() for m in re.finditer('companyTagsMap', c)]
second_tags = tags_positions[1]
print(f"companyTagsMap 位置: {second_tags}")

# 逐字符解析，跳过大括号嵌套
body_start = second_tags + len('const companyTagsMap = {')
depth = 1; i = body_start
while i < len(c) and depth > 0:
    if c[i] == '{': depth += 1
    elif c[i] == '}': depth -= 1
    i += 1
tags_end = i - 1
tags_body = c[body_start:tags_end]

def strip_paren(s):
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

keys = re.findall(r"'([^']+)':", tags_body)
print(f"companyTagsMap key 数: {len(keys)}")

# 提取 rankingData 公司名
ranking_names = re.findall(r"\{\s*company:\s*['\"]([^'\"]+)['\"]", c)
ranking_set = set(ranking_names)

bad_keys = [(k, strip_paren(k)) for k in keys if strip_paren(k) != k]
print(f"需修正 key: {len(bad_keys)} 个")

# 替换 key
new_tags_body = tags_body
for old_key, new_key in bad_keys:
    new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")

# 重组文件（替换 companyTagsMap 部分）
part1 = c[:second_tags]
part2 = 'const companyTagsMap = {' + new_tags_body + '}'
part3 = c[tags_end+1:]
c = part1 + part2 + part3
print(f"替换 companyTagsMap 后长度: {len(c)}")

# ══════════════════════════════════════════════════════════════
# 第二步：给 getCompanyInfo 添加 normName 并修正 fuzzy match
# ══════════════════════════════════════════════════════════════
gi_pos = c.find('function getCompanyInfo(name)')
print(f"getCompanyInfo 位置: {gi_pos}")

# 在 companies 对象定义前插入 normName 函数
old_fn_head = (
    "function getCompanyInfo(name) {\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
new_fn_head = (
    "function getCompanyInfo(name) {\n"
    "            // 名称标准化：去掉 emoji 和英文括号后缀\n"
    "            const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');\n"
    "            const normName = (s) => stripEmoji(s).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
c = c.replace(old_fn_head, new_fn_head, 1)
print(f"插入 normName 后长度: {len(c)}")

# 找 fuzzy match 块并替换
old_fuzzy = (
    "// 模糊匹配\n"
    "            for (const [key, info] of Object.entries(companies)) {\n"
    "                if (name.includes(key) || key.includes(name)) return info;\n"
    "            }"
)
new_fuzzy = (
    "// 模糊匹配（支持 emoji 前缀和括号后缀）\n"
    "            for (const [key, info] of Object.entries(companies)) {\n"
    "                const normKey = normName(key);\n"
    "                const nn = normName(name);\n"
    "                if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "            }"
)
c = c.replace(old_fuzzy, new_fuzzy, 1)
print(f"更新 fuzzy match 后长度: {len(c)}")

# ══════════════════════════════════════════════════════════════
# 第三步：在 fuzzy match 后插入 rankingData + companyTagsMap fallback
# ══════════════════════════════════════════════════════════════
# 找 fuzzy match 结尾（最后的 `}` 和紧跟的函数结尾 `}`）
old_fuzzy_end = (
    "                if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "            }\n"
    "        }"
)
new_fuzzy_end = (
    "                if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "            }\n"
    "            // === Fallback: 对不在 companies 对象里的公司，从 rankingData + companyTagsMap 补数据 ===\n"
    "            const normN = normName(name);\n"
    "            const rankingInfo = rankingData.find(item => {\n"
    "                const rn = normName(item.company);\n"
    "                return rn === normN || normN.includes(rn) || rn.includes(normN);\n"
    "            });\n"
    "            if (rankingInfo) {\n"
    "                const tagEntry = Object.entries(companyTagsMap).find(([k]) => normName(k) === normN)?.[1];\n"
    "                return {\n"
    "                    name: rankingInfo.company,\n"
    "                    name_en: companyNameMapEN[rankingInfo.company] || '',\n"
    "                    website: '',\n"
    "                    founded: rankingInfo.founded,\n"
    "                    headquarters: rankingInfo.headquarters,\n"
    "                    segment: rankingInfo.segment,\n"
    "                    isOverseas: rankingInfo.isOverseas,\n"
    "                    valuation: rankingInfo.valuation,\n"
    "                    valuationCNY: 0,\n"
    "                    currency: rankingInfo.valuation.includes('美元') ? '美元' : '人民币',\n"
    "                    latest: '',\n"
    "                    date: '',\n"
    "                    brain: tagEntry?.brain || '',\n"
    "                    training: tagEntry?.training || '',\n"
    "                    scene: tagEntry?.scene || '',\n"
    "                    founders: [],\n"
    "                    investors: [],\n"
    "                    milestones: []\n"
    "                };\n"
    "            }\n"
    "        }"
)
c = c.replace(old_fuzzy_end, new_fuzzy_end, 1)
print(f"添加 fallback 后长度: {len(c)}")

# ══════════════════════════════════════════════════════════════
# 验证
# ══════════════════════════════════════════════════════════════
gi_pos2 = c.find('function getCompanyInfo(name)')
depth = 0; i = gi_pos2
while i < len(c):
    if c[i] == '{': depth += 1
    elif c[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
func = c[gi_pos2:i+1]
opens = func.count('{'); closes = func.count('}')
print(f"\n函数括号配对: {opens}/{closes} {'✓ OK' if opens==closes else '✗ ERROR'}")
print(f"函数长度: {len(func)} chars")

# 检查关键内容
print("\n=== 关键代码段 ===")
lines = func.split('\n')
for j, l in enumerate(lines):
    s = l.strip()
    if any(x in s for x in ['normName', 'rankingInfo', 'tagEntry', 'Fallback', 'brain:']):
        print(f"  {j:3d}: {s[:90]}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n最终文件长度: {len(c)}")
print("company.html 已写入 ✓")
