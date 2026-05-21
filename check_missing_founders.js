const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf8');

// 提取rankingData获取估值
const rankingMatch = html.match(/const rankingData = \[([\s\S]*?)\];/);
const rankingStr = rankingMatch[1];

// 解析估值数据
const valuationRegex = /company:\s*['"]([^'"]+)['"].*?valuationCNY:\s*(\d+)/g;
const valuations = {};
let match;
while ((match = valuationRegex.exec(rankingStr)) !== null) {
    valuations[match[1]] = parseInt(match[2]) || 0;
}

// 也从valuation字符串提取估值
const valStrRegex = /company:\s*['"]([^'"]+)['"].*?valuation:\s*['"]([^'"]+)['"]/g;
while ((match = valStrRegex.exec(rankingStr)) !== null) {
    const name = match[1];
    const valStr = match[2];
    if (!valuations[name]) {
        // 尝试从字符串提取数字
        const numMatch = valStr.match(/(\d+(?:\.\d+)?)/);
        if (numMatch) {
            if (valStr.includes('亿美元') || valStr.includes('美元')) {
                valuations[name] = parseFloat(numMatch[1]) * 7.2;
            } else if (valStr.includes('港元') || valStr.includes('港币')) {
                valuations[name] = parseFloat(numMatch[1]) * 0.9;
            } else {
                valuations[name] = parseFloat(numMatch[1]);
            }
        }
    }
}

// 提取getCompanyInfo中的公司及其founders状态
const funcStart = html.indexOf('function getCompanyInfo(name) {');
const funcEnd = html.lastIndexOf('return null;\n            }');
const funcBody = html.substring(funcStart, funcEnd);

// 分割成各个公司
const companyRegex = /['"]([^'"]+)':\s*\{[\s\S]*?(?=,\s*['"][^'"]+':\s*\{|$)/g;
const companies = [];
let companyMatch;

while ((companyMatch = companyRegex.exec(funcBody)) !== null) {
    const name = companyMatch[1];
    const block = companyMatch[0];
    
    // 跳过重复或空名
    if (!name || name.length < 2) continue;
    
    // 检查是否有待补充
    const hasPending = block.includes('待补充');
    
    // 检查是否有founders
    const hasFounders = block.includes('founders:');
    
    // 如果有待补充或没有founders
    if (hasPending || !hasFounders) {
        companies.push({
            name,
            hasFounders,
            hasPending,
            valuation: valuations[name] || 0
        });
    }
}

// 按估值排序
companies.sort((a, b) => b.valuation - a.valuation);

// 输出
console.log('=== 需要补充团队信息的公司（按估值排序）===\n');

let count = 0;
companies.forEach((c, i) => {
    if (c.valuation > 0 || c.hasPending) {
        count++;
        const status = c.hasPending ? '[有"待补充"]' : '[无团队信息]';
        const val = c.valuation > 0 ? `${c.valuation}亿` : '估值未知';
        console.log(`${count}. ${c.name} ${status} - ${val}`);
    }
});

console.log(`\n共 ${count} 个公司需要补充团队信息`);
console.log('\n=== 按估值Top20优先处理 ===');
companies.slice(0, 20).forEach((c, i) => {
    const status = c.hasPending ? '[待补充]' : '[无信息]';
    const val = c.valuation > 0 ? `${c.valuation}亿` : '估值未知';
    console.log(`${i+1}. ${c.name} - ${val} ${status}`);
});
