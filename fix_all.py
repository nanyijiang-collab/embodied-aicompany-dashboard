#!/usr/bin/env python3
"""修复 company.html 中 companyTagsMap key 不一致 + getCompanyInfo fuzzy match 问题"""

import re, os

with open('company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. 提取 rankingData 所有 company 名称 ───────────────────────────
ranking_names = re.findall(r"\{\s*company:\s*['\"]([^'\"]+)['\"]", content)
ranking_set = set(ranking_names)
print(f"rankingData: {len(ranking_set)} 个公司名")

# ─── 2. 提取 companyTagsMap 的所有 key（逐字符解析，跳过大括号嵌套） ───
tags_start = content.find('const companyTagsMap = {')
tags_end = content.find('\n};', tags_start) + 2
tags_body = content[tags_start + len('const companyTagsMap = {'): tags_end]

# 找所有 'key': 前的 key
keys_raw = re.findall(r"'([^']+)':", tags_body)
print(f"companyTagsMap: {len(keys_raw)} 个 key")

# ─── 3. 分析不一致情况 ────────────────────────────────────────────────
def strip_en_paren(s):
    """去掉英文括号后缀"""
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

def strip_emoji(s):
    """去掉 emoji"""
    return re.sub(r'[\U00010000-\U0010ffff]', '', s).strip()

# 统计
bad_keys = []   # 带括号的 key（需要在 companyTagsMap 中重命名）
missing_from_ranking = []  # companyTagsMap 有但 rankingData 没有的公司

for key in keys_raw:
    base = strip_en_paren(key)
    has_paren = (key != base)
    in_rank = (base in ranking_set)
    if has_paren:
        bad_keys.append((key, base))
    if not in_rank:
        missing_from_ranking.append(key)

print(f"\n=== 带括号的 key ({len(bad_keys)} 个) ===")
for old, new in bad_keys:
    print(f"  '{old}' -> '{new}'")

print(f"\n=== companyTagsMap 有但 rankingData 没有 ({len(missing_from_ranking)} 个) ===")
for k in missing_from_ranking:
    print(f"  '{k}'")

# ─── 4. 替换 companyTagsMap 中带括号的 key ────────────────────────────
new_tags_body = tags_body
replaced_count = 0
for old_key, new_key in bad_keys:
    if f"'{old_key}':" in new_tags_body:
        new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")
        print(f"  ✓ '{old_key}' -> '{new_key}'")
        replaced_count += 1
    else:
        print(f"  ✗ 未找到: '{old_key}'")

print(f"\n共替换 {replaced_count} 处")

# ─── 5. 重新组装 company.html ─────────────────────────────────────────
new_content = content[:tags_start] + 'const companyTagsMap = {' + new_tags_body + content[tags_end:]

# ─── 6. 修复 getCompanyInfo fuzzy match（加 emoji 剥离） ───────────────
# 找到 fuzzy match 位置
fuzzy_start = new_content.find('// 模糊匹配\nfor (const [key, info]')
fuzzy_end = new_content.find('\n}', fuzzy_start) + 1

old_fuzzy = new_content[fuzzy_start:fuzzy_end]
print(f"\n原始 fuzzy match ({len(old_fuzzy)} chars):\n{old_fuzzy.strip()}")

new_fuzzy = """// 模糊匹配（支持 emoji 前缀和括号后缀）
const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');
for (const [key, info] of Object.entries(companies)) {
    const normKey = stripEmoji(key);
    const normName = stripEmoji(name);
    if (normName === normKey || normName.includes(normKey) || normKey.includes(normName)) return info;
}"""

new_content = new_content[:fuzzy_start] + new_fuzzy + new_content[fuzzy_end:]
print(f"\n新 fuzzy match:\n{new_fuzzy}")

# ─── 7. 验证 companyTagsMap ───────────────────────────────────────────
keys_after = re.findall(r"'([^']+)':", new_tags_body)
still_bad = [(k, strip_en_paren(k)) for k in keys_after if strip_en_paren(k) != k]
if still_bad:
    print(f"\n仍有 {len(still_bad)} 个不一致:")
    for k in still_bad:
        print(f"  '{k}'")
else:
    print("\n验证通过 ✓ 所有 key 均已统一")

# ─── 8. 写回文件 ──────────────────────────────────────────────────────
with open('company.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("已写入 company.html")

# ─── 9. 同步更新 companies.html 的 allCompanies ───────────────────────
with open('companies.html', 'r', encoding='utf-8') as f:
    chtml = f.read()

# 去掉 allCompanies 里各公司名称的英文括号后缀
for old_key, new_key in bad_keys:
    # 在 allCompanies 中，name 可能是 '{ name:"xxx", ... }'
    chtml = chtml.replace(f'name:"{old_key}"', f'name:"{new_key}"')

with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(chtml)
print(f"已同步更新 companies.html ({len(bad_keys)} 个 name 更新)")

print("\n全部完成！")
