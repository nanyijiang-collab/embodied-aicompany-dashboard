const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf8');

// 需要添加的缺失公司标签
const missingEntries = {
    'Apptronik': { brain: '[E2E-VLA] 端到端视言行', training: '[IL-Teleop] 模仿学习', scene: '[I-Heavy] 重工业' },
    'Sanctuary AI': { brain: '[E2E-VLA] 端到端视言行', training: '[VLM-Micro-tuning] 多模态微调', scene: '[I-Heavy] [S-Commercial]' },
    'Skydio': { brain: '[Autonomous-AI] 自主AI', training: '[Sim2Real-RL] 仿真强化学习', scene: '[H-Special] 特种巡检' },
    '英伟达 (NVIDIA)': { brain: '[Platform-Infra] 平台与基建', training: '[Synthetic-Data] 合成数据驱动', scene: '[Agnostic] 通用领域' },
    '星动纪元': { brain: '[E2E-VLA] 端到端视言行', training: '[VLA-Scaling] 模型规模化扩展', scene: '[I-Heavy] 重工业' },
    '智朝机器人': { brain: '[Hierarchical] 分层架构', training: '[IL-Teleop] 模仿学习', scene: '[S-Commercial] 商业服务' },
    '国家地方共建具身智能机器人创新中心': { brain: '[Platform-Hub] 平台中心', training: '[Policy-Standard] 行业标准', scene: '[Agnostic] 通用' },
    '共建中心 (创新中心)': { brain: '[Platform-Hub] 平台中心', training: '[Policy-Standard] 行业标准', scene: '[Agnostic] 通用' },
    '宇叠': { brain: '[E2E-VLA] 端到端视言行', training: '[Sim2Real-RL] 仿真强化学习', scene: '[I-Precision] 工业精密' },
    '诺亦腾': { brain: '[Component] 核心零部件', training: '[Precision-Trans] 精密传动', scene: '[Component] 零部件' },
    '坤维科技': { brain: '[Component] 核心零部件', training: '[Sensor-Fusion] 传感器融合', scene: '[I-Precision] 工业精密' },
    '因时机器人': { brain: '[Component] 核心零部件', training: '[Precision-Trans] 精密传动', scene: '[Component] 零部件' },
    '智平方机器人': { brain: '[E2E-VLA] 端到端视言行', training: '[VLA-Scaling] 模型规模化扩展', scene: '[Agnostic] 通用领域' },
    '星源智机器人': { brain: '[World Model] 物理世界模型', training: '[Sim2Real-RL] 仿真强化学习', scene: '[I-Heavy] 重工业' }
};

// 找到 companyTagsMap 的结束位置
const start = html.indexOf('const companyTagsMap = {');
const endSemi = html.indexOf(';', start + 20);

// 构建要添加的条目
const entriesToAdd = Object.entries(missingEntries)
    .map(([name, tags]) => {
        return `            '${name}': { brain: '${tags.brain}', training: '${tags.training}', scene: '${tags.scene}' }`;
    })
    .join(',\n');

// 插入到 }; 之前
let newHtml;
if (endSemi > 0) {
    // 检查最后一个条目后面有没有逗号
    const beforeSemi = html.substring(0, endSemi).trim();
    const lastChar = beforeSemi[beforeSemi.length - 1];

    if (lastChar === '}') {
        // 需要加逗号
        newHtml = html.substring(0, endSemi) + ',\n' + entriesToAdd + '\n        ' + html.substring(endSemi);
    } else {
        newHtml = html.substring(0, endSemi) + '\n' + entriesToAdd + '\n        ' + html.substring(endSemi);
    }
} else {
    console.error('找不到 companyTagsMap 的结束位置');
    process.exit(1);
}

fs.writeFileSync('company.html', newHtml);
console.log('已添加', Object.keys(missingEntries).length, '个缺失公司标签');
console.log('新增公司:', Object.keys(missingEntries).join(', '));

// 验证
const newHtmlContent = fs.readFileSync('company.html', 'utf8');
const newStart = newHtmlContent.indexOf('const companyTagsMap = {');
const newEndSemi = newHtmlContent.indexOf(';', newStart + 20);
const newBody = newHtmlContent.substring(newStart, newEndSemi + 1);
const newEntries = newBody.match(/['\"][^'\"]+['\"]\s*:/g);
console.log('\n验证: companyTagsMap 现在有', newEntries ? newEntries.length : 0, '个条目');
