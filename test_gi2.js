const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// Extract all needed sections cleanly
// 1. companyTagsMap - find the declaration
const tagsDecl = html.indexOf('const companyTagsMap = {');
// Find end by counting braces
let depth = 0, tagsEnd = tagsDecl;
do {
    if (html[tagsEnd] === '{') depth++;
    else if (html[tagsEnd] === '}') depth--;
    tagsEnd++;
} while (depth > 0);
const tagsCode = html.slice(tagsDecl, tagsEnd);

// 2. rankingData
const rdDecl = html.indexOf('const rankingData = [');
let depth2 = 0, rdEnd = rdDecl;
do {
    if (html[rdEnd] === '[') depth2++;
    else if (html[rdEnd] === ']') depth2--;
    rdEnd++;
} while (depth2 > 0);
rdEnd++; // include the semicolon
const rdCode = html.slice(rdDecl, rdEnd) + ';';

// 3. companyNameMapEN
const enDecl = html.indexOf('const companyNameMapEN = {');
let depth3 = 0, enEnd = enDecl;
do {
    if (html[enEnd] === '{') depth3++;
    else if (html[enEnd] === '}') depth3--;
    enEnd++;
} while (depth3 > 0);
enEnd++;
const enCode = html.slice(enDecl, enEnd) + ';';

// 4. getCompanyInfo
const giDecl = html.indexOf('function getCompanyInfo(name)');
let depth4 = 0, giEnd = giDecl;
do {
    if (html[giEnd] === '{') depth4++;
    else if (html[giEnd] === '}') depth4--;
    giEnd++;
} while (depth4 > 0);
giEnd++;
const giCode = html.slice(giDecl, giEnd);

// Test
const testName = process.argv[2] || '至简动力';
const code = [
    'const name = ' + JSON.stringify(testName) + ';',
    tagsCode,
    rdCode,
    enCode,
    giCode,
    "const result = getCompanyInfo(name);",
    "console.log('Result type:', typeof result);",
    "if (result) {",
    "  console.log('name:', result.name);",
    "  console.log('valuation:', result.valuation);",
    "  console.log('founded:', result.founded);",
    "  console.log('brain:', result.brain || '(empty)');",
    "  console.log('scene:', result.scene || '(empty)');",
    "} else {",
    "  console.log('RESULT IS NULL!');",
    "}"
].join('\n');

console.log('=== Testing getCompanyInfo("' + testName + '") ===');
try {
    new Function(code)();  // Use Function constructor to avoid eval issues
} catch (e) {
    console.error('JS Error:', e.message);
    const lines = code.split('\n');
    const m = e.stack.match(/:(\d+)/);
    if (m) {
        const n = parseInt(m[1]) - 1;
        for (let i = Math.max(0, n-2); i < Math.min(lines.length, n+3); i++) {
            console.error((i===n?'>>> ':'    ') + i + ': ' + lines[i]);
        }
    }
}