# F-V5E-02 Knowledge API Report

## Files Created/Modified

### Created
- `services/ai-service/app/api/knowledge.py` - New API router with GET /api/knowledge/entries/{entry_id} endpoint

### Modified
- `services/ai-service/main.py` - Added knowledge router import and registration
- `deploy/docker-compose.yml` - Added volume mounts for knowledge-base and materials
- `deploy/nginx/conf.d/student.conf` - Knowledge API nginx location block (already present)

## Build Result

```
#9 DONE 2.8s
#10 [ai-service 6/6] RUN mkdir -p /app/data/chroma
#10 DONE 0.1s
#11 [ai-service] exporting to image
#11 exporting layers
#11 exporting layers 4.7s done
#11 writing image sha256:ee991c6445c7b4679a70383a061121aa36074caf7341b9975d9101dc53ff42aa
#11 naming to docker.io/library/deploy-ai-service done
#11 DONE 5.4s
#12 [ai-service] resolving provenance for metadata file
#12 DONE 0.1s
 ai-service  Built
```

Services status after restart:
```
yx_ai_service     deploy-ai-service     "uvicorn main:app --…"   ai-service     23 seconds ago   Up 16 seconds (healthy)   0.0.0.0:8000->8000/tcp
yx_nginx          nginx:1.25-alpine     "/docker-entrypoint.…"   nginx          3 hours ago      Up 53 minutes             0.0.0.0:80-81->80-81/tcp
```

## Curl Verification Output

### AC-E05: Base entry ID test
```bash
curl -s 'http://localhost/api/knowledge/entries/KB-0150-电费缴纳指南' | python3 -c 'import json,sys; d=json.load(sys.stdin); print("code:", d.get("code")); print("title:", d["data"]["title"]); print("url:", d["data"]["material_file_url"]); print("content_len:", len(d["data"]["content"]))'
```
Output:
```
code: 0
title: 电费缴纳指南
url: /materials/student-handbook.pdf
content_len: 477
```

### AC-E06: Chunk ID test
```bash
curl -s 'http://localhost/api/knowledge/entries/KB-0150-电费缴纳指南__chunk_0' | python3 -c 'import json,sys; d=json.load(sys.stdin); print("AC-E06 chunk-id PASS" if d.get("code")==0 else "FAIL")'
```
Output:
```
AC-E06 chunk-id PASS
```

### AC-E07: material_file_url verification
The response includes:
- `material_file_url: "/materials/student-handbook.pdf"`
- `material_title: "学生手册（含图片版）"`

## AC Acceptance Summary

| AC | Description | Status |
|----|-------------|--------|
| AC-E05 | GET /api/knowledge/entries/KB-0150-电费缴纳指南 returns full MD | ✅ PASS |
| AC-E06 | GET with chunk ID (KB-0150-电费缴纳指南__chunk_0) also works | ✅ PASS |
| AC-E07 | Returns material_file_url field | ✅ PASS |

## Implementation Notes

1. **Path Resolution**: The code detects container vs local dev environment by checking if `knowledge-base` and `materials` directories exist at the base path.

2. **Volume Mounts Added to docker-compose.yml**:
   - `../knowledge-base:/app/knowledge-base:ro` - KB entries
   - `./materials:/app/materials:ro` - Material index and PDFs

3. **Frontmatter Parsing**: Simple regex-based YAML frontmatter parser extracts metadata (title, material_id, category, tags) from markdown files.

4. **Chunk ID Handling**: The entry_id parameter is split on `__chunk_` to extract the base entry ID, allowing both full entry IDs and chunk IDs to work.
