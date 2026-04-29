#!/usr/bin/env python3
"""修复 companyTagsMap key 与 rankingData company 字段不一致的问题"""

import re

with open('company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 提取 rankingData 里所有 company 名称
ranking_companies = re.findall(r"\{\s*company:\s*['\"]([^'\"]+)['\"]", content)
ranking_set = set(ranking_companies)
print(f"rankingData: {len(ranking_set)} 个公司名")

# 2. 提取 companyTagsMap 所有 key（逐字符解析，跳过大括号嵌套）
tags_start = content.find('const companyTagsMap = {')
tags_end = content.find('\n};', tags_start) + 2
tags_body = content[tags_start + len('const companyTagsMap = {'): tags_end]

keys_raw = re.findall(r"'([^']+)':", tags_body)
print(f"companyTagsMap: {len(keys_raw)} 个 key")

# 3. 找不一致的
mismatches = []
for key in keys_raw:
    chinese = re.sub(r'\s*\([^)]*\)\s*$', '', key).strip()
    if key != chinese:
        in_rank = chinese in ranking_set
        mismatches.append((key, chinese, in_rank))

print(f"\n=== 不一致的 key ({len(mismatches)} 个) ===")
for old, new, ok in mismatches:
    tag = "✓" if ok else "✗"
    print(f"  {tag} '{old}' -> '{new}'")

# 4. 替换：直接在 tags_body 里替换
new_tags_body = tags_body
for old_key, new_key, _ in mismatches:
    # 匹配 'old_key': -> 'new_key':
    new_tags_body = new_tags_body.replace(
        f"'{old_key}':", f"'{new_key}':"
    )

# 5. 重新组装
new_content = content[:tags_start] + 'const companyTagsMap = {' + new_tags_body + content[tags_end:]

# 6. 验证
keys_new = re.findall(r"'([^']+)':", new_tags_body)
still_bad = [(k, re.sub(r'\s*\([^)]*\)\s*$','',k).strip()) for k in keys_new
             if re.sub(r'\s*\([^)]*\)\s*$','',k).strip() != k]
if still_bad:
    print(f"\n仍有 {len(still_bad)} 个不一致!")
    for k in still_bad:
        print(f"  '{k}'")
else:
    print("\n验证通过 ✓")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"已写入 company.html")
