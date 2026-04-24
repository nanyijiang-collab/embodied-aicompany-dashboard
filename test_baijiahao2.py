import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 试试百家号RSS
rss_urls = [
    'https://baijiahao.baidu.com/feed/feed?app_id=1594065641659845',
    'https://baijiahao.baidu.com/feed/feed?author_id=123456',
]

# 试试通过百度搜索百家号文章
# 用搜狗搜索百家号
search_url = 'https://www.sogou.com/web?query=' + quote('具身智能 site:baijiahao.baidu.com') + '&num=10'
resp = requests.get(search_url, headers=headers, timeout=15)
print('Sogou search status:', resp.status_code)
print('URL:', resp.url)

soup = BeautifulSoup(resp.text, 'html.parser')
results = soup.select('div.vrwrap')
print('Results found:', len(results))

for r in results[:5]:
    title = r.select_one('h3 a') or r.select_one('a')
    if title:
        link = title.get('href', '')
        print(' -', title.get_text(strip=True)[:50])
        print('  ', link[:80])
