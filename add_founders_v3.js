const fs = require('fs');
let html = fs.readFileSync('company.html', 'utf8');

// 需要添加founders的公司列表
const companiesToUpdate = {
    'Figure AI': [
        {name: 'Brett Adcock', title: '创始人/CEO', bio: '2022年创立Figure AI，曾创办Venture民主化平台'},
        {name: 'Jerry Pratt', title: 'CTO', bio: 'IHMC 20年+人形机器人专家，2022年加入Figure AI'}
    ],
    '1X Technologies': [
        {name: 'Bernt Øivind Børnich', title: '创始人/CEO', bio: '2014年在挪威奥斯陆创立1X（前身Halodi Robotics），专注人形机器人研发'}
    ],
    'Skild AI': [
        {name: 'Deepak Pathak', title: '联合创始人/CEO', bio: '前卡内基梅隆大学教授，机器人和AI领域25年经验'},
        {name: 'Abhinav Gupta', title: '联合创始人/总裁', bio: '前卡内基梅隆大学教授，机器人领域25年经验'}
    ],
    'Physical Intelligence': [
        {name: 'Karol Hausman', title: '联合创始人/CEO', bio: '前Google DeepMind资深研究科学家，斯坦福大学兼职教授'},
        {name: 'Sergey Levine', title: '联合创始人', bio: 'UC Berkeley教授，深度强化学习先驱'}
    ],
    'Apptronik': [
        {name: 'Jeff Cardenas', title: '联合创始人/CEO', bio: '2016年创立Apptronik，机器人领域专家'},
        {name: 'Nick Paine', title: '联合创始人/CTO', bio: '2016年共同创立Apptronik，机器人技术负责人'}
    ],
    'Agility Robotics': [
        {name: 'Damion Shelton', title: '联合创始人/董事长', bio: '连续创业者，机器人领域先驱'},
        {name: 'Jonathan Hurst', title: '联合创始人/首席机器人官', bio: '前俄勒冈州立大学机器人教授，ATRIAS双足机器人发明者'},
        {name: 'Peggy Johnson', title: 'CEO', bio: '微软老将，2024年3月接任CEO'},
        {name: 'Melonee Wise', title: 'CTO', bio: '前Uber机器人负责人，Willow Garage总裁'}
    ],
    'Sanctuary AI': [
        {name: 'Geordie Rose', title: '联合创始人/CEO', bio: '量子计算背景，2018年创立Sanctuary AI'},
        {name: 'Olivia Norton', title: '联合创始人', bio: '共同创始人之一'}
    ],
    'Boston Dynamics': [
        {name: 'Marc Raibert', title: '创始人', bio: '1992年创立，MIT博士，卡特姆勒平衡理论创始人'},
        {name: 'Robert Playter', title: 'CEO', bio: '2020年担任CEO，前执行副总裁'}
    ],
    '灵心巧手': [
        {name: '周永', title: '创始人/CEO', bio: '华中科技大学少年班天才，2019年创立，专注柔性灵巧手研发'}
    ],
    '银河通用': [
        {name: '王鹤', title: '创始人/CTO', bio: '保送清华，斯坦福博士归国创业，2023年5月联合创立'},
        {name: '姚腾洲', title: '联合创始人', bio: '北航机器人研究所硕士，师从王田苗教授，曾任ABB机器人研发'}
    ],
    '它石智航': [
        {name: '陈亦伦', title: 'CEO', bio: '前华为自动驾驶CTO、清华大学AIR智能机器人方向首席专家、大疆首席工程师'},
        {name: '王兴兴', title: '联合创始人/首席技术顾问', bio: '宇树科技创始人，提供技术指导'}
    ],
    '星海图': [
        {name: '高继扬', title: '创始人/CEO', bio: '1992年生，清华电子系保送，南加州大学计算机视觉博士，曾任Waymo'}
    ],
    '星动纪元': [
        {name: '陈建宇', title: '创始人/CEO', bio: '清华大学交叉信息研究院助理教授、博士生导师，2023年8月创立'}
    ],
    '逐际动力': [
        {name: '张巍', title: '创始人/CEO', bio: '南方科技大学长聘教授，普渡大学博士，2017年专注足式机器人研究'}
    ],
    '光轮智能': [
        {name: '谢晨', title: '创始人/CEO', bio: '北京大学物理系学士，哥伦比亚大学数量金融博士，前英伟达、Cruise、蔚来高管'}
    ],
    'Sunday Robotics': [
        {name: '赵子豪 (Tony Zhao)', title: '联合创始人/CEO', bio: '斯坦福博士（退学），前DeepMind、Tesla工程师，Mobile ALOHA发明者'},
        {name: '迟宬 (Cheng Chi)', title: '联合创始人', bio: '哥伦比亚大学计算机科学博士'}
    ],
    'Skydio': [
        {name: 'Adam Bry', title: '联合创始人/CEO', bio: 'MIT背景，自主飞行无人机专家'},
        {name: 'Abe Bachrach', title: 'CTO', bio: '联合创始人，技术负责人'}
    ],
    '普渡机器人': [
        {name: '张涛', title: '创始人/CEO', bio: '专注服务机器人研发'}
    ],
    '帕西尼感知': [
        {name: '许晋诚', title: '创始人/CEO', bio: '师从日本早稻田大学菅野重树教授，触觉传感器专家'}
    ],
    '乐聚机器人': [
        {name: '常琳', title: '联合创始人/CEO', bio: '哈尔滨工业大学计算机博士，2016年创立'},
        {name: '冷晓琨', title: '联合创始人/CTO', bio: '哈工大博士，机器人技术负责人'}
    ],
    '魔法原子': [
        {name: '吴长征', title: '创始人/原CEO', bio: '前小米机器人核心研发负责人，2026年3月离职创业'},
        {name: '陈春玉', title: 'CEO', bio: '2026年3月接任CEO'}
    ],
    '无界动力': [
        {name: '张玉峰', title: '创始人/CEO', bio: '前智能驾驶领域技术专家，2025年创立'},
        {name: '夏中谱', title: '联合创始人/联席CTO', bio: '中科院自动化研究所博士，前理想汽车智驾端到端技术负责人'}
    ],
    '思灵机器人': [
        {name: '陈兆芃', title: '创始人/CEO', bio: '德国慕尼黑工业大学硕士，2018年创立'}
    ],
    '梅卡曼德': [
        {name: '邵天兰', title: '创始人/CEO', bio: '清华大学软件学院本科，德国慕尼黑工业大学机器人硕士'}
    ],
    '至简动力': [
        {name: '贾鹏', title: '创始人/CEO', bio: '前理想汽车智驾技术研发负责人，2025年7月创立'},
        {name: '王凯', title: '联合创始人/董事长', bio: '前理想汽车CTO'},
        {name: '王佳佳', title: '联合创始人/COO', bio: '前理想汽车智驾量产负责人'}
    ]
};

