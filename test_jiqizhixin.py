import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 测试机器之心官网
url = 'https://www.jiqizhixin.com/articles'
resp = requests.get(url, headers=headers, timeout=15)
print('jiqizhixin.com status:', resp.status_code, 'chars:', len(resp.text))
soup = BeautifulSoup(resp.text, 'html.parser')
arts = [a for a in soup.find_all('a', href=True) if '/articles/' in a.get('href', '')]
print('Article links:', len(arts))
for a in arts[:5]:
    href = a.get('href', '')
    if not href.startswith('http'):
        href = 'https://www.jiqizhixin.com' + href
    print(' -', a.get_text(strip=True)[:50], '->', href[:70])

print()

# 测试机器之心搜索页面
url2 = 'https://www.jiqizhixin.com/graph/technologies'
resp2 = requests.get(url2, headers=headers, timeout=15)
print('jiqizhixin tech status:', resp2.status_code, 'chars:', len(resp2.text))
