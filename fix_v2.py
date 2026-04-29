#!/usr/bin/env python3
"""
一次性修复 company.html 详情页空白问题
1. companyTagsMap key 统一去掉英文括号后缀（与 rankingData 对齐）
2. getCompanyInfo 添加 normName 函数（兼容 emoji/括号）
3. fuzzy match 使用 normName
4. 添加 rankingData + companyTagsMap fallback
"""

import re

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"原始文件长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════
# 第一步：修复 companyTagsMap key
# 注意：找 `const companyTagsMap = {` 声明（只有1个），而不是所有引用
# ═══════════════════════════════════════════════════════════════
decl = re.search(r'const\s+companyTagsMap\s*=\s*\{', c)
if not decl:
    print("ERROR: 未找到 companyTagsMap 声明")
    exit(1)
decl_pos = decl.start()
print(f"companyTagsMap 声明位置: {decl_pos}")

# 逐字符解析 body
body_start = decl_pos + decl.end()
depth = 1; i = body_start
while i < len(c) and depth > 0:
    if c[i] == '{': depth += 1
    elif c[i] == '}': depth -= 1
    i += 1
tags_end = i - 1
tags_body = c[body_start:tags_end]

# 提取所有 key（支持单引号和双引号）
keys_sq = re.findall(r"'([^']+)'", tags_body)
keys_dq = re.findall(r'"([^"]+)"', tags_body)
all_keys = {k: None for k in keys_sq + keys_dq}
print(f"companyTagsMap key 数: {len(all_keys)}")

def strip_paren(s):
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

bad_keys = [(k, strip_paren(k)) for k in all_keys if strip_paren(k) != k]
print(f"需修正 key: {len(bad_keys)} 个")

new_tags_body = tags_body
for old_key, new_key in bad_keys:
    # 同时替换单引号和双引号形式
    new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")
    new_tags_body = new_tags_body.replace(f'"{old_key}":', f'"{new_key}":')

# 重组
c = c[:decl_pos] + 'const companyTagsMap = {' + new_tags_body + '}' + c[tags_end+1:]
print(f"替换 companyTagsMap 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════
# 第二步：getCompanyInfo 添加 normName
# ═══════════════════════════════════════════════════════════════
gi = c.find('function getCompanyInfo(name)')
if gi < 0:
    print("ERROR: 未找到 getCompanyInfo 函数"); exit(1)
print(f"getCompanyInfo 位置: {gi}")

old_head = (
    "function getCompanyInfo(name) {\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
new_head = (
    "function getCompanyInfo(name) {\n"
    "            // 名称标准化：去掉 emoji 和英文括号后缀\n"
    "            const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');\n"
    "            const normName = (s) => stripEmoji(s).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
if old_head not in c:
    print("ERROR: 未找到函数头匹配"); exit(1)
c = c.replace(old_head, new_head, 1)
print(f"插入 normName 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════
# 第三步：更新 fuzzy match
# ═══════════════════════════════════════════════════════════════
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
if old_fuzzy not in c:
    print("ERROR: 未找到 fuzzy match"); exit(1)
c = c.replace(old_fuzzy, new_fuzzy, 1)
print(f"更新 fuzzy match 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════
# 第四步：添加 rankingData + companyTagsMap fallback
# ═══════════════════════════════════════════════════════════════
old_end_marker = (
    "                if (nn === normKey || nn.includes(normKey) || normKey.includes(nn)) return info;\n"
    "            }\n"
    "        }"
)
new_end_with_fallback = (
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
    "                    founded: rankingInfo.founded || '待补充',\n"
    "                    headquarters: rankingInfo.headquarters || (rankingInfo.isOverseas ? '海外' : '待补充'),\n"
    "                    segment: rankingInfo.segment || 'n.a.',\n"
    "                    isOverseas: rankingInfo.isOverseas,\n"
    "                    valuation: rankingInfo.valuation,\n"
    "                    valuationCNY: rankingInfo.valuationCNY || 0,\n"
    "                    currency: rankingInfo.currency || '人民币',\n"
    "                    latest: rankingInfo.latest || '-',\n"
    "                    latest_en: rankingInfo.latest_en || '',\n"
    "                    date: rankingInfo.date || '',\n"
    "                    founders: [],\n"
    "                    investors: [],\n"
    "                    brain: tagEntry?.brain || '',\n"
    "                    training: tagEntry?.training || '',\n"
    "                    scene: tagEntry?.scene || '',\n"
    "                    milestones: [\n"
    "                        {date: rankingInfo.date || '-', event: `最新融资: ${rankingInfo.latest || '待补充'} (${rankingInfo.valuation || '估值待定'})`}\n"
    "                    ]\n"
    "                };\n"
    "            }\n"
    "            return null;\n"
    "        }"
)
if old_end_marker not in c:
    print("ERROR: 未找到函数结尾 marker"); exit(1)
c = c.replace(old_end_marker, new_end_with_fallback, 1)
print(f"添加 fallback 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════
# 验证
# ═══════════════════════════════════════════════════════════════
gi2 = c.find('function getCompanyInfo(name)')
depth = 0; i = gi2
while i < len(c):
    if c[i] == '{': depth += 1
    elif c[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
func = c[gi2:i+1]
opens = func.count('{'); closes = func.count('}')
ok = opens == closes
print(f"\n函数括号配对: {opens}/{closes} {'OK' if ok else 'ERROR'}")
if not ok:
    print("ERROR: 函数括号不配对！"); exit(1)

# 检查关键内容
has_norm = 'const normName' in func
has_rank = 'rankingInfo' in func
has_tag = 'tagEntry' in func
print(f"normName: {'YES' if has_norm else 'MISSING'}")
print(f"rankingInfo fallback: {'YES' if has_rank else 'MISSING'}")
print(f"tagEntry: {'YES' if has_tag else 'MISSING'}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n最终文件长度: {len(c)}")
print("company.html 已写入")