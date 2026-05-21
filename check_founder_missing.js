const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf8');

// 简单方法：直接搜索包含"待补充"的行
const lines = html.split('\n');
const pending = [];

lines.forEach((line, i) => {
    if (line.includes('待补充')) {
        // 往上找公司名
        for (let j = i; j >= 0 && j > i - 30; j--) {
            if (lines[j].match(/name:\s*['"][^'"]+['"]/)) {
                const nameMatch = lines[j].match(/name:\s*['"]([^'"]+)['"]/);
                const titleMatch = line.match(/title:\s*['"]([^'"]+)['"]/);
                if (nameMatch) {
                    pending.push({
                        name: nameMatch[1],
                        title: titleMatch ? titleMatch[1] : '未知',
                        line: i + 1
                    });
                }
                break;
            }
        }
    }
});

// 去重
const unique = [...new Map(pending.map(p => [p.name + p.title, p])).values()];

console.log('=== 有"待补充"的公司（共' + unique.length + '个）===\n');
unique.forEach((p, i) => {
    console.log(`${i+1}. ${p.name} - 缺失: ${p.title}`);
});

// 也搜索没有founders字段的公司
console.log('\n=== 正在检查无founders字段的公司... ===');
const noFounders = [];

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // 找公司定义开始
    if (line.match(/^\s{12}'[^']+':\s*\{/) && !line.includes('founders:')) {
        // 提取公司名
        const nameMatch = line.match(/'([^']+)':/);
        if (nameMatch) {
            const name = nameMatch[1];
            // 检查接下来的100行内是否有founders
            let hasFounders = false;
            for (let j = i; j < i + 100 && j < lines.length; j++) {
                if (lines[j].includes('founders:')) {
                    hasFounders = true;
                    break;
                }
                // 如果遇到下一个公司定义，停止
                if (j > i && lines[j].match(/^\s{12}'[^']+':\s*\{/)) {
                    break;
                }
            }
            if (!hasFounders) {
                noFounders.push(name);
            }
        }
    }
}

const uniqueNoFounders = [...new Set(noFounders)];
console.log(`\n无团队信息的公司（共${uniqueNoFounders.length}个）：\n`);
uniqueNoFounders.slice(0, 30).forEach((name, i) => {
    console.log(`${i+1}. ${name}`);
});
if (uniqueNoFounders.length > 30) {
    console.log(`... 等共 ${uniqueNoFounders.length} 个`);
}
