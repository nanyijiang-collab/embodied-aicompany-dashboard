import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 甲子光年在百家号的页面
urls = [
    'https://baijiahao.baidu.com/u?app_id=1594065641659845',  # 甲子光年
    'https://mbd.baidu.com/homepage/joined',
]

for url in urls:
    resp = requests.get(url, headers=headers, timeout=10)
    print('URL:', url)
    print('Status:', resp.status_code)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.select_one('title')
        print('Title:', title.get_text(strip=True) if title else 'none')
        # 找文章链接
        links = soup.find_all('a', href=True)
        bj_links = [l for l in links if 'baijiahao' in l.get('href', '')]
        print('Baijiahao links:', len(bj_links))
        for l in bj_links[:3]:
            print(' -', l.get('href', '')[:80])
    print()
