# Task Report: f-v5d-05-frontend-upgrade

**Status**: COMPLETED  
**Completed At**: 2026-04-06  
**Executor**: T3

---

## STEP-PLAN

1. Update `apps/student-app/src/pages/chat/index.vue`:
   - [1a] Extend Source interface with `material_file_url` and `material_title`
   - [1b] Extend sourcePreview ref with `materialFileUrl`
   - [1c] Update SSE parsing (2 locations) to map new fields
   - [1d] Update showSourcePreviewPopup to use material_title as priority
   - [1e] Replace openSourceDetailFromPreview with PDF-first logic
   - [1f] Update button template with conditional text
   - [1g,h] Update SCSS for safe-area padding and source-item styling

2. Create `apps/student-app/src/pages/viewer/pdf.vue` (new file)

3. Update `apps/student-app/src/pages.json` to add pdf viewer route

4. Build verification with `npx uni build -p h5`

5. Rebuild nginx static files and restart nginx

---

## STEP-EXECUTED

### [1] chat/index.vue Changes

#### [1a] Source Interface (line ~243-249)
```typescript
interface Source {
  entry_id: string
  title: string
  content?: string
  url: string
  score?: number
  material_file_url?: string  // ADDED
  material_title?: string      // ADDED
}
```

#### [1b] sourcePreview Ref (line ~269-281)
```typescript
const sourcePreview = ref<{
  visible: boolean
  entryId: string
  title: string
  content: string
  score?: number
  materialFileUrl?: string  // ADDED
}>({
  visible: false,
  entryId: '',
  title: '',
  content: '',
  score: undefined,
  materialFileUrl: undefined  // ADDED
})
```

#### [1c] SSE Parsing (2 locations - lines ~478 and ~507)
Both locations updated to include:
```typescript
material_file_url: s.material_file_url || '',
material_title: s.material_title || ''
```

#### [1d] showSourcePreviewPopup (line ~630)
- Title now uses `source.material_title || source.title || '参考资料'`
- Added `materialFileUrl: source.material_file_url || ''`

#### [1e] openSourceDetailFromPreview (line ~644)
Complete replacement with PDF-first logic:
- If `materialFileUrl` exists → navigate to `/pages/viewer/pdf`
- Else if `entryId` exists → navigate to `/pages/knowledge/detail`
- Else close popup

#### [1f] Button Template (line ~195-206)
- Updated `v-if` to check both `entryId || materialFileUrl`
- Added conditional text: `{{ sourcePreview.materialFileUrl ? '查看原始文件' : '查看参考摘要' }}`

#### [1g] SCSS - source-preview-actions (line ~1457)
- Changed padding-bottom to: `max(12px, env(safe-area-inset-bottom, 12px))`
- Updated `.preview-btn` with `justify-content: center` and increased height to 44px
- Added `.preview-btn-disabled` class

#### [1h] SCSS - source-item (line ~1169)
- Updated background to `#ffffff`
- Updated border to `1px solid rgba(0, 106, 100, 0.2)`

---

### [2] Created pdf.vue

**Path**: `apps/student-app/src/pages/viewer/pdf.vue`

Features:
- Custom navbar with back button (←)
- Web-view component for PDF rendering
- URL and title passed via query params
- Full viewport height with safe-area support

---

### [3] pages.json Route Added

```json
{
  "path": "pages/viewer/pdf",
  "style": {
    "navigationBarTitleText": "原始文件",
    "navigationStyle": "custom"
  }
}
```

Route added after `pages/knowledge/detail` entry.

---

### [4] Build Verification

```bash
cd /home/easten/dev/yixiaoguan/apps/student-app
source ~/.nvm/nvm.sh && nvm use 24
npx uni build -p h5
```

**Result**: `DONE  Build complete.`

Only deprecation warnings (Sass @import, legacy-js-api) - no errors.

---

### [5] Nginx Rebuild

```bash
docker compose -f deploy/docker-compose.yml build student-nginx
docker compose -f deploy/docker-compose.yml restart nginx
```

Both commands completed successfully.

---

## STEP-CHECK

| Check | Status |
|-------|--------|
| Source interface extended | ✅ |
| sourcePreview ref extended | ✅ |
| SSE parsing (both locations) updated | ✅ |
| showSourcePreviewPopup uses material_title | ✅ |
| openSourceDetailFromPreview PDF-first logic | ✅ |
| Button conditional text | ✅ |
| SCSS safe-area padding | ✅ |
| SCSS source-item border/background | ✅ |
| pdf.vue created | ✅ |
| pages.json route added | ✅ |
| Build passes | ✅ |
| Nginx rebuilt | ✅ |

---

## BLOCKERS

None.

---

## Files Changed

1. `apps/student-app/src/pages/chat/index.vue` - Modified
2. `apps/student-app/src/pages/viewer/pdf.vue` - Created
3. `apps/student-app/src/pages.json` - Modified

---

## New Anti-Patterns Discovered

None.
