#!/usr/bin/env python3
"""
修复 company.html 详情页标签丢失问题（两个bug）

Bug 1: companyTagsMap key 带有英文括号（如 '至简动力 (Simple)'），
        但 rankingData 和 URL 参数用的是纯中文 '至简动力'，
        导致 lookup 永远找不到。

Bug 2: 整个 getCompanyInfo 没有名称标准化函数，
        导致任何带 emoji 或括号的显示名都无法正确匹配。

修复方案：
1. companyTagsMap 所有带括号的 key 统一去掉括号后缀
2. getCompanyInfo 添加 normName 函数
3. tagInfo 查找改用 normName 标准化匹配
"""

import re, sys

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"原始长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 修复1：统一 companyTagsMap key
# ═══════════════════════════════════════════════════════════════════
decl = re.search(r'const\s+companyTagsMap\s*=\s*\{', c)
if not decl:
    print("ERROR: 未找到 companyTagsMap 声明"); sys.exit(1)
decl_pos = decl.start()
body_start = decl.end()

depth = 1; i = body_start
while i < len(c) and depth > 0:
    if c[i] == '{': depth += 1
    elif c[i] == '}': depth -= 1
    i += 1
tags_end = i - 1
tags_body = c[body_start:tags_end]

keys = re.findall(r"'([^']+)'", tags_body)
print(f"companyTagsMap key 数: {len(keys)}")

def strip_paren(s):
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

bad = [(k, strip_paren(k)) for k in keys if strip_paren(k) != k]
print(f"带括号需修正: {len(bad)} 个  样例: {bad[:3]}")

new_tags = tags_body
for ok, nk in bad:
    new_tags = new_tags.replace(f"'{ok}':", f"'{nk}':")

c = c[:decl_pos] + 'const companyTagsMap = {' + new_tags + '}' + c[tags_end+1:]
print(f"修正 key 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 修复2：在 getCompanyInfo 添加 normName，修正 tagInfo 查找
# ═══════════════════════════════════════════════════════════════════
# 2a. 在 companies 对象定义前插入 normName
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
    print("ERROR: 未找到函数头"); sys.exit(1)
c = c.replace(old_head, new_head, 1)
print(f"插入 normName 后长度: {len(c)}")

# 2b. 修正 fuzzy match（使用 normName）
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
    print("ERROR: 未找到 fuzzy match"); sys.exit(1)
c = c.replace(old_fuzzy, new_fuzzy, 1)
print(f"更新 fuzzy match 后长度: {len(c)}")

# 2c. 修正 rankingInfo 查找（使用 normName）
old_rank_find = "rankingData.find(item => item.company === name || item.company.includes(name))"
new_rank_find = (
    "rankingData.find(item => {\n"
    "                const rn = normName(item.company);\n"
    "                const nn = normName(name);\n"
    "                return rn === nn || nn.includes(rn) || rn.includes(nn);\n"
    "            })"
)
if old_rank_find not in c:
    print("ERROR: 未找到 rankingInfo 查找"); sys.exit(1)
c = c.replace(old_rank_find, new_rank_find, 1)
print(f"修正 rankingInfo 查找后长度: {len(c)}")

# 2d. 修正 tagInfo 查找（使用 normName + companyTagsMap key遍历）
old_tag = (
    "const tagInfo = companyTagsMap[name] || companyTagsMap[rankingInfo?.company];"
)
new_tag = (
    "const normN = normName(name);\n"
    "            const tagEntry = Object.entries(companyTagsMap).find(([k]) => normName(k) === normN)?.[1];"
)
if old_tag not in c:
    print("ERROR: 未找到 tagInfo 查找"); sys.exit(1)
c = c.replace(old_tag, new_tag, 1)

# 2e. 替换 brain/training/scene 中的 tagInfo → tagEntry
c = c.replace('tagInfo?.brain', 'tagEntry?.brain')
c = c.replace('tagInfo?.training', 'tagEntry?.training')
c = c.replace('tagInfo?.scene', 'tagEntry?.scene')
print(f"替换 tagInfo → tagEntry 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 验证
# ═══════════════════════════════════════════════════════════════════
print("\n=== 验证 ===")

# 1. companyTagsMap key 验证
keys_after = re.findall(
    r"'([^']+)'",
    c[c.find('const companyTagsMap = {'):c.find('const companyTagsMap = {')+10000]
)
zm = [k for k in keys_after if '至简' in k]
zj = [k for k in keys_after if '逐际' in k]
paren = [k for k in keys_after if '(' in k]
print(f"至简动力 TagsMap key: {zm}")
print(f"逐际动力 TagsMap key: {zj}")
print(f"剩余带括号key: {len(paren)} 个  样例: {paren[:3]}")

# 2. 函数完整性验证
gi = c.find('function getCompanyInfo(name)')
depth = 0; i = gi
while i < len(c):
    if c[i] == '{': depth += 1
    elif c[i] == '}':
        depth -= 1
        if depth == 0: break
    i += 1
func = c[gi:i+1]
print(f"函数括号配对: {func.count('{')}/{func.count('}')} {'OK' if func.count('{')==func.count('}') else 'ERROR'}")
print(f"有 normName: {'YES' if 'const normName' in func else 'NO'}")
print(f"有 tagEntry: {'YES' if 'tagEntry' in func else 'NO'}")
print(f"tagInfo 残留: {'YES' if 'tagInfo' in func else 'NO'}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n最终长度: {len(c)}")
print("✓ 写入完成")