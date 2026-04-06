from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import json, re
import os

router = APIRouter(prefix='/api/knowledge', tags=['knowledge'])

# Paths (relative to this file: app/api/knowledge.py)
_BASE = Path(__file__).parent.parent.parent  # = services/ai-service/ or /app in container

# In container: volumes mounted at /app/knowledge-base and /app/materials
# In dev: paths are relative to project root (2 levels up from this file)
_IN_CONTAINER = (_BASE / 'knowledge-base').exists() and (_BASE / 'materials').exists()

if _IN_CONTAINER:
    _KB_ENTRIES = _BASE / 'knowledge-base' / 'entries'
    _MATERIAL_INDEX = _BASE / 'materials' / 'material-index.json'
else:
    # Local dev: resolve from project root
    _PROJECT_ROOT = _BASE.parent.parent
    _KB_ENTRIES = _PROJECT_ROOT / 'knowledge-base' / 'entries'
    _MATERIAL_INDEX = _PROJECT_ROOT / 'deploy' / 'materials' / 'material-index.json'


def _load_material_index() -> dict:
    if not _MATERIAL_INDEX.exists():
        return {}
    with open(_MATERIAL_INDEX, 'r', encoding='utf-8') as f:
        return json.load(f)


def _find_entry_file(base_entry_id: str) -> Path | None:
    for md_file in _KB_ENTRIES.rglob('*.md'):
        if md_file.stem == base_entry_id:
            return md_file
    return None


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith('---'):
        return {}, text
    end = text.find('---', 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end+3:].strip()
    fm = {}
    for line in fm_text.splitlines():
        m = re.match(r'^(\w+):\s*(.+)$', line.strip())
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            fm[key] = val
    return fm, body


@router.get('/entries/{entry_id}')
async def get_entry(entry_id: str):
    base_id = entry_id.split('__chunk_')[0]
    md_file = _find_entry_file(base_id)
    if not md_file:
        raise HTTPException(status_code=404, detail='条目不存在')
    text = md_file.read_text(encoding='utf-8')
    fm, body = _parse_frontmatter(text)
    material_id = fm.get('material_id', '')
    title = fm.get('title', base_id)
    idx = _load_material_index()
    mat_info = idx.get(material_id, {})
    pdf = mat_info.get('pdf', '')
    material_file_url = f'/materials/{pdf}' if pdf else ''
    material_title = mat_info.get('title', '')
    return JSONResponse({
        'code': 0,
        'msg': 'success',
        'data': {
            'entry_id': base_id,
            'title': title,
            'content': body,
            'material_file_url': material_file_url,
            'material_title': material_title,
            'page_start': fm.get('page_start', ''),
            'page_end': fm.get('page_end', ''),
            'metadata': {k: v for k, v in fm.items() if k not in ('title', 'material_id')}
        }
    })