let updatedCount = 0;

Object.keys(companiesToUpdate).forEach(companyName => {
    const founders = companiesToUpdate[companyName];
    
    // 查找公司定义开始位置
    const companyStartStr = `'${companyName}': {`;
    const startPos = html.indexOf(companyStartStr);
    
    if (startPos === -1) {
        console.log(`未找到公司: ${companyName}`);
        return;
    }
    
    // 在这个公司的定义范围内检查是否已有founders
    // 找到公司定义结束位置（下一个公司开始或函数结束）
    let endPos = startPos + companyStartStr.length;
    let braceCount = 1;
    let inString = false;
    let stringChar = '';
    
    for (let i = endPos; i < html.length && braceCount > 0; i++) {
        const c = html[i];
        const prev = i > 0 ? html[i-1] : '';
        
        if (!inString) {
            if (c === '"' || c === "'") {
                inString = true;
                stringChar = c;
            } else if (c === '{') {
                braceCount++;
            } else if (c === '}') {
                braceCount--;
                if (braceCount === 0) {
                    endPos = i + 1;
                    break;
                }
            }
        } else {
            if (c === stringChar && prev !== '\\') {
                inString = false;
            }
        }
    }
    
    const companyBlock = html.substring(startPos, endPos);
    
    // 检查这个公司是否已有founders
    if (companyBlock.includes('founders:')) {
        console.log(`已有founders: ${companyName}`);
        return;
    }
    
    // 生成founders字符串
    const foundersStr = '\n                    founders: [\n' + 
        founders.map(f => `                        {name: '${f.name}', title: '${f.title}', bio: '${f.bio}'},`).join('\n') + 
        '\n                    ],';
    
    // 找到scene字段后的位置
    const sceneMatch = companyBlock.match(/scene:\s*\[[^\]]+\],\s*/);
    
    if (sceneMatch) {
        const sceneEndInBlock = companyBlock.indexOf(sceneMatch[0]) + sceneMatch[0].length;
        const insertPos = startPos + sceneEndInBlock;
        
        html = html.slice(0, insertPos) + foundersStr + html.slice(insertPos);
        
        console.log(`已添加: ${companyName}`);
        updatedCount++;
    } else {
        console.log(`未找到scene字段: ${companyName}`);
    }
});

fs.writeFileSync('company.html', html);
console.log(`\n共更新了 ${updatedCount} 个公司`);
