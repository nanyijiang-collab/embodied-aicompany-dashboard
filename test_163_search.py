import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 163搜索接口
keywords = ['具身智能', '人形机器人', '机器人融资', '机器之心 具身', '智元机器人', '宇树科技']

for kw in keywords:
    url = 'https://www.163.com/dy/search/' + quote(kw) + '.html'
    resp = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, 'html.parser')
    arts = [a for a in soup.find_all('a', href=True) if 'www.163.com/dy/article/' in a.get('href', '')]
    # 去重
    seen = set()
    unique = []
    for a in arts:
        href = a.get('href', '')
        if href not in seen:
            seen.add(href)
            unique.append(a)

    print('[' + kw + '] ' + str(len(unique)) + ' articles')
    for a in unique[:3]:
        print('  -', a.get_text(strip=True)[:50])
        print('    ', a.get('href', '')[:70])
    print()
