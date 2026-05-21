const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf8');

// 找到getCompanyInfo函数体
const funcStart = html.indexOf('function getCompanyInfo(name) {');
const funcEnd = html.indexOf('function getEnglish(name)');
const funcBody = html.substring(funcStart, funcEnd);

// 分割公司 - 按缩进和公司名分割
const lines = funcBody.split('\n');
const companies = [];
let currentCompany = null;

lines.forEach((line, i) => {
    // 公司开始
    const startMatch = line.match(/^\s{12}'([^']+)':\s*\{/);
    if (startMatch) {
        currentCompany = { name: startMatch[1], hasFounders: false, hasPending: false, line: i };
    }
    
    if (currentCompany) {
        if (line.includes('founders:')) {
            currentCompany.hasFounders = true;
        }
        if (line.includes('待补充')) {
            currentCompany.hasPending = true;
        }
        
        // 公司结束（遇到另一个公司或函数结束）
        if (i > currentCompany.line && line.match(/^\s{8,12}'/)) {
            companies.push(currentCompany);
            currentCompany = null;
        }
    }
});

// 添加最后一个
if (currentCompany) {
    companies.push(currentCompany);
}

// 去重并统计
const seen = new Set();
const uniqueCompanies = companies.filter(c => {
    if (seen.has(c.name)) return false;
    seen.add(c.name);
    return true;
});

console.log('=== 有"待补充"的公司 ===');
const pending = uniqueCompanies.filter(c => c.hasPending);
console.log(`${pending.length} 个`);
pending.forEach(c => console.log(`  - ${c.name}`));

console.log('\n=== 无founders的公司 ===');
const noFounders = uniqueCompanies.filter(c => !c.hasFounders);
console.log(`${noFounders.length} 个`);

console.log('\n=== 有founders的公司 ===');
const hasFounders = uniqueCompanies.filter(c => c.hasFounders && !c.hasPending);
console.log(`${hasFounders.length} 个`);
hasFounders.forEach(c => console.log(`  - ${c.name}`));
