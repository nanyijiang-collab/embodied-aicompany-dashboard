# -*- coding: utf-8 -*-
"""
Embodied AI Media Monitor - 主爬虫程序
功能：抓取具身智能公司媒体动态
包含：
- 主爬虫类 EmbodiedAICrawler
- 新公司探测器 NewCompanyDetector  
- 链接验证器 LinkValidator（自动验证新闻链接质量）
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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============== 链接验证器 ==============
class LinkValidator:
    """链接质量验证器 - 防止假链接进入数据"""

    # 可信新闻源（验证通过率高）
    TRUSTED_SOURCES = {
        'techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
        'engadget.com', 'reuters.com', 'bloomberg.com',
        '36kr.com', 'jiqizhixin.com', 'qbitai.com', 'ifeng.com',
        'sina.com.cn', 'sohu.com', 'qq.com', '163.com',
        'eastmoney.com', 'cls.cn', 'jiemian.com', 'thepaper.cn',
        'github.com', 'arxiv.org',
    }

    # 已知假/无效域名
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
        """检测是否是首页链接"""
        if not url:
            return True
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        # 空路径或只有index.html等
        if not path or path.lower() in ['', 'index', 'index.html', 'home']:
            return True
        return False

    def is_trusted_source(self, url: str) -> bool:
        """检查是否是可信来源"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace('www.', '')
        return domain in self.TRUSTED_SOURCES

    def validate_single(self, url: str, company: str = '') -> Dict:
        """验证单个链接，返回验证结果"""
        if not url:
            return {'valid': False, 'reason': '空链接', 'suggestion': '需要提供新闻链接'}

        # 检查缓存
        if url in self.validation_cache:
            return self.validation_cache[url]

        result = {
            'valid': True,
            'url': url,
            'reason': '',
            'suggestion': '',
            'is_trusted': self.is_trusted_source(url)
        }

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # 1. 检查是否是首页
        if self.is_homepage_url(url):
            result['valid'] = False
            result['reason'] = '链接指向首页'
            result['suggestion'] = f'请搜索{company}的具体新闻文章'
            self.validation_cache[url] = result
            return result

        # 2. 检查已知假域名
        if any(bad in domain for bad in self.KNOWN_BAD_DOMAINS):
            result['valid'] = False
            result['reason'] = '域名不存在或为假链接'
            result['suggestion'] = f'请搜索{company}的真实新闻链接'
            self.validation_cache[url] = result
            return result

        # 3. 可信来源跳过HTTP验证
        if result['is_trusted']:
            self.validation_cache[url] = result
            return result

        # 4. HTTP验证
        try:
            resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            if resp.status_code >= 400:
                result['valid'] = False
                result['reason'] = f'HTTP {resp.status_code}'
                result['suggestion'] = f'链接失效，请搜索{company}的新闻'
            time.sleep(0.3)
        except Exception as e:
            result['valid'] = False
            result['reason'] = '连接失败'
            result['suggestion'] = f'请验证链接或搜索{company}的新闻'

        self.validation_cache[url] = result
        return result

    def validate_events(self, events: List[Dict]) -> Tuple[List[Dict], Dict]:
        """验证事件列表中的所有链接"""
        report = {'total': len(events), 'valid': 0, 'invalid': 0, 'issues': []}
        validated = []
        seen_urls = {}

        for event in events:
            url = event.get('source_url', '')
            company = event.get('company', '')

            # 跳过空链接
            if not url:
                report['invalid'] += 1
                report['issues'].append({
                    'company': company,
                    'title': event.get('title', '')[:40],
                    'issue': '空链接'
                })
                continue

            # 检测重复
            if url in seen_urls:
                continue  # 跳过重复

            # 验证
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
        {'name': 'Physical Intelligence', 'alias': ['PI', 'Physical Intelligence', 'π'], 'website': 'https://physicalintelligence.ai'},
        {'name': 'Skild AI', 'alias': ['Skild AI', 'Skild Brain'], 'website': 'https://skildai.com'},
        {'name': 'Figure AI', 'alias': ['Figure AI', 'Figure'], 'website': 'https://figure.ai'},
        {'name': 'Agility Robotics', 'alias': ['Agility', 'Digit'], 'website': 'https://agilityrobotics.com'},
        {'name': 'Apptronik', 'alias': ['Apptronik', 'Apollo'], 'website': 'https://apptronik.com'},
        {'name': 'Field AI', 'alias': ['Field AI'], 'website': 'https://fieldai.com'},
        {'name': 'Sanctuary AI', 'alias': ['Sanctuary AI', 'Phoenix'], 'website': 'https://sanctuary.ai'},
    ],
    'overseas_other': [
        {'name': '1X Technologies', 'alias': ['1X', 'EVE'], 'website': 'https://1x.tech'},
        {'name': 'Boston Dynamics', 'alias': ['Boston Dynamics', 'Atlas'], 'website': 'https://bostondynamics.com'},
        {'name': 'Mimic Robotics', 'alias': ['Mimic Robotics', 'Mimic'], 'website': 'https://mimicrobotics.com'},
        {'name': 'Anybotics', 'alias': ['Anybotics'], 'website': 'https://anybotics.com'},
        {'name': 'Hexagon', 'alias': ['Hexagon'], 'website': 'https://hexagon.com'},
        {'name': 'Skydio', 'alias': ['Skydio'], 'website': 'https://skydio.com'},
    ],
    'domestic_vla': [
        {'name': '千寻智能', 'alias': ['千寻智能', 'QIANKUN']},
        {'name': '银河通用', 'alias': ['银河通用']},
        {'name': '自变量机器人', 'alias': ['自变量机器人', 'Zibii']},
        {'name': '智元机器人', 'alias': ['智元机器人', 'Agibot']},
        {'name': '魔法原子', 'alias': ['魔法原子', 'MagicLab']},
        {'name': '星海图', 'alias': ['星海图', 'SeaStars']},
        {'name': '智平方', 'alias': ['智平方', 'RoboStep']},
        {'name': '它石智航', 'alias': ['它石智航']},
        {'name': '跨维智能', 'alias': ['跨维智能', 'DexVerse']},
        {'name': '穹彻智能', 'alias': ['穹彻智能', 'Noin Robotics']},
    ],
    'domestic_control': [
        {'name': '星动纪元', 'alias': ['星动纪元', 'StarMotion']},
        {'name': '思灵机器人', 'alias': ['思灵机器人', 'Agile Robots']},
        {'name': '逐际动力', 'alias': ['逐际动力', 'Zongqi']},
        {'name': '灵初智能', 'alias': ['灵初智能', 'Lingchu']},
        {'name': '大晓机器人', 'alias': ['大晓机器人', 'Daxiao']},
        {'name': '梅卡曼德', 'alias': ['梅卡曼德', 'Mech-Mind']},
        {'name': '傅利叶智能', 'alias': ['傅利叶智能', 'Fourier']},
        {'name': '七腾机器人', 'alias': ['七腾机器人', 'Qiteng']},
        {'name': '珞石机器人', 'alias': ['珞石机器人', 'ROKAE']},
        {'name': '镜识科技', 'alias': ['镜识科技', 'MirrorTech']},
        {'name': '优理奇智能', 'alias': ['优理奇智能', 'Yuliqi']},
        {'name': '加速进化', 'alias': ['加速进化', 'Boonz']},
        {'name': '帕西尼感知', 'alias': ['帕西尼感知', 'Paxini']},
        {'name': '地瓜机器人', 'alias': ['地瓜机器人', 'Yolo']},
        {'name': '觅蜂科技', 'alias': ['觅蜂科技', 'Mifeng']},
    ]
}

