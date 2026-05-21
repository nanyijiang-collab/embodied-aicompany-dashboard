const fs = require('fs');
let html = fs.readFileSync('company.html', 'utf8');

// 收集的创始人信息 (第一批 Top20)
const foundersData = {
    'Figure AI': {
        founders: [
            {name: 'Brett Adcock', title: '创始人/CEO', bio: '2022年创立Figure AI，曾创办Venture民主化平台'},
            {name: 'Jerry Pratt', title: 'CTO', bio: 'IHMC 20年+人形机器人专家，2022年加入Figure AI'}
        ]
    },
    '1X Technologies': {
        founders: [
            {name: 'Bernt Øivind Børnich', title: '创始人/CEO', bio: '2014年在挪威奥斯陆创立1X（前身Halodi Robotics），专注人形机器人研发'}
        ]
    },
    'Skild AI': {
        founders: [
            {name: 'Deepak Pathak', title: '联合创始人/CEO', bio: '前卡内基梅隆大学教授，机器人和AI领域25年经验'},
            {name: 'Abhinav Gupta', title: '联合创始人/总裁', bio: '前卡内基梅隆大学教授，机器人领域25年经验'}
        ]
    },
    'Physical Intelligence': {
        founders: [
            {name: 'Karol Hausman', title: '联合创始人/CEO', bio: '前Google DeepMind资深研究科学家，斯坦福大学兼职教授'},
            {name: 'Sergey Levine', title: '联合创始人', bio: 'UC Berkeley教授，深度强化学习先驱'}
        ]
    },
    'Apptronik': {
        founders: [
            {name: 'Jeff Cardenas', title: '联合创始人/CEO', bio: '2016年创立Apptronik，机器人领域专家'},
            {name: 'Nick Paine', title: '联合创始人/CTO', bio: '2016年共同创立Apptronik，机器人技术负责人'}
        ]
    },
    'Agility Robotics': {
        founders: [
            {name: 'Damion Shelton', title: '联合创始人/董事长', bio: '连续创业者，机器人领域先驱'},
            {name: 'Jonathan Hurst', title: '联合创始人/首席机器人官', bio: '前俄勒冈州立大学机器人教授，ATRIAS双足机器人发明者'},
            {name: 'Peggy Johnson', title: 'CEO', bio: '微软老将，2024年3月接任CEO'},
            {name: 'Melonee Wise', title: 'CTO', bio: '前Uber机器人负责人，Willow Garage总裁'}
        ]
    },
    'Sanctuary AI': {
        founders: [
            {name: 'Geordie Rose', title: '联合创始人/CEO', bio: '量子计算背景，2018年创立Sanctuary AI'},
            {name: 'Olivia Norton', title: '联合创始人', bio: '共同创始人之一'}
        ]
    },
    'Boston Dynamics': {
        founders: [
            {name: 'Marc Raibert', title: '创始人', bio: '1992年创立，MIT博士，卡特姆勒平衡理论创始人'},
            {name: 'Robert Playter', title: 'CEO', bio: '2020年担任CEO，前执行副总裁'}
        ]
    },
    '灵心巧手': {
        founders: [
            {name: '周永', title: '创始人/CEO', bio: '华中科技大学少年班天才，2019年创立，专注柔性灵巧手研发'}
        ]
    },
    '银河通用': {
        founders: [
            {name: '王鹤', title: '创始人/CTO', bio: '保送清华，斯坦福博士归国创业，2023年5月联合创立'},
            {name: '姚腾洲', title: '联合创始人', bio: '北航机器人研究所硕士，师从王田苗教授，曾任ABB机器人研发'}
        ]
    },
    '它石智航': {
        founders: [
            {name: '陈亦伦', title: 'CEO', bio: '前华为自动驾驶CTO、清华大学AIR智能机器人方向首席专家、大疆首席工程师'},
            {name: '王兴兴', title: '联合创始人/首席技术顾问', bio: '宇树科技创始人，提供技术指导'}
        ]
    },
    '星海图': {
        founders: [
            {name: '高继扬', title: '创始人/CEO', bio: '1992年生，清华电子系保送，南加州大学计算机视觉博士，曾任Waymo'}
        ]
    },
    '星动纪元': {
        founders: [
            {name: '陈建宇', title: '创始人/CEO', bio: '清华大学交叉信息研究院助理教授、博士生导师，2023年8月创立'}
        ]
    },
    '逐际动力': {
        founders: [
            {name: '张巍', title: '创始人/CEO', bio: '南方科技大学长聘教授，普渡大学博士，2017年专注足式机器人研究'}
        ]
    },
    '光轮智能': {
        founders: [
            {name: '谢晨', title: '创始人/CEO', bio: '北京大学物理系学士，哥伦比亚大学数量金融博士，前英伟达、Cruise、蔚来高管'}
        ]
    },
    'Sunday Robotics': {
        founders: [
            {name: '赵子豪 (Tony Zhao)', title: '联合创始人/CEO', bio: '斯坦福博士（退学），前DeepMind、Tesla工程师，Mobile ALOHA发明者'},
            {name: '迟宬 (Cheng Chi)', title: '联合创始人', bio: '哥伦比亚大学计算机科学博士'}
        ]
    },
    'Skydio': {
        founders: [
            {name: 'Adam Bry', title: '联合创始人/CEO', bio: 'MIT背景，自主飞行无人机专家'},
            {name: 'Abe Bachrach', title: 'CTO', bio: '联合创始人，技术负责人'}
        ]
    },
    '普渡机器人': {
        founders: [
            {name: '张涛', title: '创始人/CEO', bio: '专注服务机器人研发'}
        ]
    },
    '帕西尼感知': {
        founders: [
            {name: '许晋诚', title: '创始人/CEO', bio: '师从日本早稻田大学菅野重树教授，触觉传感器专家，工信部人形机器人标准化技术委员会委员'}
        ]
    },
    '乐聚机器人': {
        founders: [
            {name: '常琳', title: '联合创始人/CEO', bio: '哈尔滨工业大学计算机博士，2016年创立'},
            {name: '冷晓琨', title: '联合创始人/CTO', bio: '哈工大博士，机器人技术负责人'}
        ]
    },
    '魔法原子': {
        founders: [
            {name: '吴长征', title: '创始人/原CEO', bio: '前小米机器人核心研发负责人，2026年3月离职创业'},
            {name: '陈春玉', title: 'CEO', bio: '2026年3月接任CEO'}
        ]
    },
    '无界动力': {
        founders: [
            {name: '张玉峰', title: '创始人/CEO', bio: '前智能驾驶领域技术专家，2025年创立'},
            {name: '夏中谱', title: '联合创始人/联席CTO', bio: '中科院自动化研究所博士，前理想汽车智驾端到端技术负责人'}
        ]
    },
    '思灵机器人': {
        founders: [
            {name: '陈兆芃', title: '创始人/CEO', bio: '德国慕尼黑工业大学硕士，2018年创立'}
        ]
    },
    '梅卡曼德': {
        founders: [
            {name: '邵天兰', title: '创始人/CEO', bio: '清华大学软件学院本科，德国慕尼黑工业大学机器人硕士'}
        ]
    },
    '至简动力': {
        founders: [
            {name: '贾鹏', title: '创始人/CEO', bio: '前理想汽车智驾技术研发负责人，2025年7月创立'},
            {name: '王凯', title: '联合创始人/董事长', bio: '前理想汽车CTO'},
            {name: '王佳佳', title: '联合创始人/COO', bio: '前理想汽车智驾量产负责人'}
        ]
    },
    '苏度科技': {
        founders: [
            {name: '待补充', title: '创始人/CEO', bio: '核心团队来自清华大学'}
        ]
    },
    '超维动力': {
        founders: [
            {name: '待补充', title: '联合创始人', bio: '核心团队来自机器人、自动驾驶和人工智能领域'}
        ]
    },
    '自然意志': {
        founders: [
            {name: '待补充', title: '联合创始人', bio: '待补充'}
        ]
    },
    'Generalist': {
        founders: [
            {name: 'Pete Florence', title: 'CEO/创始人', bio: '前DeepMind高级研究科学家，参与PaLM-E、RT-2项目'},
            {name: '待补充', title: 'CTO', bio: '核心团队来自OpenAI、Google DeepMind、Waymo等'}
        ]
    }
};

