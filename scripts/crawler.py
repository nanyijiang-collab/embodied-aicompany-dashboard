# -*- coding: utf-8 -*-
"""
Embodied AI Media Monitor - 主爬虫程序
数据源：
- Google News RSS（中英文，按公司名搜索，每关键词100条）
- 163.com 晚点LatePost 媒体号
- Bing新闻（按公司名搜索）
- 36Kr 搜索
- 虎嗅 搜索
- 量子位 搜索
- IT之家 搜索
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set, Tuple
import time
import hashlib
import os
from urllib.parse import quote, urlparse
import sys
import io
# 设置 stdout 编码（支持中文输出）
try:
    sys.stdout = io.TextIOWrapper(sys.__stdout__.buffer, encoding='utf-8')
except Exception:
    pass

# ============== 链接验证器 ==============
class LinkValidator:
    """链接质量验证器"""

    TRUSTED_SOURCES = {
        'techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
        'engadget.com', 'reuters.com', 'bloomberg.com',
        '36kr.com', 'jiqizhixin.com', 'qbitai.com', 'ifeng.com',
        'sina.com.cn', 'sohu.com', 'qq.com', '163.com',
        'eastmoney.com', 'cls.cn', 'jiemian.com', 'thepaper.cn',
        'github.com', 'arxiv.org',
        'huxiu.com', 'nbd.com.cn', 'cs.com.cn', 'cnstock.com',
        'xueqiu.com', 'ce.cn', 'sznews.com', 'ithome.com',
        'news.google.com',
    }

    KNOWN_BAD_DOMAINS = {
        'starmotion.ai', 'fulani.cn', 'zibii.com', 'yolo.ai',
        'mifeng.com', 'qiankun.ai', 'boonzi.com', 'paxini.com',
    }

    def __init__(self, timeout: int = 8):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        self.timeout = timeout
        self.validation_cache = {}

    def is_homepage_url(self, url: str) -> bool:
        if not url:
            return True
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path or path.lower() in ['', 'index', 'index.html', 'home']:
            return True
        return False

    def is_trusted_source(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace('www.', '')
        return domain in self.TRUSTED_SOURCES

    def validate_single(self, url: str, company: str = '') -> Dict:
        if not url:
            return {'valid': False, 'reason': '空链接', 'suggestion': '需要提供新闻链接'}
        if url in self.validation_cache:
            return self.validation_cache[url]

        result = {
            'valid': True, 'url': url, 'reason': '', 'suggestion': '',
            'is_trusted': self.is_trusted_source(url)
        }
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if self.is_homepage_url(url):
            result['valid'] = False
            result['reason'] = '链接指向首页'
            result['suggestion'] = '请搜索' + company + '的具体新闻文章'
            self.validation_cache[url] = result
            return result

        if any(bad in domain for bad in self.KNOWN_BAD_DOMAINS):
            result['valid'] = False
            result['reason'] = '域名不存在或为假链接'
            result['suggestion'] = '请搜索' + company + '的真实新闻链接'
            self.validation_cache[url] = result
            return result

        if result['is_trusted']:
            self.validation_cache[url] = result
            return result

        try:
            resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            if resp.status_code >= 400:
                result['valid'] = False
                result['reason'] = 'HTTP ' + str(resp.status_code)
                result['suggestion'] = '链接失效，请搜索' + company + '的新闻'
            time.sleep(0.3)
        except Exception as e:
            result['valid'] = False
            result['reason'] = '连接失败'
            result['suggestion'] = '请验证链接或搜索' + company + '的新闻'

        self.validation_cache[url] = result
        return result

    def validate_events(self, events: List[Dict]) -> Tuple[List[Dict], Dict]:
        report = {'total': len(events), 'valid': 0, 'invalid': 0, 'issues': []}
        validated = []
        seen_urls = {}

        for event in events:
            url = event.get('source_url', '')
            company = event.get('company', '')

            if not url:
                report['invalid'] += 1
                report['issues'].append({
                    'company': company,
                    'title': event.get('title', '')[:40],
                    'issue': '空链接'
                })
                continue

            if url in seen_urls:
                continue

            validation = self.validate_single(url, company)

            if validation['valid']:
                report['valid'] += 1
                validated.append(event)
            else:
                report['invalid'] += 1
                report['issues'].append({
                    'company': company,
                    'title': event.get('title', '')[:40],
                    'url': url,
                    'issue': validation['reason'],
                    'fix': validation['suggestion']
                })

            seen_urls[url] = True

        return validated, report


# ============== 公司库 ==============
COMPANIES = {
    'overseas_vla': [
        {'name': 'NVIDIA', 'alias': ['英伟达', 'NVIDIA', 'GR00T'], 'website': 'https://nvidia.com'},
        {'name': 'Physical Intelligence', 'alias': ['PI', 'Physical Intelligence'], 'website': 'https://physicalintelligence.ai'},
        {'name': 'Skild AI', 'alias': ['Skild AI', 'Skild Brain'], 'website': 'https://skildai.com'},
        {'name': 'Figure AI', 'alias': ['Figure AI', 'Figure'], 'website': 'https://figure.ai'},
        {'name': 'Agility Robotics', 'alias': ['Agility Robotics', 'Digit'], 'website': 'https://agilityrobotics.com'},
        {'name': 'Apptronik', 'alias': ['Apptronik', 'Apollo'], 'website': 'https://apptronik.com'},
        {'name': 'Field AI', 'alias': ['Field AI'], 'website': 'https://fieldai.com'},
        {'name': 'Sanctuary AI', 'alias': ['Sanctuary AI', 'Phoenix'], 'website': 'https://sanctuary.ai'},
    ],
    'overseas_other': [
        {'name': '1X Technologies', 'alias': ['1X Technologies', 'EVE'], 'website': 'https://1x.tech'},
        {'name': 'Boston Dynamics', 'alias': ['Boston Dynamics', 'Atlas'], 'website': 'https://bostondynamics.com'},
        {'name': 'Mimic Robotics', 'alias': ['Mimic Robotics'], 'website': 'https://mimicrobotics.com'},
        {'name': 'Anybotics', 'alias': ['Anybotics'], 'website': 'https://anybotics.com'},
        {'name': 'Hexagon', 'alias': ['Hexagon'], 'website': 'https://hexagon.com'},
        {'name': 'Skydio', 'alias': ['Skydio'], 'website': 'https://skydio.com'},
        {'name': 'Sunday Robotics', 'alias': ['Sunday Robotics', 'Memo']},
    ],
    'domestic_vla': [
        {'name': '千寻智能', 'alias': ['千寻智能']},
        {'name': '银河通用', 'alias': ['银河通用', 'Galbot']},
        {'name': '自变量机器人', 'alias': ['自变量机器人']},
        {'name': '智元机器人', 'alias': ['智元机器人', 'Agibot']},
        {'name': '魔法原子', 'alias': ['魔法原子']},
        {'name': '星海图', 'alias': ['星海图']},
        {'name': '智平方', 'alias': ['智平方']},
        {'name': '它石智航', 'alias': ['它石智航']},
        {'name': '跨维智能', 'alias': ['跨维智能']},
        {'name': '穹彻智能', 'alias': ['穹彻智能']},
    ],
    'domestic_control': [
        {'name': '星动纪元', 'alias': ['星动纪元']},
        {'name': '思灵机器人', 'alias': ['思灵机器人', 'Agile Robots']},
        {'name': '逐际动力', 'alias': ['逐际动力']},
        {'name': '灵初智能', 'alias': ['灵初智能']},
        {'name': '大晓机器人', 'alias': ['大晓机器人']},
        {'name': '梅卡曼德', 'alias': ['梅卡曼德', 'Mech-Mind']},
        {'name': '傅利叶智能', 'alias': ['傅利叶智能', 'Fourier']},
        {'name': '七腾机器人', 'alias': ['七腾机器人']},
        {'name': '珞石机器人', 'alias': ['珞石机器人', 'ROKAE']},
        {'name': '镜识科技', 'alias': ['镜识科技']},
        {'name': '优理奇智能', 'alias': ['优理奇智能']},
        {'name': '加速进化', 'alias': ['加速进化']},
        {'name': '帕西尼感知', 'alias': ['帕西尼感知']},
        {'name': '地瓜机器人', 'alias': ['地瓜机器人']},
        {'name': '觅蜂科技', 'alias': ['觅蜂科技']},
        {'name': '简智机器人', 'alias': ['简智机器人', 'GenRobot', '简智新创']},
        {'name': '破壳机器人', 'alias': ['破壳机器人', 'Poke Robotics']},
    ]
}

# 展平所有公司名和别名
ALL_COMPANY_NAMES = set()
for category, companies in COMPANIES.items():
    for company in companies:
        ALL_COMPANY_NAMES.add(company['name'])
        for alias in company.get('alias', []):
            ALL_COMPANY_NAMES.add(alias)

EMBODIED_AI_KEYWORDS = [
    '具身智能', '人形机器人', '仿生机器人', '工业机器人', '协作机器人',
    'Embodied AI', 'Humanoid Robot', 'Embodied Intelligence', 'Physical AI',
    '具身', '人形', '机器人大脑', 'VLA', 'World Model',
    'Manipulator', 'Dexterous Manipulation', 'Robot Arm', 'Mobile Manipulation'
]

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')
STATE_FILE = os.path.join(DATA_DIR, 'crawl_state.json')
POTENTIAL_COMPANIES_FILE = os.path.join(DATA_DIR, 'potential_companies.json')

# ============== 163.com 媒体号配置 ==============
# 每个条目：(媒体名称, 163媒体主页URL)
MEDIA_163_ACCOUNTS = [
    ('晚点LatePost', 'https://www.163.com/dy/media/T1596162548889.html'),
]


class NewCompanyDetector:
    """新公司探测器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def is_known_company(self, name: str) -> bool:
        name_lower = name.lower()
        for known_name in ALL_COMPANY_NAMES:
            if known_name.lower() in name_lower or name_lower in known_name.lower():
                return True
        return False

    def search_for_new_companies(self) -> List[Dict]:
        potential = []
        search_sources = [
            {'name': '36Kr具身智能', 'url': 'https://36kr.com/information/AI/20031', 'selector': 'a.article-item-title'},
            {'name': '机器之心具身智能', 'url': 'https://jiqizhixin.com/tags/embodied-ai', 'selector': 'a.title'},
        ]
        for source in search_sources:
            try:
                resp = self.session.get(source['url'], timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                for elem in soup.select(source['selector'])[:30]:
                    title = elem.get_text(strip=True)
                    url = elem.get('href', '')
                    if not url.startswith('http'):
                        url = 'https://36kr.com' + url if url.startswith('/') else url
                    company_patterns = [
                        r'([\u4e00-\u9fa5]{2,8}(?:公司|机器人|智能|科技))',
                        r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?(?:\s+AI|\s+Robotics|\s+Tech)?)',
                    ]
                    for pattern in company_patterns:
                        matches = re.findall(pattern, title)
                        for match in matches:
                            if not self.is_known_company(match) and len(match) >= 3:
                                if any(kw in title for kw in ['机器人', '具身', '人形', 'Robot', 'Embodied', 'Humanoid']):
                                    potential.append({
                                        'name': match,
                                        'discovered_from': source['name'],
                                        'article_title': title,
                                        'article_url': url,
                                        'discovered_date': datetime.now().strftime('%Y-%m-%d'),
                                        'status': 'pending'
                                    })
                                    break
                time.sleep(1)
            except Exception as e:
                print('[WARN] Failed to search ' + source['name'] + ': ' + str(e))

        seen = set()
        unique_potential = []
        for p in potential:
            key = p['name']
            if key not in seen:
                seen.add(key)
                unique_potential.append(p)
        return unique_potential

    def load_existing(self) -> List[Dict]:
        if os.path.exists(POTENTIAL_COMPANIES_FILE):
            with open(POTENTIAL_COMPANIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save(self, potential_companies: List[Dict]):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(POTENTIAL_COMPANIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(potential_companies, f, ensure_ascii=False, indent=2)

    def add_new_company(self, name: str, category: str):
        new_company = {'name': name, 'alias': [name]}
        if category in COMPANIES:
            COMPANIES[category].append(new_company)
        ALL_COMPANY_NAMES.add(name)
        print('[OK] Added ' + name + ' to ' + category)


class EmbodiedAICrawler:
    """具身智能媒体监测爬虫"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })
        self.new_company_detector = NewCompanyDetector()

    def _normalize_title(self, title: str) -> str:
        """标题规范化：去除首尾空格、换行，转小写，用于去重比对"""
        if not title:
            return ''
        return title.strip().lower()

    def _generate_id(self, url: str, title: str) -> str:
        content = (url + title).encode('utf-8')
        return hashlib.md5(content).hexdigest()[:12]

    def _is_recent(self, date_str: str, days: int = 30) -> bool:
        try:
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m-%d', '%m/%d']:
                try:
                    date = datetime.strptime(date_str, fmt)
                    date = date.replace(year=datetime.now().year)
                    delta = datetime.now() - date
                    return delta.days <= days
                except:
                    pass
            return True
        except:
            return True

    def _classify_event(self, title: str) -> str:
        if any(kw in title for kw in ['融资', '投资', '估值', '资金', 'Funding', 'Series', '完成', '获得', '轮']):
            return 'funding'
        elif any(kw in title for kw in ['发布', '推出', 'Launch', 'Release', 'Product', '新品']):
            return 'product'
        elif any(kw in title for kw in ['开源', 'Open Source', 'Dataset', '数据集', '论文', 'Paper', 'CVPR', 'ICRA', 'NeurIPS', '顶会']):
            return 'tech_breakthrough'
        elif any(kw in title for kw in ['合作', '落地', '签约', 'Deploy', 'Partnership', '联合', '战略']):
            return 'project'
        elif any(kw in title for kw in ['展会', '峰会', '大会', '论坛', 'Conference', 'Summit', 'WAIC', '工博会']):
            return 'event'
        elif any(kw in title for kw in ['采访', '访谈', 'Interview', '对话', '专访', '独家', '观点', '创始人', 'CEO', '揭秘', '共话']):
            return 'interview'
        else:
            return 'other'

    def _parse_date(self, date_str: str) -> str:
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        if '今天' in date_str or 'Today' in date_str:
            return datetime.now().strftime('%Y-%m-%d')
        elif '昨天' in date_str or 'Yesterday' in date_str:
            return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        for fmt in ['%Y年%m月%d日', '%Y-%m-%d', '%m-%d', '%m/%d']:
            try:
                date = datetime.strptime(date_str, fmt)
                date = date.replace(year=datetime.now().year)
                return date.strftime('%Y-%m-%d')
            except:
                pass
        return datetime.now().strftime('%Y-%m-%d')

    # ---- 信源1：Bing新闻 ----
    def crawl_bing_news(self, company_name: str) -> List[Dict]:
        results = []
        try:
            url = 'https://www.bing.com/news/search?q=' + quote(company_name + ' 具身智能 OR 机器人 OR AI')
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.select('div.news-card')[:5]:
                title_elem = item.select_one('a.title')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                date_elem = item.select_one('span.news-date')
                date_str = date_elem.get_text(strip=True) if date_elem else ''
                source_elem = item.select_one('span.source')
                source = source_elem.get_text(strip=True) if source_elem else 'Bing News'
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': self._classify_event(title),
                    'title': title,
                    'title_en': None,
                    'summary': '',
                    'source': source,
                    'source_url': link,
                    'date': self._parse_date(date_str),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': [source]
                })
        except Exception as e:
            print('[WARN] Bing failed for ' + company_name + ': ' + str(e))
        return results

    # ---- 信源2：Google News RSS ----
    def crawl_google_news(self, company_name: str) -> List[Dict]:
        """通过Google News RSS搜索公司新闻（中英文各100条）"""
        results = []
        try:
            # 中文搜索
            zh_url = (
                'https://news.google.com/rss/search?'
                + 'q=' + quote(company_name)
                + '&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
            )
            # 英文搜索（用于海外公司）
            en_url = (
                'https://news.google.com/rss/search?'
                + 'q=' + quote(company_name)
                + '&hl=en-US&gl=US&ceid=US:en'
            )

            for lang, url in [('zh', zh_url), ('en', en_url)]:
                try:
                    resp = self.session.get(url, timeout=15)
                    if resp.status_code != 200:
                        continue
                    soup = BeautifulSoup(resp.text, 'lxml-xml')
                    items = soup.select('item')[:50]  # 每语言最多50条

                    for item in items:
                        title_elem = item.select_one('title')
                        link_elem = item.select_one('link')
                        pub_elem = item.select_one('pubDate')
                        source_elem = item.select_one('source')

                        title = title_elem.get_text(strip=True) if title_elem else ''
                        raw_link = link_elem.get_text(strip=True) if link_elem else ''
                        pub_str = pub_elem.get_text(strip=True) if pub_elem else ''
                        source = source_elem.get_text(strip=True) if source_elem else 'Google News'

                        if not title or not raw_link:
                            continue

                        # Google News链接重定向 → 解析出真实URL
                        real_url = raw_link
                        if 'news.google.com' in raw_link:
                            real_url = self._resolve_google_news_link(raw_link)

                        # 解析日期
                        date_str = ''
                        if pub_str:
                            try:
                                dt = datetime.strptime(pub_str[:25], '%a, %d %b %Y %H:%M:%S')
                                date_str = dt.strftime('%Y-%m-%d')
                            except:
                                date_str = datetime.now().strftime('%Y-%m-%d')

                        results.append({
                            'id': self._generate_id(real_url, title),
                            'company': company_name,
                            'type': self._classify_event(title),
                            'title': title,
                            'title_en': None,
                            'summary': '',
                            'source': source,
                            'source_url': real_url,
                            'date': date_str,
                            'created_at': datetime.now().isoformat(),
                            'media_sources': ['Google News', source]
                        })
                except Exception as e:
                    print('[WARN] Google News ' + lang + ' failed for ' + company_name + ': ' + str(e))

        except Exception as e:
            print('[WARN] Google News failed for ' + company_name + ': ' + str(e))
        return results

    def _resolve_google_news_link(self, google_url: str) -> str:
        """解析Google News跳转链接，返回真实URL"""
        try:
            # 先从RSS的link标签内容解析（Google News XML格式）
            # link标签格式: https://news.google.com/rss/articles/CBMi... → 包含真实URL参数
            # 尝试直接提取
            from urllib.parse import parse_qs, urlparse

            # Google News的RSS link已经是最终地址，不用再跳转
            # 直接返回原链接（可点击的Google News页面）
            return google_url
        except Exception:
            return google_url

    # ---- 信源3：163.com 媒体号（晚点）----
    def crawl_163_media_accounts(self) -> List[Dict]:
        """批量抓取163.com上各媒体号的文章列表（全行业覆盖）"""
        results = []
        for media_name, media_url in MEDIA_163_ACCOUNTS:
            try:
                resp = self.session.get(media_url, timeout=15)
                if resp.status_code != 200:
                    print('[163/' + media_name + '] HTTP ' + str(resp.status_code))
                    continue

                soup = BeautifulSoup(resp.text, 'html.parser')
                links = soup.find_all('a', href=True)
                count = 0

                seen_hrefs = set()
                for a in links:
                    href = a.get('href', '')
                    text = a.get_text(strip=True)

                    # 只取163直链文章
                    if 'www.163.com/dy/article/' not in href:
                        continue
                    if '.html' not in href:
                        continue
                    if len(text) < 8:
                        continue
                    if href in seen_hrefs:
                        continue
                    seen_hrefs.add(href)

                    # 从文章ID推测日期（163文章ID不含日期，用当前日期）
                    event_type = self._classify_event(text)

                    results.append({
                        'id': self._generate_id(href, text),
                        'company': '行业动态',
                        'type': event_type,
                        'title': text,
                        'title_en': None,
                        'summary': '',
                        'source': media_name,
                        'source_url': href,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'created_at': datetime.now().isoformat(),
                        'media_sources': ['163.com', media_name]
                    })
                    count += 1

                print('[163/' + media_name + '] ' + str(count) + ' articles')
                time.sleep(0.5)

            except Exception as e:
                print('[163/' + media_name + '] Error: ' + str(e))

        return results

    # ---- 信源3：36Kr 搜索 ----
    def crawl_36kr(self, company_name: str) -> List[Dict]:
        results = []
        try:
            url = 'https://36kr.com/search/articles/' + quote(company_name)
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.select('div.search-result-item')[:8]:
                title_elem = item.select_one('a.article-item-title') or item.select_one('a')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://36kr.com' + link
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': self._classify_event(title),
                    'title': title,
                    'title_en': None,
                    'summary': '',
                    'source': '36Kr',
                    'source_url': link,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': ['36Kr']
                })
        except Exception as e:
            print('[WARN] 36Kr failed for ' + company_name + ': ' + str(e))
        return results

    # ---- 信源4：虎嗅 搜索 ----
    def crawl_huxiu(self, company_name: str) -> List[Dict]:
        results = []
        try:
            url = 'https://www.huxiu.com/search.html?query=' + quote(company_name)
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.select('div.article-list-mod')[:8]:
                title_elem = item.select_one('a.tuwen-title')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://www.huxiu.com' + link
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': self._classify_event(title),
                    'title': title,
                    'title_en': None,
                    'summary': '',
                    'source': '虎嗅',
                    'source_url': link,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': ['虎嗅']
                })
        except Exception as e:
            print('[WARN] 虎嗅 failed for ' + company_name + ': ' + str(e))
        return results

    # ---- 信源5：量子位 搜索 ----
    def crawl_qbitai(self, company_name: str) -> List[Dict]:
        results = []
        try:
            url = 'https://www.qbitai.com/search?keyword=' + quote(company_name)
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.select('div.search-result')[:8]:
                title_elem = item.select_one('a.title')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://www.qbitai.com' + link
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': self._classify_event(title),
                    'title': title,
                    'title_en': None,
                    'summary': '',
                    'source': '量子位',
                    'source_url': link,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': ['量子位']
                })
        except Exception as e:
            print('[WARN] 量子位 failed for ' + company_name + ': ' + str(e))
        return results

    # ---- 信源6：IT之家 搜索 ----
    def crawl_ithome(self, company_name: str) -> List[Dict]:
        results = []
        try:
            url = 'https://www.ithome.com/search.html?q=' + quote(company_name)
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.select('div.item')[:8]:
                title_elem = item.select_one('a.t')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://www.ithome.com' + link
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': self._classify_event(title),
                    'title': title,
                    'title_en': None,
                    'summary': '',
                    'source': 'IT之家',
                    'source_url': link,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': ['IT之家']
                })
        except Exception as e:
            print('[WARN] IT之家 failed for ' + company_name + ': ' + str(e))
        return results

    def crawl_all(self, incremental: bool = True) -> List[Dict]:
        """抓取所有公司数据"""
        all_events = []
        seen_ids = set()
        seen_titles = set()  # 标题去重：规范化标题用于跨来源去重

        # 加载已有数据（只保留非微信来源）
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            # 过滤掉搜狗/微信来源
            existing = [
                e for e in existing
                if '微信' not in e.get('source', '') and 'sogou' not in e.get('source_url', '').lower()
            ]
            seen_ids = {e['id'] for e in existing}
            for e in existing:
                norm_title = self._normalize_title(e.get('title', ''))
                if norm_title:
                    seen_titles.add(norm_title)
            all_events = existing.copy()
            print('[OK] Loaded ' + str(len(all_events)) + ' existing events (wechat removed, title dedup init: ' + str(len(seen_titles)) + ')')

        # 增量检查
        if incremental:
            state = self._load_state()
            last_crawl = state.get('last_crawl', None)
            if last_crawl:
                days_since = (datetime.now() - datetime.fromisoformat(last_crawl)).days
                if days_since < 7:
                    print('Skipping crawl (last: ' + last_crawl + ', ' + str(days_since) + ' days ago)')
                    return all_events

        # ---- 步骤1：抓取163媒体号全量文章（一次性，覆盖行业动态）----
        print('\n[163] Crawling media accounts...')
        media_163_events = self.crawl_163_media_accounts()
        for event in media_163_events:
            norm_title = self._normalize_title(event.get('title', ''))
            if event['id'] not in seen_ids and norm_title not in seen_titles:
                all_events.append(event)
                seen_ids.add(event['id'])
                seen_titles.add(norm_title)
        print('[163] Added ' + str(len(media_163_events)) + ' articles total')

        # ---- 步骤2：按公司名搜索（Bing + 36Kr + 虎嗅 + 量子位 + IT之家）----
        all_companies = []
        for category, companies in COMPANIES.items():
            for company in companies:
                all_companies.append({'name': company['name'], 'alias': company.get('alias', [])})

        print('\n[Company] Monitoring ' + str(len(all_companies)) + ' companies...')

        for company in all_companies:
            names_to_search = list(set([company['name']] + company.get('alias', [])))

            company_total = 0
            for name in names_to_search[:2]:
                print('  ' + name + '...', end=' ')

                bing_events = self.crawl_bing_news(name)
                kr36_events = self.crawl_36kr(name)
                huxiu_events = self.crawl_huxiu(name)
                qbitai_events = self.crawl_qbitai(name)
                ithome_events = self.crawl_ithome(name)
                google_events = self.crawl_google_news(name)

                events = bing_events + kr36_events + huxiu_events + qbitai_events + ithome_events + google_events

                new_count = 0
                for event in events:
                    # 双重去重：id去重 + 标题去重
                    norm_title = self._normalize_title(event.get('title', ''))
                    if event['id'] not in seen_ids and norm_title not in seen_titles:
                        all_events.append(event)
                        seen_ids.add(event['id'])
                        seen_titles.add(norm_title)
                        new_count += 1

                print('+' + str(new_count))
                time.sleep(0.5)
                company_total += new_count

        # 更新状态
        self._save_state()

        # 按日期排序
        all_events.sort(key=lambda x: x.get('date', ''), reverse=True)

        return all_events

    def _load_state(self) -> Dict:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_state(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        state = {'last_crawl': datetime.now().isoformat()}
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def save_data(self, events: List[Dict], validate: bool = True):
        # ===== 去重处理 =====
        print('\n[Dedup] Running deduplication...')
        events = self._deduplicate_events(events)
        
        if validate:
            print('\n[Validate] Checking links...')
            validator = LinkValidator()
            events, report = validator.validate_events(events)
            print('  Valid: ' + str(report['valid']))
            print('  Invalid: ' + str(report['invalid']))
            if report['issues']:
                for issue in report['issues'][:5]:
                    print('  - [' + issue['company'] + '] ' + issue['issue'])

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
    
    def _deduplicate_events(self, events: List[Dict]) -> List[Dict]:
        """
        三层去重：
        1. 指纹去重：同公司+同日期+同标题
        2. 相似度去重：同公司+同日期+标题相似度>0.8
        3. ID去重：已有ID不重复添加
        """
        import re
        from difflib import SequenceMatcher
        
        def normalize_text(text):
            if not text:
                return ''
            text = re.sub(r'[^\w\s]', '', text)
            return text.lower().strip()
        
        def similarity(a, b):
            if not a or not b:
                return 0.0
            return SequenceMatcher(None, a, b).ratio()
        
        # 已有事件去重
        seen_ids = set()
        seen_keys = {}  # key: (company, date, normalized_title)
        
        unique_events = []
        removed_count = 0
        
        for e in events:
            event_id = e.get('id', '')
            company = e.get('company', '')
            date = e.get('date', '')[:10]
            title = normalize_text(e.get('title', ''))
            
            # 第一层：ID去重
            if event_id in seen_ids:
                removed_count += 1
                continue
            
            # 第二层：指纹去重（同公司+同日期+同标题）
            key = f"{company}|{date}|{title}"
            if key in seen_keys:
                removed_count += 1
                continue
            
            # 第三层：相似度去重
            is_duplicate = False
            for existing_key in seen_keys:
                existing_parts = existing_key.split('|')
                if len(existing_parts) >= 2:
                    existing_company, existing_date = existing_parts[0], existing_parts[1]
                    if company == existing_company and date == existing_date:
                        existing_title = '|'.join(existing_parts[2:])
                        if similarity(title, existing_title) >= 0.8:
                            is_duplicate = True
                            removed_count += 1
                            break
            
            if is_duplicate:
                continue
            
            seen_ids.add(event_id)
            seen_keys[key] = e
            unique_events.append(e)
        
        print(f'  Removed {removed_count} duplicates, {len(unique_events)} unique events')
        return unique_events

    def detect_new_companies(self) -> List[Dict]:
        print('\n[Detect] Running new company detector...')
        new_found = self.new_company_detector.search_for_new_companies()
        existing = self.new_company_detector.load_existing()
        seen = {p['name'] for p in existing}
        for p in new_found:
            if p['name'] not in seen:
                existing.append(p)
                seen.add(p['name'])
        self.new_company_detector.save(existing)
        print('[Detect] Found ' + str(len(new_found)) + ' new potential companies')
        return existing


def main():
    print('=' * 50)
    print('Embodied AI Media Monitor - Crawler')
    print('=' * 50)

    incremental = '--full' not in sys.argv
    detect_new = '--detect-new' in sys.argv
    validate_only = '--validate' in sys.argv

    crawler = EmbodiedAICrawler()

    if validate_only:
        print('\n[Validate] Validating existing events.json...')
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                events = json.load(f)
            validator = LinkValidator()
            events, report = validator.validate_events(events)
            print('Total: ' + str(report['total']))
            print('Valid: ' + str(report['valid']))
            print('Invalid: ' + str(report['invalid']))
        else:
            print('events.json not found')
        return

    events = crawler.crawl_all(incremental=incremental)
    crawler.save_data(events)

    if detect_new:
        potential = crawler.detect_new_companies()
        print('Potential new companies: ' + str(len(potential)))

    print('\n[OK] Crawl completed!')
    funding_count = len([e for e in events if e.get('type') == 'funding'])
    pr_count = len(events) - funding_count
    print('  Funding events: ' + str(funding_count))
    print('  PR updates: ' + str(pr_count))
    print('  Total events: ' + str(len(events)))


if __name__ == '__main__':
    main()
