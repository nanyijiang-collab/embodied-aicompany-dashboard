const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// 正确的提取：body_start 在 opening { 之后一位
const tagsDecl = html.indexOf('const companyTagsMap = {');
const bodyStart = tagsDecl + 25;  // after the opening {
let depth = 0, te = bodyStart;
do {
    if (html[te] === '{') depth++;
    else if (html[te] === '}') depth--;
    te++;
} while (depth > 0);
const tagsBody = html.slice(bodyStart, te - 1);
console.log('tagsBody length:', tagsBody.length);
console.log('first 200:', JSON.stringify(tagsBody.substring(0, 200)));

// rankingData
const rdDecl = html.indexOf('const rankingData = [');
const rdStart = rdDecl + 19;  // after [
depth=0; let re2=rdStart;
do { if(html[re2]=='[') depth++; else if(html[re2]==']') depth--; re2++; } while(depth>0);
const rdCode = html.slice(rdDecl+19, re2-1)+';';

// companyNameMapEN
const enDecl = html.indexOf('const companyNameMapEN = {');
const enStart = enDecl + 24;
depth=0; let ee=enStart;
do { if(html[ee]=='{') depth++; else if(html[ee]=='}') depth--; ee++; } while(depth>0);
const enCode = html.slice(enDecl+24, ee-1)+';';

// getCompanyInfo
const giDecl = html.indexOf('function getCompanyInfo(name)');
depth=0; let ge=giDecl;
do { if(html[ge]=='{') depth++; else if(html[ge]=='}') depth--; ge++; } while(depth>0);
ge++;
const giCode = html.slice(giDecl, ge);

const code = [
    'const companyTagsMap = {' + tagsBody + '};',
    rdCode,
    enCode,
    giCode,
    "const r1 = getCompanyInfo('至简动力');",
    "const r2 = getCompanyInfo('宇树科技');",
    "const r3 = getCompanyInfo('Figure AI');",
    "console.log('=== 至简动力 ===');",
    "console.log('NULL?', r1 === null);",
    "console.log('name:', r1?.name);",
    "console.log('valuation:', r1?.valuation);",
    "console.log('brain:', r1?.brain || '(empty)');",
    "console.log('scene:', r1?.scene || '(empty)');",
    "console.log('=== 宇树科技 ===');",
    "console.log('name:', r2?.name, 'brain:', r2?.brain || '(empty)');",
    "console.log('=== Figure AI ===');",
    "console.log('name:', r3?.name, 'brain:', r3?.brain || '(empty)');",
].join('\n');

console.log('\ncode sizes - tags:', tagsBody.length, 'rd:', rdCode.length, 'en:', enCode.length, 'gi:', giCode.length);
console.log('\n--- Testing ---');
try {
    eval(code);
} catch(e) {
    console.error('JS Error:', e.message);
    const lines = code.split('\n');
    const m = e.stack.match(/:(\d+)/);
    if (m) {
        const n = parseInt(m[1]) - 1;
        for (let i = Math.max(0,n-3); i < Math.min(lines.length,n+4); i++) {
            console.error((i===n?'>>> ':'    '), i+1, ':', lines[i].substring(0,120));
        }
    }
}