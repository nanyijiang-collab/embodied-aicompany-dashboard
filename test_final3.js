const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// 找最后一个 const companyTagsMap = { （实际数据定义）
let lastTagsDecl = -1, pos = 0;
while (true) {
    const idx = html.indexOf('const companyTagsMap = {', pos);
    if (idx === -1) break;
    lastTagsDecl = idx;
    pos = idx + 1;
}
console.log('companyTagsMap 声明位置:', lastTagsDecl);
console.log('周围:', JSON.stringify(html.substring(lastTagsDecl, lastTagsDecl+60)));

// 提取 companyTagsMap
const tagsDecl = lastTagsDecl;
const bodyStart = tagsDecl + 24;  // char AFTER opening {
let depth = 1, te = bodyStart;   // start at 1 since we're AFTER the opening brace
do {
    if (html[te] === '{') depth++;
    else if (html[te] === '}') depth--;
    te++;
} while (depth > 0);
const tagsBody = html.slice(bodyStart, te - 1);
console.log('tagsBody length:', tagsBody.length, '(should be > 0)');
console.log('first 200:', JSON.stringify(tagsBody.substring(0, 200)));

// 找 rankingData
let lastRD = -1; pos = 0;
while (true) {
    const idx = html.indexOf('const rankingData = [', pos);
    if (idx === -1) break;
    lastRD = idx; pos = idx + 1;
}
console.log('\nrankingData 位置:', lastRD);
const rdStart = lastRD + 19;
depth = 0; let re2 = rdStart;
do { if(html[re2]==='[') depth++; else if(html[re2]===']') depth--; re2++; } while(depth>0);
const rdCode = html.slice(rdStart, re2-1) + ';';
console.log('rankingData code length:', rdCode.length);

// 找 companyNameMapEN
let lastEN = -1; pos = 0;
while (true) {
    const idx = html.indexOf('const companyNameMapEN = {', pos);
    if (idx === -1) break;
    lastEN = idx; pos = idx + 1;
}
console.log('companyNameMapEN 位置:', lastEN);
const enStart = lastEN + 24;
depth = 0; let ee = enStart;
do { if(html[ee]==='{') depth++; else if(html[ee]==='}') depth--; ee++; } while(depth>0);
const enCode = html.slice(enStart, ee-1) + ';';
console.log('companyNameMapEN code length:', enCode.length);

// 找 getCompanyInfo
const giDecl = html.indexOf('function getCompanyInfo(name)');
depth = 0; let ge = giDecl;
do { if(html[ge]==='{') depth++; else if(html[ge]==='}') depth--; ge++; } while(depth>0);
ge++;
const giCode = html.slice(giDecl, ge);
console.log('getCompanyInfo code length:', giCode.length);

const code = [
    'const companyTagsMap = {' + tagsBody + '};',
    rdCode,
    enCode,
    giCode,
    "const r1 = getCompanyInfo('至简动力');",
    "const r2 = getCompanyInfo('宇树科技');",
    "const r3 = getCompanyInfo('Figure AI');",
    "console.log('\\n=== 至简动力 ===');",
    "console.log('NULL?', r1 === null);",
    "console.log('name:', r1?.name);",
    "console.log('valuation:', r1?.valuation);",
    "console.log('founded:', r1?.founded);",
    "console.log('headquarters:', r1?.headquarters);",
    "console.log('brain:', r1?.brain || '(empty)');",
    "console.log('training:', r1?.training || '(empty)');",
    "console.log('scene:', r1?.scene || '(empty)');",
    "console.log('milestones:', JSON.stringify(r1?.milestones));",
    "console.log('\\n=== 宇树科技 (in companies object) ===');",
    "console.log('name:', r2?.name, 'brain:', r2?.brain || '(empty)');",
    "console.log('\\n=== Figure AI (overseas) ===');",
    "console.log('name:', r3?.name, 'brain:', r3?.brain || '(empty)');",
].join('\n');

console.log('\n=== Running tests ===');
try {
    eval(code);
} catch(e) {
    console.error('JS Error:', e.message);
    const lines = code.split('\n');
    const m = e.stack.match(/:(\d+)/);
    if (m) {
        const n = parseInt(m[1]) - 1;
        for (let i = Math.max(0,n-3); i < Math.min(lines.length,n+4); i++) {
            const marker = (i===n) ? '>>> ' : '    ';
            console.error(marker + (i+1) + ': ' + lines[i].substring(0, 150));
        }
    }
}