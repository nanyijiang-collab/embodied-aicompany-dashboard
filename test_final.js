const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// 正确的提取方式
const tagsDecl = html.indexOf('const companyTagsMap = {');
let depth = 0, te = tagsDecl + 24;  // start AT the opening {
do {
    if (html[te] === '{') depth++;
    else if (html[te] === '}') depth--;
    te++;
} while (depth > 0);
// 现在 te 指向 closing } 的下一位
const tagsBody = html.slice(tagsDecl + 24, te - 1);
console.log('tagsBody length:', tagsBody.length);
console.log('tagsBody first 200:', JSON.stringify(tagsBody.substring(0, 200)));
console.log('tagsBody last 50:', JSON.stringify(tagsBody.substring(tagsBody.length - 50)));

// 构建测试代码
const rdDecl = html.indexOf('const rankingData = [');
depth=0; let re2=rdDecl+18;
do { if(html[re2]=='[') depth++; else if(html[re2]==']') depth--; re2++; } while(depth>0);
const rdCode = html.slice(rdDecl+19, re2-1)+';';

const enDecl = html.indexOf('const companyNameMapEN = {');
depth=0; let ee=enDecl+24;
do { if(html[ee]=='{') depth++; else if(html[ee]=='}') depth--; ee++; } while(depth>0);
const enCode = html.slice(enDecl+24, ee-1)+';';

const giDecl = html.indexOf('function getCompanyInfo(name)');
depth=0; let ge=giDecl;
do { if(html[ge]=='{') depth++; else if(html[ge]=='}') depth--; ge++; } while(depth>0);
const giCode = html.slice(giDecl, ge+1);

console.log('\nExtracted code sizes:');
console.log('companyTagsMap:', tagsBody.length, 'chars');
console.log('rankingData:', rdCode.length, 'chars');
console.log('companyNameMapEN:', enCode.length, 'chars');
console.log('getCompanyInfo:', giCode.length, 'chars');

// 测试 getCompanyInfo
const code = [
    'const companyTagsMap = {' + tagsBody + '};',
    rdCode,
    enCode,
    giCode,
    "const r1 = getCompanyInfo('至简动力');",
    "const r2 = getCompanyInfo('宇树科技');",
    "const r3 = getCompanyInfo('Figure AI');",
    "console.log('=== 至简动力 ===');",
    "console.log('result:', r1 ? 'VALID' : 'NULL');",
    "console.log('name:', r1?.name);",
    "console.log('valuation:', r1?.valuation);",
    "console.log('brain:', r1?.brain || '(empty)');",
    "console.log('scene:', r1?.scene || '(empty)');",
    "console.log('=== 宇树科技 ===');",
    "console.log('name:', r2?.name, 'brain:', r2?.brain || '(empty)');",
    "console.log('=== Figure AI ===');",
    "console.log('name:', r3?.name, 'brain:', r3?.brain || '(empty)');",
].join('\n');

console.log('\n--- Testing ---');
try {
    eval(code);
} catch(e) {
    console.error('JS Error:', e.message);
}