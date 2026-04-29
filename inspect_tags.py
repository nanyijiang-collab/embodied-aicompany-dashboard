import subprocess

# 获取origin/main版本
result = subprocess.run(
    ['git', 'show', 'origin/main:company.html'],
    capture_output=True, text=True, encoding='utf-8',
    cwd='c:/Users/ZhuanZ/WorkBuddy/20260422102414'
)
c = result.stdout

import re

# companyTagsMap声明位置
decl = re.search(r'const\s+companyTagsMap\s*=\s*\{', c)
decl_pos = decl.start()
body_start = decl.end()
depth=1; i=body_start
while i < len(c) and depth > 0:
    if c[i]=='{': depth+=1
    elif c[i]=='}': depth-=1
    i+=1
tags_end = i-1
tags_body = c[body_start:tags_end]

keys = re.findall(r"'([^']+)'", tags_body)
print(f"companyTagsMap key总数: {len(keys)}")

# 至简动力 逐际动力 相关
for k in keys:
    if '至简' in k or '逐际' in k:
        print(f'  相关key: {repr(k)}')

# 打印带括号的key，看有没有至简和逐际
paren_keys = [k for k in keys if '(' in k]
print(f'\n带括号key: {len(paren_keys)} 个')
for k in paren_keys[:5]:
    print(f'  {repr(k)}')
print('  ...')
for k in paren_keys[-3:]:
    print(f'  {repr(k)}')

# 打印不带括号的key
no_paren = [k for k in keys if '(' not in k]
print(f'\n不带括号key: {len(no_paren)} 个')
for k in no_paren[:10]:
    print(f'  {repr(k)}')
print('  ...')
for k in no_paren[-5:]:
    print(f'  {repr(k)}')

# 验证：找 getCompanyInfo 里 fuzzy match 后的 rankingInfo 块
gi = c.find('function getCompanyInfo(name)')
fuzzy_end = c.find('rankingInfo', gi)
print(f'\n=== getCompanyInfo fuzzy match 后 rankingInfo 块 ===')
print(c[fuzzy_end:fuzzy_end+800])