with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# 验证第一步：companyTagsMap 声明位置和 key
decl = re.search(r'const\s+companyTagsMap\s*=\s*\{', c)
decl_pos = decl.start()
body_start = decl.end()
depth = 1; i = body_start
while i < len(c) and depth > 0:
    if c[i] == '{': depth += 1
    elif c[i] == '}': depth -= 1
    i += 1
tags_end = i - 1
tags_body = c[body_start:tags_end]
keys_sq = re.findall(r"'([^']+)'", tags_body)
keys_dq = re.findall(r'"([^"]+)"', tags_body)
print(f"companyTagsMap key数: {len(keys_sq)}单引号 + {len(keys_dq)}双引号")
print(f"单引号样例: {keys_sq[:3]}")

# 验证第二步：函数头
old_head = (
    "function getCompanyInfo(name) {\n"
    "            // 公司完整信息库（可扩展）\n"
    "            const companies = {"
)
print(f"函数头匹配: {'YES' if old_head in c else 'NO'}")

# 验证第三步：fuzzy match
old_fuzzy = (
    "// 模糊匹配\n"
    "            for (const [key, info] of Object.entries(companies)) {\n"
    "                if (name.includes(key) || key.includes(name)) return info;\n"
    "            }"
)
print(f"fuzzy match匹配: {'YES' if old_fuzzy in c else 'NO'}")

# 验证第四步：函数结尾marker
# 现在的fuzzy match结束后是什么？
gi = c.find('function getCompanyInfo(name)')
depth=0; i=gi
while i < len(c):
    if c[i]=='{': depth+=1
    elif c[i]=='}':
        depth-=1
        if depth==0: break
    i+=1
lines = c[gi:i+1].split('\n')
print(f"getCompanyInfo总行数: {len(lines)}")
print("最后15行:")
for j,l in enumerate(lines[-15:], len(lines)-14):
    print(f"  {j:3d}: {repr(l)}")

# 检查rankingInfo是否已在函数中
print(f"函数内已有rankingInfo: {'YES' if 'rankingInfo' in c[gi:i+1] else 'NO'}")
print(f"函数内已有tagInfo: {'YES' if 'tagInfo' in c[gi:i+1] else 'NO'}")
print(f"函数内已有null返回: {'YES' if 'return null' in c[gi:i+1] else 'NO'}")