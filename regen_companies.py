# -*- coding: utf-8 -*-
import json

# UTF-16 编码读取 tag_data.json
with open('tag_data.json', 'r', encoding='utf-16') as f:
    tag_data = json.load(f)
print('Loaded %d companies' % len(tag_data))

OVERSEAS_SET = {
    'NVIDIA (英伟达)', 'Tesla Optimus (特斯拉)', 'Figure AI', '1X Technologies',
    'Hexagon (海克斯康)', 'Skild AI', 'Physical Intelligence', 'Anybotics',
    'Mimic Robotics', 'Field AI', 'Agility Robotics', 'Sunday Robotics',
    'Boston Dynamics', 'Skydio', 'Sanctuary AI', 'Apptronik', 'Generalist'
}

items_js = []
for item in tag_data:
    name = json.dumps(item['name'], ensure_ascii=False)
    brain = json.dumps(item.get('brain', '-') or '-', ensure_ascii=False)
    training = json.dumps(item.get('training', '-') or '-', ensure_ascii=False)
    scene = json.dumps(item.get('scene', '-') or '-', ensure_ascii=False)
    positioning = json.dumps(item.get('positioning', '-') or '-', ensure_ascii=False)
    overseas = 'true' if item['name'] in OVERSEAS_SET else 'false'
    items_js.append(
        '  { name:%s, overseas:%s, brain:%s, training:%s, scene:%s, positioning:%s }'
        % (name, overseas, brain, training, scene, positioning)
    )

js_data = ',\n'.join(items_js)

new_script = """
// ============================================================
// 标签数据（来自 标签2.xlsx）
// ============================================================
const allCompanies = [
%s
];

// Brain arch -> CSS class
function brainClass(brain) {
    if (!brain) return 'tag-default';
    if (brain.includes('E2E-VLA')) return 'tag-e2e';
    if (brain.includes('Hierarchical/RL')) return 'tag-sim2rl';
    if (brain.includes('Hierarchical')) return 'tag-hier';
    if (brain.includes('Sim2Real')) return 'tag-sim2rl';
    if (brain.includes('World Model')) return 'tag-world';
    if (brain.includes('Component')) return 'tag-comp';
    if (brain.includes('Platform-Hub')) return 'tag-hub';
    if (brain.includes('Platform') || brain.includes('Infra')) return 'tag-plat';
    if (brain.includes('Cross-Embodiment')) return 'tag-cross';
    if (brain.includes('IL-Teleop')) return 'tag-il';
    if (brain.includes('Brain-Vision')) return 'tag-vis';
    if (brain.includes('Integrated-OEM')) return 'tag-intg';
    return 'tag-default';
}

function renderTag(text, cls) {
    if (!text || text === '-') return '<span class="no-tag">---</span>';
    return '<span class="tag ' + cls + '">' + text + '</span>';
}

function renderPos(pos) {
    if (!pos || pos === '-') return '<span class="no-tag">---</span>';
    return '<span class="pos-text">' + pos + '</span>';
}

var activeFilter = 'all';

function renderTable() {
    var tbody = document.getElementById('tableBody');
    var search = document.getElementById('searchInput').value.trim().toLowerCase();
    var visCount = 0;
    var rows = allCompanies.map(function(c, i) {
        var brain    = c.brain    || '-';
        var training = c.training || '-';
        var scene    = c.scene    || '-';
        var pos      = c.positioning || '-';

        var matchesSearch = !search
            || c.name.toLowerCase().indexOf(search) > -1
            || brain.toLowerCase().indexOf(search) > -1
            || scene.toLowerCase().indexOf(search) > -1
            || training.toLowerCase().indexOf(search) > -1;

        var matchesFilter = true;
        if (activeFilter === 'overseas') matchesFilter = c.overseas;
        else if (activeFilter === 'domestic') matchesFilter = !c.overseas;
        else if (activeFilter !== 'all') {
            matchesFilter = brain.toLowerCase().indexOf(activeFilter.toLowerCase()) > -1;
        }

        var visible = matchesSearch && matchesFilter;
        if (visible) visCount++;

        return '<tr class="' + (visible ? '' : 'hidden') + '">' +
            '<td style="color:#334060;font-size:11px;white-space:nowrap;">' + (i + 1) + '</td>' +
            '<td class="col-name">' +
            '<a href="company.html?name=' + encodeURIComponent(c.name) + '" class="company-link">' +
            '<span class="region-dot ' + (c.overseas ? 'overseas' : 'domestic') + '"></span>' +
            c.name + '</a></td>' +
            '<td class="col-brain">' + renderTag(brain, brainClass(brain)) + '</td>' +
            '<td class="col-training">' + renderTag(training, 'tag-train') + '</td>' +
            '<td class="col-scene">' + renderTag(scene, 'tag-scene') + '</td>' +
            '<td class="col-pos">' + renderPos(pos) + '</td>' +
            '</tr>';
    });

    var emptyRow = visCount === 0
        ? '<tr class="empty-row"><td colspan="6">---</td></tr>' : '';

    tbody.innerHTML = rows.join('') + emptyRow;
    document.getElementById('visibleCount').textContent = visCount;
    document.getElementById('totalCount').textContent   = allCompanies.length;
}

function filterTable() { renderTable(); }

function setFilter(val, btn) {
    var btns = document.querySelectorAll('.filter-btn');
    for (var i = 0; i < btns.length; i++) btns[i].classList.remove('active');
    btn.classList.add('active');
    activeFilter = val;
    renderTable();
}

// Init
renderTable();
""" % js_data

# 替换 HTML 中的 script 内容
with open('companies.html', 'r', encoding='utf-8') as f:
    raw = f.read()

s_start = raw.index('<script>') + len('<script>')
s_end = raw.index('</script>', s_start)

new_html = raw[:s_start] + '\n' + new_script.strip() + '\n' + raw[s_end:]

with open('companies.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('companies.html regenerated successfully!')