// 找到每个公司定义，检查是否已有founders，然后添加
const companyNames = Object.keys(foundersData);
let updatedCount = 0;

companyNames.forEach(companyName => {
    // 检查是否已有founders字段
    const hasFoundersRegex = new RegExp(`['\"]${companyName}['\"][\\s\\S]{0,2000}founders:\\s*\\[`);
    if (!hasFoundersRegex.test(html)) {
        // 找到公司定义的结束位置（下一个顶层属性前）
        const companyStartRegex = new RegExp(`['\"]${companyName}['\"]:\\s*\\{`);
        const match = html.match(companyStartRegex);
        
        if (match) {
            const startPos = html.indexOf(match[0]) + match[0].length;
            
            // 找到公司对象结束位置（下一个公司开始前的,}）
            const rest = html.substring(startPos);
            const braceCount = { count: 1, inString: false, stringChar: '' };
            let endPos = 0;
            
            for (let i = 0; i < rest.length; i++) {
                const c = rest[i];
                const prev = i > 0 ? rest[i-1] : '';
                
                if (!braceCount.inString) {
                    if (c === '"' || c === "'") {
                        braceCount.inString = true;
                        braceCount.stringChar = c;
                    } else if (c === '{') {
                        braceCount.count++;
                    } else if (c === '}') {
                        braceCount.count--;
                        if (braceCount.count === 0) {
                            endPos = startPos + i;
                            break;
                        }
                    }
                } else {
                    if (c === braceCount.stringChar && prev !== '\\') {
                        braceCount.inString = false;
                    }
                }
            }
            
            if (endPos > startPos) {
                // 插入founders
                const founders = foundersData[companyName].founders;
                let foundersStr = 'founders: [\n';
                founders.forEach(f => {
                    foundersStr += `                        {name: '${f.name}', title: '${f.title}', bio: '${f.bio}'},\n`;
                });
                foundersStr += '                    ],';
                
                // 在最后一个属性后插入
                const insertPos = endPos - 1;
                html = html.slice(0, insertPos) + ',\n                    ' + foundersStr + '\n                ' + html.slice(insertPos + 1);
                updatedCount++;
                console.log(`已添加: ${companyName}`);
            }
        }
    } else {
        console.log(`已有founders: ${companyName}`);
    }
});

fs.writeFileSync('company.html', html);
console.log(`\n共更新了 ${updatedCount} 个公司`);
