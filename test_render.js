const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// 提取各数据块
const tagsDecl = html.indexOf('const companyTagsMap = {');
let depth = 0, te = tagsDecl;
do { if(html[te]=='{') depth++; else if(html[te]=='}') depth--; te++; } while(depth>0);
const tagsCode = html.slice(tagsDecl, te);

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

const code = [
    tagsCode,
    rdCode,
    enCode,
    giCode,
    'const r1 = getCompanyInfo("至简动力");',
    'const r2 = getCompanyInfo("逐际动力");',
    'console.log("=== 至简动力 ===");',
    'console.log("name:", r1?.name);',
    'console.log("valuation:", r1?.valuation);',
    'console.log("brain:", r1?.brain);',
    'console.log("scene:", r1?.scene);',
    'console.log("milestones:", JSON.stringify(r1?.milestones));',
    'console.log("=== 逐际动力 ===");',
    'console.log("name:", r2?.name);',
    'console.log("valuation:", r2?.valuation);',
    'console.log("brain:", r2?.brain);',
    'console.log("scene:", r2?.scene);',
].join('\n');

try {
    eval(code);
} catch(e) {
    console.error('Error:', e.message);
    const lines = code.split('\n');
    const m = e.stack.match(/:(\d+)/);
    if (m) {
        const n = parseInt(m[1]) - 1;
        for (let i = Math.max(0,n-3); i < Math.min(lines.length, n+4); i++) {
            console.error((i===n?'>>> ':'    '), i+1, ':', lines[i]);
        }
    }
}