const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// 用 Python 先提取好，再用 Node 只做测试
// 先用 Python 写提取好的数据到临时文件
// 这里直接尝试：把 companyTagsMap 的内容简化测试

// 检查 companyTagsMap 第一屏
const tagsDecl = html.indexOf('const companyTagsMap = {');
let depth = 0, te = tagsDecl;
do { if(html[te]=='{') depth++; else if(html[te]=='}') depth--; te++; } while(depth>0);
const tagsBody = html.slice(tagsDecl, te);

// 找 tagsBody 里的奇怪引用
const lines = tagsBody.split('\n');
for (const line of lines.slice(0, 20)) {
    console.log(line.substring(0, 100));
}

// 尝试只看 rankingData + getCompanyInfo，不看 companyTagsMap
const rdDecl = html.indexOf('const rankingData = [');
depth=0; let re2=rdDecl;
do { if(html[re2]=='[') depth++; else if(html[re2]==']') depth--; re2++; } while(depth>0);
re2++;
const rdCode = html.slice(rdDecl, re2)+';';

const enDecl = html.indexOf('const companyNameMapEN = {');
depth=0; let ee=enDecl;
do { if(html[ee]=='{') depth++; else if(html[ee]=='}') depth--; ee++; } while(depth>0);
ee++;
const enCode = html.slice(enDecl, ee)+';';

const giDecl = html.indexOf('function getCompanyInfo(name)');
depth=0; let ge=giDecl;
do { if(html[ge]=='{') depth++; else if(html[ge]=='}') depth--; ge++; } while(depth>0);
ge++;
const giCode = html.slice(giDecl, ge);

// 跳过 companyTagsMap，只测 rankingData + getCompanyInfo
const code2 = [
    rdCode,
    enCode,
    giCode,
    "console.log('normName test:', normName('至简动力 (Simple)'), '==>', normName('至简动力'));",
    "const r1 = getCompanyInfo('至简动力');",
    "console.log('name:', r1?.name, 'valuation:', r1?.valuation, 'brain:', r1?.brain, 'scene:', r1?.scene);",
    "const r2 = getCompanyInfo('宇树科技');",
    "console.log('宇树 name:', r2?.name, 'brain:', r2?.brain, 'scene:', r2?.scene);",
].join('\n');

console.log('\n--- Testing without companyTagsMap ---');
try {
    eval(code2);
} catch(e) {
    console.error('Error:', e.message);
}