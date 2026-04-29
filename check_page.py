with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# 找至简动力和逐际动力的 rankingData 条目
# rankingData 数组在 const rankingData = [...] 里
rd_pos = c.find('const rankingData = [')
# 找这个数组的结束
depth=0; i=rd_pos; start=rd_pos+len('const rankingData = ')
while i < len(c):
    if c[i]=='[': depth+=1
    elif c[i]==']':
        depth-=1
        if depth==0: break
    i+=1
rd_body = c[start:i]

# 找至简动力
zm = re.search(r"company:\s*'([^']*至简[^']*)'", rd_body)
zj = re.search(r"company:\s*'([^']*逐际[^']*)'", rd_body)
print('至简动力:', zm.group() if zm else 'NOT FOUND')
print('逐际动力:', zj.group() if zj else 'NOT FOUND')

# 验证tagInfo查找逻辑
# 当前代码: companyTagsMap[name] || companyTagsMap[rankingInfo?.company]
# name='至简动力', rankingInfo.company='至简动力'
# 所以是 companyTagsMap['至简动力'] || companyTagsMap['至简动力']
# 这个key存在吗？

keys = re.findall(r"'([^']+)'", c[c.find('const companyTagsMap'):c.find('const companyTagsMap')+20000])
print('至简动力在TagsMap:', any('至简' in k for k in keys))
print('逐际动力在TagsMap:', any('逐际' in k for k in keys))
# 找带括号的key
paren = [k for k in keys if '(' in k]
print('带括号key数:', len(paren))
print('带括号样例:', paren[:5])

# 问题：至简动力和逐际动力 不在 companyTagsMap 里！
# 所以 tagInfo 是 undefined，但函数还是会返回数据（name, valuation等）
# 页面不应该完全空白，而是标签为空
# 再检查一下是否函数根本就没被调用

# 看看company页面的renderCompanyDetail函数
rc_pos = c.find('function renderCompanyDetail')
rc_body = c[rc_pos:rc_pos+2000]
print('\nrenderCompanyDetail前30行:')
for j,l in enumerate(rc_body.split('\n')[:30]):
    print(f'  {j:3d}: {l}')