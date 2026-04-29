with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

funcs = re.findall(r'function\s+(\w+)\s*\(', c)
print('index.html functions:', funcs)

# 找链接构造
links = re.findall(r'company\.html\?', c)
print('company.html链接出现次数:', len(links))

# 看看链接是怎么拼的
idx = c.find('company.html')
print('链接上下文:')
print(c[idx-50:idx+150])

print('\nindex.html 有 rankingData:', 'rankingData' in c)
print('index.html 有 companyTagsMap:', 'companyTagsMap' in c)
print('index.html 有 companyNameMapEN:', 'companyNameMapEN' in c)

# 找renderRankingItem或类似的渲染函数
for f in funcs:
    if 'rank' in f.lower() or 'company' in f.lower() or 'card' in f.lower() or 'item' in f.lower():
        print('相关函数:', f)