const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');

// Extract rankingData
const rdStart = html.indexOf('const rankingData = [');
const rdEnd = html.indexOf('];', rdStart) + 2;
const rdCode = 'const rankingData = ' + html.slice(rdStart + 19, rdEnd) + ';';

// Extract companyTagsMap
const tagsStart = html.indexOf('const companyTagsMap = {');
const bodyStart = tagsStart + 25;
let depth = 1, i = bodyStart;
while (i < html.length && depth > 0) {
    if (html[i] === '{') depth++;
    else if (html[i] === '}') depth--;
    i++;
}
const tagsBody = html.slice(bodyStart, i - 1);
const tagsCode = 'const companyTagsMap = {' + tagsBody + '};';

// Extract companyNameMapEN
const enStart = html.indexOf('const companyNameMapEN = {');
const enEnd = html.indexOf('};', enStart) + 2;
const enBody = html.slice(enStart + 24, enEnd - 2);
const enCode = 'const companyNameMapEN = {' + enBody + '};';

// Extract getCompanyInfo
const giStart = html.indexOf('function getCompanyInfo(name)');
let depth2 = 0, j = giStart;
while (j < html.length) {
    if (html[j] === '{') depth2++;
    else if (html[j] === '}') {
        depth2--;
        if (depth2 === 0) { j++; break; }
    }
    j++;
}
const giCode = html.slice(giStart, j);

// Test
const testName = process.argv[2] || '至简动力';
const testCode = [
    "const name = '" + testName + "';",
    tagsCode,
    rdCode,
    enCode,
    giCode,
    "const result = getCompanyInfo(name);",
    "console.log('Result type:', typeof result);",
    "console.log('Result:', JSON.stringify(result, null, 2));"
].join('\n');

console.log('Testing with name:', testName);
console.log('---');
try {
    eval(testCode);
} catch (e) {
    console.error('Error:', e.message);
    // Find the line
    const lines = testCode.split('\n');
    const match = e.stack.match(/:(\d+):/);
    if (match) {
        const lineNum = parseInt(match[1]) - 1;
        console.error('Near line:', lines[lineNum - 2], '|', lines[lineNum - 1], '|', lines[lineNum]);
    }
}