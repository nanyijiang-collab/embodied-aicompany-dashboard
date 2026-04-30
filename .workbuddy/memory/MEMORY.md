# 具身智能媒体监测系统 - 核心规范

## 估值排行榜（74家公司 - 2026年4月29日更新）
- 共74家公司（已删除：思特威Smartsens、智朝机器人、神源久机器人）

## 新增公司（2026-04-27）

## 数据规范

### 过滤规则（重要！）

**1. 来源黑名单**
- `世界机器人大会官网` - 数据有未来日期，来源不可靠

**2. 拼盘新闻过滤**
- 标题含以下关键词的文章会被过滤（汇总类文章）：
  - 周报、晚报、晨报、日报、周刊
  - 汇总、盘点、回顾、一览、总结
  - 周记、一周、本月、年度
  - Top10、TOP10
  - 今日要闻、今日新闻、今日资讯
  - 产业周报、行业周报、科技周报

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

## 数据统计（2026-04-27 晚）
- 总事件数：5107条
- 人事动态：100+条（含今天搜索新增）

## 已添加人事动态的公司（39家）
- Boston Dynamics：Aaron Saunders离职、Milan Kovac加入（特斯拉）、Robert Playter卸任CEO
- Agility Robotics：创始人Damion Shelton卸任CEO、Melonee Wise离职
- Figure AI：CTO Jerry Pratt离职、团队重组、Caitlin Kalinowski加入
- 1X Technologies：从特斯拉挖人
- Physical Intelligence：Karol Hausman创立
- 智元机器人：彭志辉创业+晋升总裁兼CTO、邓泰华加入CEO、魏强闫维新离职
- 魔法原子：创始人吴长征离职、CTO陈春玉接棒
- 星动纪元：陈建宇创业
- 银河通用：王鹤创业
- 千寻智能：韩峰涛创业
- 众擎机器人：李力耘加入CTO（前小鹏）
- 星海图：许华哲离职创业（破壳机器人）
- Sanctuary AI：创始人Geordie Rose被罢免CEO
- 特斯拉：Ashish Kumar离职加入Meta、Milan Kovac离职
- 宇树科技：王兴兴晋升董事长
- 傅利叶：顾捷创业
- 梅卡曼德：邵天兰创业
- 思灵机器人：陈兆芃创业
- 穹彻智能：卢策吾创业
- 大晓机器人：王晓刚出任董事长（商汤联合创始人）
- 逐际动力：COO张力离职
- Hexagon：Anders Svensson接任CEO
- Apptronik：Jeff Cardenas/Nicholas Paine创立
- Skild AI：Abhinav Gupta/Deepak Pathak创立
- 灵御智能：金戈创业
- Generalist：Pete Florence创业
- **智在无界：卢宗青创业（北大/智源背景，联想之星领投）**
- **Tesla Optimus：Milan Kovac离职、Ashish Kumar加入Meta**
- 昆仑行/至简动力/无界动力/小雨智造/阿米奥机器人/灵足时代/破壳机器人/原力无限

## 无重大人事变动的公司（45家）- 已确认搜索
优必选、英伟达、Figure、GR00T、Phoenix、Skydio、Sunday Robotics、七腾机器人、优理奇智能、光轮智能、加速进化、地瓜机器人、帕西尼感知、影身智能、星灿智能、智平方、智身科技、未来不远、泉智博、灵初智能、灵心巧手、珞石机器人、睿尔曼智能、知行机器人、简智新创、简智机器人、自变量机器人、觅蜂科技、跨维智能、镜识科技、Anybotics、Field AI、Galbot、Mimic Robotics、Apollo（百度）、Memo AI、EVE

## 缺人事动态的公司
无（51家公司已全部搜索完毕）

## 项目结构
- `index.html` - 主看板页面
- `company.html` - 公司详情页面（URL参数：?name=公司名，公司信息在getCompanyInfo函数中定义）
- `scripts/crawler.py` - 主爬虫脚本
- `scripts/add_personnel.py` - 人事动态添加脚本
- `data/events.json` - 事件数据库
- `data/potential_companies.json` - 潜在新公司
- `data/crawl_state.json` - 爬虫状态
- `docs/ADD_COMPANY_GUIDE.md` - 添加新公司标准工作流程
- `docs/标签体系SOP.md` - 标签打标标准作业程序

## 例行工作：新增公司必须打标签

**每次新增公司时，必须在 `companies.html` 的 `allCompanies` 数组中添加完整的标签信息：**

```javascript
{ 
  name:"公司名 (英文名)", 
  overseas:true/false, 
  brain:"[标签] 标签名", 
  training:"[标签] 标签名", 
  scene:"[标签] 场景名", 
  positioning:"定位描述" 
}
```

**标签参考文档**：`docs/标签体系SOP.md`

### Brain 架构标签（5类）
- `[E2E-VLA]` 端到端视言行
- `[World Model]` 物理世界模型
- `[Hierarchical]` 分层架构
- `[Cross-Embodiment]` 跨本体通用
- `[IL-Teleop]` 模仿学习
- `[Component]` 核心零部件

### Training 数据范式标签（3类）
- `[IL-Teleop]` 模仿学习（遥操作）
- `[Sim2Real-RL]` 仿真强化学习
- `[Synthetic-Data]` 合成数据

### Scene 场景标签（8类）
- `[I-Heavy]` 工业-重工
- `[I-Precision]` 工业-精密
- `[I-Light]` 轻工业
- `[L-Logistics]` 仓储物流
- `[S-Commercial]` 商业服务
- `[C-Home]` 家庭场景
- `[C-Edu]` 教育场景
- `[H-Special]` 特种巡检
- `[Agnostic]` 通用领域
- `[Research]` 科研