# 展平所有公司名和别名用于匹配
ALL_COMPANY_NAMES = set()
for category, companies in COMPANIES.items():
    for company in companies:
        ALL_COMPANY_NAMES.add(company['name'])
        for alias in company.get('alias', []):
            ALL_COMPANY_NAMES.add(alias)

# 具身智能关键词（用于识别新公司）
EMBODIED_AI_KEYWORDS = [
    '具身智能', '人形机器人', '仿生机器人', '工业机器人', '协作机器人',
    'Embodied AI', 'Humanoid Robot', 'Embodied Intelligence', 'Physical AI',
    '具身', '人形', '机器人大脑', 'VLA', 'World Model',
    'Manipulator', 'Dexterous Manipulation', 'Robot Arm', 'Mobile Manipulation'
]

# ============== 数据目录 ==============
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')
STATE_FILE = os.path.join(DATA_DIR, 'crawl_state.json')
POTENTIAL_COMPANIES_FILE = os.path.join(DATA_DIR, 'potential_companies.json')


class NewCompanyDetector:
    """新公司探测器 - 自动发现疑似具身智能新公司"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def is_known_company(self, name: str) -> bool:
        """检查是否是已知的公司"""
        name_lower = name.lower()
        for known_name in ALL_COMPANY_NAMES:
            if known_name.lower() in name_lower or name_lower in known_name.lower():
                return True
        return False
    
    def extract_company_from_text(self, text: str) -> List[Dict]:
        """从文本中提取可能的公司名"""
        found_companies = []
        
        # 具身智能相关关键词匹配
        for keyword in EMBODIED_AI_KEYWORDS:
            if keyword.lower() in text.lower():
                # 尝试提取公司名（通常在关键词附近）
                # 这里简化处理，实际可以用NLP
                pass
        
        return found_companies
    
    def search_for_new_companies(self) -> List[Dict]:
        """搜索新公司"""
        potential = []
        
        # 搜索来源
        search_sources = [
            {
                'name': '36Kr具身智能',
                'url': 'https://36kr.com/information/AI/20031',
                'selector': 'a.article-item-title',
            },
            {
                'name': '机器之心具身智能',
                'url': 'https://jiqizhixin.com/tags/embodied-ai',
                'selector': 'a.title',
            }
        ]
        
        for source in search_sources:
            try:
                resp = self.session.get(source['url'], timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # 查找所有文章标题
                for elem in soup.select(source['selector'])[:30]:
                    title = elem.get_text(strip=True)
                    url = elem.get('href', '')
                    if not url.startswith('http'):
                        url = 'https://36kr.com' + url if url.startswith('/') else url
                    
                    # 提取公司名（简单模式：找 "XX公司"、"XX机器人" 等）
                    company_patterns = [
                        r'([\u4e00-\u9fa5]{2,8}(?:公司|机器人|智能|科技))',
                        r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?(?:\s+AI|\s+Robotics|\s+Tech)?)',
                    ]
                    
                    for pattern in company_patterns:
                        matches = re.findall(pattern, title)
                        for match in matches:
                            if not self.is_known_company(match) and len(match) >= 3:
                                # 检查是否是具身智能相关
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
                print(f"[WARN] Failed to search {source['name']}: {e}")
        
        # 去重
        seen = set()
        unique_potential = []
        for p in potential:
            key = p['name']
            if key not in seen:
                seen.add(key)
                unique_potential.append(p)
        
        return unique_potential
    
    def load_existing(self) -> List[Dict]:
        """加载已发现的潜在公司"""
        if os.path.exists(POTENTIAL_COMPANIES_FILE):
            with open(POTENTIAL_COMPANIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save(self, potential_companies: List[Dict]):
        """保存潜在公司列表"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(POTENTIAL_COMPANIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(potential_companies, f, ensure_ascii=False, indent=2)
    
    def add_new_company(self, name: str, category: str):
        """将新公司添加到监测列表"""
        new_company = {'name': name, 'alias': [name]}
        
        # 根据分类确定添加到哪里
        if category == 'domestic_vla':
            COMPANIES['domestic_vla'].append(new_company)
        elif category == 'domestic_control':
            COMPANIES['domestic_control'].append(new_company)
        elif category == 'overseas_vla':
            COMPANIES['overseas_vla'].append(new_company)
        elif category == 'overseas_other':
            COMPANIES['overseas_other'].append(new_company)
        
        # 更新全局公司名列表
        ALL_COMPANY_NAMES.add(name)
        print(f"[OK] Added '{name}' to {category}")


