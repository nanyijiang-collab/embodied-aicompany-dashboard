#!/usr/bin/env python3
"""完整修复 company.html: 统一 companyTagsMap key + 修复所有查找路径"""

import re

with open('company.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. 提取 rankingData ───────────────────────────────────────────────
ranking_names = re.findall(r"\{\s*company:\s*['\"]([^'\"]+)['\"]", content)
ranking_set = set(ranking_names)
print(f"rankingData: {len(ranking_set)} 个")

# ── 2. 解析 companyTagsMap（逐字符，跳过大括号嵌套）────────────────────
positions = [m.start() for m in re.finditer('companyTagsMap', content)]
second_pos = positions[1]
start = second_pos + len('const companyTagsMap = {')
depth = 1; i = start
while i < len(content) and depth > 0:
    depth += 1 if content[i] == '{' else -1 if content[i] == '}' else 0
    i += 1
end = i - 1
tags_body = content[start:end]
keys = re.findall(r"'([^']+)':", tags_body)
print(f"companyTagsMap: {len(keys)} 个 key")

def strip_paren(s):
    return re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

def strip_emoji(s):
    return re.sub(r'[\U00010000-\U0010ffff]', '', s).strip()

def normalize(s):
    return strip_paren(strip_emoji(s)).strip()

# ── 3. 检查哪些 key 在 rankingData 里找不到 ────────────────────────────
missed = [(k, normalize(k)) for k in keys if normalize(k) not in ranking_set]
print(f"\nrankingData 中找不到的 key ({len(missed)} 个):")
for old, norm in missed:
    print(f"  '{old}' -> normalize='{norm}'")

# ── 4. 对所有 companyTagsMap key 做括号后缀剥离，修正为纯中文名 ─────────
bad = [(k, strip_paren(k)) for k in keys if strip_paren(k) != k]
print(f"\n需修正 key ({len(bad)} 个):")
for o, n in bad:
    print(f"  '{o}' -> '{n}'")

new_tags_body = tags_body
for old_key, new_key in bad:
    new_tags_body = new_tags_body.replace(f"'{old_key}':", f"'{new_key}':")

# ── 5. 重新组装 company.html ───────────────────────────────────────────
new_content = (content[:second_pos] +
               'const companyTagsMap = {' + new_tags_body + '}' +
               content[end+1:])

# ── 6. 修复所有 companyTagsMap 查找路径，加入 normalize 函数 ───────────
# 6a. 找 fuzzy match 并替换
fm_start = new_content.find('// 模糊匹配')
fm_end = new_content.find('\n}', fm_start) + 1
old_fuzzy = new_content[fm_start:fm_end]
print(f"\nfuzzy match 原始 ({len(old_fuzzy)} chars)")

new_fuzzy = """// 模糊匹配（支持 emoji 前缀和括号后缀）
const stripEmoji = (s) => s.replace(/[\\u{10000}-\\u{10FFFF}]/gu, '');
const normName = (s) => stripEmoji(s).replace(/\\s*\\([^)]*\\)\\s*$/, '').trim();
for (const [key, info] of Object.entries(companies)) {
    const nk = normName(key), nn = normName(name);
    if (nn === nk || nn.includes(nk) || nk.includes(nn)) return info;
}"""
new_content = new_content[:fm_start] + new_fuzzy + new_content[fm_end:]

# 6b. 找 fallback 代码块里的 companyTagsMap 查找，加入 normalize
# 当前: companyTagsMap[name] || companyTagsMap[rankingInfo?.company]
# 改为: 先尝试精确，再用 normalize 遍历
fallback_start = new_content.find('// === Fallback: 用 rankingData 数据填充基础信息 ===')
if fallback_start == -1:
    fallback_start = new_content.find('// Fallback: 用 rankingData')
fallback_end = new_content.find('// === End Fallback', fallback_start)
print(f"\nfallback 块: [{fallback_start}, {fallback_end}]")
print(f"原始 fallback 片段:\n{new_content[fallback_start:fallback_start+400]}")

# 替换 tagInfo 查找
old_taglookup = "const tagInfo = companyTagsMap[name] || companyTagsMap[rankingInfo?.company];"
new_taglookup = """// 先精确匹配，再用 normalize 遍历兼容所有命名格式
const tagInfo = companyTagsMap[name] || companyTagsMap[rankingInfo?.company]
    || Object.entries(companyTagsMap).find(([k]) => normName(k) === normName(name))?.[1]
    || Object.entries(companyTagsMap).find(([k]) => normName(k) === normName(rankingInfo?.company ?? ''))?.[1];"""
new_content = new_content.replace(old_taglookup, new_taglookup)

# ── 7. 验证 ─────────────────────────────────────────────────────────────
keys_after = re.findall(r"'([^']+)':", new_tags_body)
still = [(k, strip_paren(k)) for k in keys_after if strip_paren(k) != k]
if still:
    print(f"\n仍不一致: {still}")
else:
    print("\n所有 companyTagsMap key 统一 ✓")

with open('company.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("company.html 已写入 ✓")
