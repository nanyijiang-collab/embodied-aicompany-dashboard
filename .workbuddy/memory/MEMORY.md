# 具身智能媒体监测系统 - 核心规范

## 数据规范

### 去重机制（重要！）
**每次数据更新必须经过去重，不允许直接追加！**

去重规则（三层）：
1. **ID去重**：已有ID不重复添加
2. **指纹去重**：同公司+同日期+同标题 → 重复
3. **相似度去重**：同公司+同日期+标题相似度≥0.8 → 重复

已集成去重的脚本：
- `scripts/crawler.py` - 主爬虫（save_data方法已集成去重）
- `scripts/add_personnel.py` - 人事动态添加（已集成去重）
- `scripts/fast_dedup.py` - 独立去重脚本（可单独运行）
- `scripts/dedup_personnel.py` - 人事动态去重脚本

独立去重命令：
```bash
python scripts/fast_dedup.py
```

## 数据统计（2026-04-27）
- 总事件数：5079条
- 融资：697条
- 产品：377条
- 项目：209条
- 采访：144条
- 技术突破：70条
- 活动展会：66条
- 人事动态：28条
- 其他：3488条

## 已添加人事动态的公司（约20家）
- Boston Dynamics：Aaron Saunders离职、Milan Kovac加入、Robert Playter卸任CEO
- Agility Robotics：Melonee Wise离职
- Figure AI：团队重组
- 1X Technologies：从特斯拉挖人
- Physical Intelligence：Karol Hausman创立
- 智元机器人：彭志辉创业+晋升总裁兼CTO
- 魔法原子：创始人吴长征离职、CTO陈春玉接棒
- 星动纪元：陈建宇创业
- 银河通用：王鹤创业
- 千寻智能：韩峰涛创业
- 众擎机器人：李力耘加入CTO
- 昆仑行/至简动力/无界动力/小雨智造/阿米奥机器人/灵足时代/破壳机器人

## 项目结构
- `index.html` - 主看板页面
- `company.html` - 公司详情页面（URL参数：?name=公司名）
- `scripts/crawler.py` - 主爬虫脚本
- `data/events.json` - 事件数据库
- `data/potential_companies.json` - 潜在新公司
- `data/crawl_state.json` - 爬虫状态
