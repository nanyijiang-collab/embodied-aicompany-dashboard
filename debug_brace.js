const fs = require('fs');
const html = fs.readFileSync('company.html', 'utf-8');
const tagsDecl = html.indexOf('const companyTagsMap = {');
console.log('tagsDecl position:', tagsDecl);
console.log('Opening brace position:', tagsDecl + 24);
console.log('Char at decl+24:', JSON.stringify(html[tagsDecl + 24]));

let depth = 0, te = tagsDecl + 24;  // start AFTER the opening brace
let step = 0;
do {
    step++;
    if (html[te] === '{') depth++;
    else if (html[te] === '}') depth--;
    te++;
    if (step % 50000 === 0) console.log('step', step, 'depth', depth, 'char', JSON.stringify(html[te-1]));
} while (depth > 0);
console.log('Closing brace at position:', te - 1);
console.log('Closing brace char:', JSON.stringify(html[te - 1]));
const tagsBody = html.slice(tagsDecl, te - 1);
console.log('tagsBody length:', tagsBody.length);
console.log('tagsBody first 200:', JSON.stringify(tagsBody.substring(0, 200)));
console.log('tagsBody last 100:', JSON.stringify(tagsBody.substring(tagsBody.length - 100)));
