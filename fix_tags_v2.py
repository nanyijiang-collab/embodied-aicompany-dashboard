#!/usr/bin/env python3
"""
修复 company.html 的两个问题：
1. companyTagsMap key 去掉英文括号后缀（如 '至简动力 (Simple)' → '至简动力'）
2. getCompanyInfo 的 tagInfo 查找改为 normName 标准化匹配
"""

import re, sys

with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"原始长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 修复1：统一 companyTagsMap key（去掉英文括号后缀）
# ═══════════════════════════════════════════════════════════════════
# 找声明（只有1个！之前错误地取了第2个引用位置）
decl = re.search(r'const\s+companyTagsMap\s*=\s*\{', c)
if not decl:
    print("ERROR: 未找到 companyTagsMap 声明"); sys.exit(1)
decl_pos = decl.start()
body_start = decl.end()

# 逐字符找 body 结束
depth = 1; i = body_start
while i < len(c) and depth > 0:
    if c[i] == '{': depth += 1
    elif c[i] == '}': depth -= 1
    i += 1
tags_end = i - 1
tags_body = c[body_start:tags_end]

# 提取所有 key（单引号）
keys = re.findall(r"'([^']+)'", tags_body)
print(f"companyTagsMap key 数: {len(keys)}")

def strip_paren(s):
    """去掉末尾的英文括号及空格"""
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

bad_keys = [(k, strip_paren(k)) for k in keys if strip_paren(k) != k]
print(f"带括号需修正: {len(bad_keys)} 个  样例: {bad_keys[:3]}")

new_tags_body = tags_body
for old_key, new_key in bad_keys:
    new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")

# 重组文件
c = c[:decl_pos] + 'const companyTagsMap = {' + new_tags_body + '}' + c[tags_end+1:]
print(f"修正 key 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 修复2：getCompanyInfo 的 tagInfo 查找改用 normName 标准化
# ═══════════════════════════════════════════════════════════════════
# 当前代码（带括号key）：
#   const tagInfo = companyTagsMap[name] || companyTagsMap[rankingInfo?.company];
# 改为（normName 标准化匹配）：
#   const tagEntry = Object.entries(companyTagsMap).find(([k]) => normName(k) === normN)?.[1];

old_tag_lookup = (
    "const tagInfo = companyTagsMap[name] || companyTagsMap[rankingInfo?.company];"
)
new_tag_lookup = (
    "const normN = normName(name);\n"
    "            const tagEntry = Object.entries(companyTagsMap).find(([k]) => normName(k) === normN)?.[1];"
)
if old_tag_lookup not in c:
    print("ERROR: 未找到 tagInfo 查找语句"); sys.exit(1)
c = c.replace(old_tag_lookup, new_tag_lookup, 1)

# 替换 brain/training/scene 中的 tagInfo 为 tagEntry
c = c.replace('tagInfo?.brain', 'tagEntry?.brain')
c = c.replace('tagInfo?.training', 'tagEntry?.training')
c = c.replace('tagInfo?.scene', 'tagEntry?.scene')
print(f"替换 tagInfo → tagEntry 后长度: {len(c)}")

# ═══════════════════════════════════════════════════════════════════
# 验证
# ═══════════════════════════════════════════════════════════════════
print("\n=== 验证 ===")
# 至简动力相关
keys_after = re.findall(r"'([^']+)'", c[c.find('const companyTagsMap'):c.find('const companyTagsMap')+10000])
zm_keys = [k for k in keys_after if '至简' in k]
zj_keys = [k for k in keys_after if '逐际' in k]
print(f"至简动力 TagsMap key: {zm_keys}")
print(f"逐际动力 TagsMap key: {zj_keys}")

has_norm = 'normName' in c
has_tag_entry = 'tagEntry' in c
has_old_tag = 'tagInfo' in c
print(f"有 normName: {has_norm}")
print(f"有 tagEntry: {has_tag_entry}")
print(f"tagInfo 残留: {has_old_tag}")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n最终长度: {len(c)}")
print("写入完成 ✓")