# F-V5E-03 Frontend Nav — Implementation Report

## Files Changed

1. **CREATED** `apps/student-app/src/api/knowledge.ts`
   - New API module with `KnowledgeEntryFull` interface and `getKnowledgeEntryFull(entryId)` function
   - Calls `GET /api/knowledge/entries/:entryId`, returns null on failure

2. **MODIFIED** `apps/student-app/src/pages/chat/index.vue`
   - Added `extractBaseEntryId(rawEntryId)` — strips `__chunk_N` suffix from entry IDs
   - Replaced `handleSourceClick`: now uses `extractBaseEntryId` (string-safe) instead of `normalizeEntryId` (numeric-only); navigates to `/pages/knowledge/detail` with full query params including `material_file_url` and `material_title`
   - Replaced `openSourceDetailFromPreview`: navigates to knowledge detail page instead of directly to PDF
   - Changed popup action button text from dynamic `'查看原始文件' : '查看参考摘要'` to static `查看详细资料`

3. **MODIFIED** `apps/student-app/src/pages/knowledge/detail.vue`
   - Added import: `getKnowledgeEntryFull` from `@/api/knowledge`
   - Added refs: `entryIdStr`, `materialFileUrl`, `materialTitle`
   - Replaced `onLoad`: reads `entry_id` (string) instead of `id` (numeric); decodes all URL params including `material_file_url` and `material_title`
   - Replaced `loadDetail`: calls `getKnowledgeEntryFull(entryIdStr)` API; falls back gracefully on failure
   - Added `openOriginalFile()` function: navigates to `/pages/viewer/pdf`
   - Added `<button v-if="materialFileUrl" class="view-original-btn" @click="openOriginalFile">查看原始文件</button>` in template
   - Added `.view-original-btn` SCSS styles

## Build Result

```
DONE  Build complete.
```
Exit status: 0 (no errors, only pre-existing deprecation warnings from Dart Sass)

## Key Code Changes

- Root cause fix: `normalizeEntryId` converted string entry IDs to numbers, always returning null for ChromaDB string IDs like `KB-20260323-0001-chunk-5`. Replaced with `extractBaseEntryId` which strips chunk suffix and preserves string format.
- Navigation flow: source click → knowledge detail page (with full metadata) → "查看原始文件" button → PDF viewer
- API fallback: if `getKnowledgeEntryFull` fails, `loadFailed=true` and fallback summary from URL params is displayed (AC-E11)
