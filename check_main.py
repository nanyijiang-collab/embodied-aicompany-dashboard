import subprocess
import re

# 获取origin/main版本
result = subprocess.run(
    ['git', 'show', 'origin/main:company.html'],
    capture_output=True, text=True, encoding='utf-8',
    cwd='c:/Users/ZhuanZ/WorkBuddy/20260422102414'
)
c = result.stdout
print(f"文件长度: {len(c)}")

gi = c.find('function getCompanyInfo(name)')
print(f"getCompanyInfo位置: {gi}")

# 找函数结尾 - 找紧跟函数体的}}
# 先找到 companies = { 对象的结束
companies_start = c.find('const companies = {', gi)
# 找 companies 对象结束
depth=0; i=companies_start
while i < len(c):
    if c[i]=='{': depth+=1
    elif c[i]=='}':
        depth-=1
        if depth==0: break
    i+=1
companies_end = i
print(f"companies对象: {companies_start} - {companies_end}")
print(f"companies后100字符: {repr(c[companies_end:companies_end+100])}")

# 找整个函数结尾
# getCompanyInfo函数在 <script> 标签里，找下一个函数定义前的那一层}
# 或者找所有连续的 }
func_end_candidates = []
depth=0; i=gi
while i < len(c) and i < gi + 30000:
    if c[i]=='{': depth+=1
    elif c[i]=='}':
        depth-=1
        if depth==0:
            func_end_candidates.append(i)
            break
    i+=1
print(f"函数结束位置: {func_end_candidates}")
if func_end_candidates:
    print('最后200字符:')
    print(repr(c[func_end_candidates[0]-100:func_end_candidates[0]+50]))
    func = c[gi:func_end_candidates[0]+1]
    lines = func.split('\n')
    print(f'\ngetCompanyInfo总行数: {len(lines)}')
    print('最后30行:')
    for j,l in enumerate(lines[-30:], len(lines)-29):
        print(f'{j:3d}: {l[:100]}')
