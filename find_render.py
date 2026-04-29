with open('company.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

rp = c.find('function renderCompanyPage')
print('renderCompanyPage位置:', rp)
# 找下一个函数
next_func = re.search(r'\n    function \w+\(', c[rp+10:])
if next_func:
    end = rp + 10 + next_func.start()
else:
    end = len(c)
print('函数结束位置:', end)
print('函数长度:', end - rp)
print()
print(c[rp:end])