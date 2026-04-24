import requests
from bs4 import BeautifulSoup
import re


def crawl_163_wandian() -> list:
    """抓取163.com晚点LatePost文章列表"""
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    source_urls = [
        ('晚点LatePost', 'https://www.163.com/dy/media/T1596162548889.html'),
        ('甲子光年', 'https://www.163.com/dy/media/T1598948703880.html'),
        ('机器之心', 'https://www.163.com/dy/media/T1596150294884.html'),
    ]

    for source_name, url in source_urls:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print('[' + source_name + '] HTTP ' + str(resp.status_code))
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', href=True)
            count = 0

            for a in links:
                href = a.get('href', '')
                text = a.get_text(strip=True)

                # 只抓163.com直链文章
                if 'www.163.com/dy/article/' not in href:
                    continue
                if '.html' not in href:
                    continue
                if len(text) < 10:
                    continue

                # 提取文章ID用于去重
                match = re.search(r'/article/([^.]+)', href)
                article_id = match.group(1) if match else href

                results.append({
                    'id': article_id,
                    'source_name': source_name,
                    'title': text,
                    'url': href,
                    'media': '163.com',
                    'media_account': source_name,
                })
                count += 1

            print('[' + source_name + '] Found ' + str(count) + ' articles')

        except Exception as e:
            print('[' + source_name + '] Error: ' + str(e))

    return results


if __name__ == '__main__':
    articles = crawl_163_wandian()
    print('\nTotal: ' + str(len(articles)) + ' articles')
    for a in articles[:10]:
        print('[' + a['media_account'] + '] ' + a['title'][:50])
        print('  -> ' + a['url'])
