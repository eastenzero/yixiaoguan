import os

files = [
    'KB-20260324-0105.md', 'KB-20260324-0106.md', 'KB-20260324-0107.md',
    'KB-20260324-0108.md', 'KB-20260324-0109.md', 'KB-20260324-0110.md',
    'KB-20260324-0111.md', 'KB-20260324-0112.md', 'KB-20260324-0113.md',
    'KB-20260324-0114.md', 'KB-20260324-0115.md', 'KB-20260324-0116.md',
    'KB-20260324-0117.md', 'KB-20260324-0118.md', 'KB-20260324-0119.md',
    'KB-20260324-0120.md', 'KB-20260324-0121.md', 'KB-20260324-0122.md',
    'KB-20260324-0123.md'
]

base = 'knowledge-base/entries/first-batch-drafts/'
results = []

for f in files:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    lines = content.split('\n')
    dash_count = 0
    fm_end = -1
    for i, line in enumerate(lines):
        if line.strip() == '---':
            dash_count += 1
            if dash_count == 2:
                fm_end = i
                break
    modified = False
    old_title = ''
    new_title = ''
    if fm_end != -1:
        for i in range(fm_end + 1, len(lines)):
            if lines[i].startswith('# '):
                old_title = lines[i]
                new_title = '## ' + lines[i][2:]
                lines[i] = new_title
                modified = True
                break
    if modified:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))
        results.append((f, old_title, new_title, '已修改'))
    else:
        results.append((f, '', '', '无需修改/未找到'))

modified_count = sum(1 for r in results if r[3] == '已修改')
print(f'修改完成: {modified_count}/{len(files)}')
