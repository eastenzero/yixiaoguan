from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from pypdf import PdfReader, PdfWriter
from pathlib import Path
import io

router = APIRouter(prefix='/api/materials', tags=['materials'])

_MATERIALS_DIR = Path('/app/materials')
if not _MATERIALS_DIR.exists():
    _MATERIALS_DIR = Path(__file__).parent.parent.parent.parent.parent / 'deploy' / 'materials'

_CACHE: dict = {}
_MAX_CACHE = 50

@router.get('/slice')
async def slice_pdf(
    file: str = Query(..., description='PDF 文件名'),
    start: int = Query(..., ge=1, description='起始页码(1-indexed)'),
    end: int = Query(..., ge=1, description='结束页码(1-indexed)'),
):
    if '/' in file or chr(92) in file or '..' in file:
        raise HTTPException(400, '非法文件名')

    pdf_path = _MATERIALS_DIR / file
    if not pdf_path.exists():
        raise HTTPException(404, 'PDF 文件不存在')

    if end < start:
        raise HTTPException(400, 'end 必须 >= start')

    if end - start + 1 > 20:
        raise HTTPException(400, '单次最多裁剪 20 页')

    cache_key = (file, start, end)
    if cache_key in _CACHE:
        pdf_bytes = _CACHE[cache_key]
    else:
        try:
            reader = PdfReader(str(pdf_path))
            total = len(reader.pages)
            if start > total:
                raise HTTPException(400, f'起始页超出范围(共{total}页)')
            actual_end = min(end, total)
            writer = PdfWriter()
            for i in range(start - 1, actual_end):
                writer.add_page(reader.pages[i])
            buf = io.BytesIO()
            writer.write(buf)
            pdf_bytes = buf.getvalue()
            if len(_CACHE) >= _MAX_CACHE:
                _CACHE.pop(next(iter(_CACHE)))
            _CACHE[cache_key] = pdf_bytes
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(500, f'PDF 裁剪失败: {str(e)}')

    slug = file.replace('.pdf', '')
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type='application/pdf',
        headers={'Content-Disposition': f'inline; filename="{slug}_p{start}-{end}.pdf"'}
    )
