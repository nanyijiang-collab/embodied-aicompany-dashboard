#!/usr/bin/env python3
"""修复 company.html companyTagsMap key 不一致问题"""

import re

with open('company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找第2个 companyTagsMap（真正的数据块）
positions = [m.start() for m in re.finditer('companyTagsMap', content)]
print(f"companyTagsMap 出现 {len(positions)} 次")
second_pos = positions[1]

# 逐字符解析，找到匹配 } 结束
start = second_pos + len('const companyTagsMap = {')
depth = 1
i = start
while i < len(content) and depth > 0:
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
    i += 1
end = i - 1  # 指向 }
print(f"解析范围: [{start}, {end}], depth={depth}")
print(f"内容开头: {repr(content[start:start+80])}")
print(f"内容结尾: {repr(content[end-10:end+5])}")

tags_body = content[start:end]
keys = re.findall(r"'([^']+)':", tags_body)
print(f"提取到 {len(keys)} 个 key, 前5: {keys[:5]}")

# rankingData
ranking_names = re.findall(r"\{\s*company:\s*['\"]([^'\"]+)['\"]", content)
ranking_set = set(ranking_names)

def strip_paren(s):
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

def strip_emoji(s):
    return re.sub(r'[\U00010000-\U0010ffff]', '', s).strip()

bad = [(k, strip_paren(k)) for k in keys if strip_paren(k) != k]
print(f"\n带括号的 key ({len(bad)} 个):")
for old, new in bad:
    ok = "OK" if new in ranking_set else "MISS"
    print(f"  [{ok}] '{old}' -> '{new}'")

# 替换
new_tags_body = tags_body
for old_key, new_key in bad:
    new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")
    print(f"  已替换: '{old_key}' -> '{new_key}'")

# 重新组装
new_content = (content[:second_pos] +
               'const companyTagsMap = {' + new_tags_body + '}' +
               content[end+1:])

# 修复 fuzzy match
fm = new_content.find('// 模糊匹配\nfor (const [key, info]')
if fm == -1:
    fm = new_content.find('// 模糊匹配')
fe = new_content.find('\n}', fm) + 1
print(f"\nfuzzy match 位置: [{fm}, {fe}]")
print(f"原始: {repr(new_content[fm:fm+60])}")

new_fuzzy = """// 模糊匹配（支持 emoji 前缀和括号后缀）
const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');
for (const [key, info] of Object.entries(companies)) {
    const normKey = stripEmoji(key);
    const normName = stripEmoji(name);
    if (normName === normKey || normName.includes(normKey) || normKey.includes(normName)) return info;
}"""

new_content = new_content[:fm] + new_fuzzy + new_content[fe:]
print("fuzzy match 已更新")

# 验证
keys_after = re.findall(r"'([^']+)':", new_tags_body)
still = [(k, strip_paren(k)) for k in keys_after if strip_paren(k) != k]
if still:
    print(f"\n仍有 {len(still)} 个不一致:")
    for k in still: print(f"  '{k}'")
else:
    print("\n验证通过 ✓")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("company.html 已写入")