class EmbodiedAICrawler:
    """具身智能媒体监测爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.new_company_detector = NewCompanyDetector()
    
    def _generate_id(self, url: str, title: str) -> str:
        """生成唯一ID用于去重"""
        content = f"{url}{title}".encode('utf-8')
        return hashlib.md5(content).hexdigest()[:12]
    
    def _is_recent(self, date_str: str, days: int = 30) -> bool:
        """检查日期是否在最近N天内"""
        try:
            # 尝试解析日期
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m-%d', '%m/%d']:
                try:
                    date = datetime.strptime(date_str, fmt)
                    # 假设是今年
                    date = date.replace(year=datetime.now().year)
                    delta = datetime.now() - date
                    return delta.days <= days
                except:
                    pass
            return True  # 无法解析时默认保留
        except:
            return True
    
    def crawl_bing_news(self, company_name: str) -> List[Dict]:
        """从Bing新闻搜索结果中获取信息"""
        results = []
        try:
            url = f"https://www.bing.com/news/search?q={quote(company_name)}+具身智能+OR+机器人+OR+AI"
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for item in soup.select('div.news-card')[:5]:
                title_elem = item.select_one('a.title')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                # 提取日期
                date_elem = item.select_one('span.news-date')
                date_str = date_elem.get_text(strip=True) if date_elem else ''
                
                # 提取来源
                source_elem = item.select_one('span.source')
                source = source_elem.get_text(strip=True) if source_elem else 'Bing News'
                
                # 判断事件类型
                event_type = self._classify_event(title)
                
                results.append({
                    'id': self._generate_id(link, title),
                    'company': company_name,
                    'type': event_type,
                    'title': title,
                    'title_en': None,  # 需要翻译
                    'summary': '',
                    'source': source,
                    'source_url': link,
                    'date': self._parse_date(date_str),
                    'created_at': datetime.now().isoformat(),
                    'media_sources': [source]
                })
                
        except Exception as e:
            print(f"[WARN] Bing search failed for {company_name}: {e}")
        
        return results
    
    def _classify_event(self, title: str) -> str:
        """分类事件类型"""
        title_lower = title.lower()
        
        if any(kw in title for kw in ['融资', '投资', '轮', '估值', '资金', 'Funding', 'Series']):
            return 'funding'
        elif any(kw in title for kw in ['发布', '推出', '推出', 'Launch', 'Release', 'Product']):
            return 'product'
        elif any(kw in title for kw in ['开源', 'Open Source', 'Dataset', '数据集']):
            return 'tech_breakthrough'
        elif any(kw in title for kw in ['合作', '落地', '签约', 'Deploy', 'Partnership']):
            return 'project'
        elif any(kw in title for kw in ['展会', '峰会', '大会', '论坛', 'Conference', 'Summit']):
            return 'event'
        elif any(kw in title for kw in ['采访', '观点', '访谈', 'CEO说', 'Interview']):
            return 'interview'
        else:
            return 'other'
    
    def _parse_date(self, date_str: str) -> str:
        """解析日期字符串"""
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        
        # 处理相对日期
        if '今天' in date_str or 'Today' in date_str:
            return datetime.now().strftime('%Y-%m-%d')
        elif '昨天' in date_str or 'Yesterday' in date_str:
            return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 尝试标准格式
        for fmt in ['%Y年%m月%d日', '%Y-%m-%d', '%m-%d', '%m/%d']:
            try:
                date = datetime.strptime(date_str, fmt)
                date = date.replace(year=datetime.now().year)
                return date.strftime('%Y-%m-%d')
            except:
                pass
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def crawl_all(self, incremental: bool = True) -> List[Dict]:
        """抓取所有公司数据"""
        all_events = []
        seen_ids = set()
        
        # 加载已有数据
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                seen_ids = {e['id'] for e in existing}
                all_events = existing.copy()
        
        # 获取所有公司
        all_companies = []
        for category, companies in COMPANIES.items():
            for company in companies:
                all_companies.append({
                    'name': company['name'],
                    'category': category
                })
        
        print(f"🔍 Monitoring {len(all_companies)} companies...")
        
        # 增量模式下只取最近更新的公司
        if incremental:
            state = self._load_state()
            last_crawl = state.get('last_crawl', None)
            if last_crawl:
                days_since = (datetime.now() - datetime.fromisoformat(last_crawl)).days
                if days_since < 7:
                    print(f"⏭️ Skipping crawl (last: {last_crawl}, {days_since} days ago)")
                    return all_events
        
        # 抓取每个公司的数据
        for company in all_companies:
            print(f"  📰 {company['name']}...", end=' ')
            events = self.crawl_bing_news(company['name'])
            
            new_count = 0
            for event in events:
                if event['id'] not in seen_ids:
                    all_events.append(event)
                    seen_ids.add(event['id'])
                    new_count += 1
            
            print(f"+{new_count}")
            time.sleep(0.5)  # 避免请求过快
        
        # 更新状态
        self._save_state()
        
        # 按日期排序
        all_events.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return all_events
    
    def _load_state(self) -> Dict:
        """加载爬虫状态"""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """保存爬虫状态"""
        os.makedirs(DATA_DIR, exist_ok=True)
        state = {'last_crawl': datetime.now().isoformat()}
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def save_data(self, events: List[Dict], validate: bool = True):
        """保存事件数据（带链接验证）"""
        # 验证链接
        if validate:
            print("\n🔍 Validating links...")
            validator = LinkValidator()
            events, report = validator.validate_events(events)

            print(f"   ✅ Valid: {report['valid']}")
            print(f"   ❌ Invalid: {report['invalid']}")

            if report['issues']:
                print("\n⚠️  Link issues found:")
                for issue in report['issues'][:5]:
                    print(f"   - [{issue['company']}] {issue['issue']}")
                    if 'fix' in issue:
                        print(f"     → {issue['fix']}")

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
    
    def detect_new_companies(self) -> List[Dict]:
        """运行新公司探测器"""
        print("\n🔬 Running new company detector...")
        new_found = self.new_company_detector.search_for_new_companies()
        
        # 加载已有的
        existing = self.new_company_detector.load_existing()
        
        # 合并去重
        seen = {p['name'] for p in existing}
        for p in new_found:
            if p['name'] not in seen:
                existing.append(p)
                seen.add(p['name'])
        
        # 保存
        self.new_company_detector.save(existing)
        
        print(f"📊 Found {len(new_found)} new potential companies")
        return existing


def main():
    """主函数"""
    print("=" * 50)
    print("Embodied AI Media Monitor - Low-cost Crawler")
    print("=" * 50)

    # 增量模式（默认）
    incremental = '--full' not in sys.argv
    detect_new = '--detect-new' in sys.argv
    validate_only = '--validate' in sys.argv  # 仅验证模式

    crawler = EmbodiedAICrawler()

    # 单独验证模式
    if validate_only:
        print("\n🔍 Validating existing events.json...")
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                events = json.load(f)
            validator = LinkValidator()
            events, report = validator.validate_events(events)
            print(f"\n📊 Validation Report:")
            print(f"   Total: {report['total']}")
            print(f"   Valid: {report['valid']}")
            print(f"   Invalid: {report['invalid']}")
            if report['issues']:
                print("\n⚠️  Issues:")
                for issue in report['issues']:
                    print(f"   - [{issue['company']}] {issue.get('url', 'N/A')}")
                    print(f"     {issue['issue']}")
        else:
            print("❌ events.json not found")
        return

    # 正常爬取模式
    events = crawler.crawl_all(incremental=incremental)
    crawler.save_data(events)  # 保存时自动验证

    # 检测新公司
    if detect_new:
        potential = crawler.detect_new_companies()
        print(f"\n📋 Potential new companies: {len(potential)}")

    print("\n[OK] Crawl completed!")

    # 统计
    funding_count = len([e for e in events if e.get('type') == 'funding'])
    pr_count = len(events) - funding_count
    print(f"   Funding events: {funding_count}")
    print(f"   PR updates: {pr_count}")
    print(f"   Total events: {len(events)}")


if __name__ == '__main__':
    main()
