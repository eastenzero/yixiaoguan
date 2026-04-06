<template>
  <view class="knowledge-detail-page">
    <view v-if="isLoading" class="loading-state">
      <text class="loading-title">正在加载参考资料...</text>
    </view>

    <view v-else class="content-wrapper">
      <view class="hero-card">
        <text class="hero-label">参考资料</text>
        <text class="hero-title">{{ displayTitle }}</text>

        <view class="hero-meta">
          <text v-if="entryId" class="meta-chip">条目 #{{ entryId }}</text>
          <text v-if="displayScore !== null" class="meta-chip">相关度 {{ Math.round(displayScore * 100) }}%</text>
          <text v-if="entry?.categoryName" class="meta-chip">{{ entry.categoryName }}</text>
        </view>
      </view>

      <view v-if="showFallbackNotice" class="fallback-notice">
        <text>以下为该参考资料的相关摘要</text>
      </view>

      <!-- 标签展示 -->
      <view v-if="displayTags.length > 0" class="tags-section">
        <view class="tags-list">
          <text v-for="tag in displayTags" :key="tag.id" class="tag-item">{{ tag.name }}</text>
        </view>
      </view>

      <view v-if="renderedContent" class="detail-card markdown-body" v-html="renderedContent"></view>
      <view v-else-if="renderedFallbackSummary" class="detail-card markdown-body" v-html="renderedFallbackSummary"></view>
      <view v-else class="detail-card plain-content">
        <text>{{ displaySummary || '暂无可展示内容' }}</text>
      </view>
      <button
        v-if="materialFileUrl"
        class="view-original-btn"
        @click="openOriginalFile"
      >查看原始文件</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import MarkdownIt from 'markdown-it'
import type { KnowledgeEntry, KnowledgeTag } from '@/types/knowledge'
import { getKnowledgeEntryFull } from '@/api/knowledge'

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: false,
  breaks: true
})

const isLoading = ref(true)
const loadFailed = ref(false)
const entryId = ref<number | null>(null)
const entryIdStr = ref<string>('')
const materialFileUrl = ref<string>('')
const materialTitle = ref<string>('')
const pageStart = ref<number>(0)
const pageEnd = ref<number>(0)
const entry = ref<KnowledgeEntry | null>(null)
const fallbackTitle = ref('')
const fallbackSummary = ref('')
const fallbackScore = ref<number | null>(null)
const fallbackTags = ref<KnowledgeTag[]>([])

const displayTitle = computed(() => {
  return entry.value?.title || fallbackTitle.value || '参考资料'
})

const displaySummary = computed(() => {
  return entry.value?.summary || fallbackSummary.value
})

const displayScore = computed(() => {
  if (entry.value?.hitCount !== undefined) {
    return null
  }
  return fallbackScore.value
})

const displayTags = computed(() => {
  return entry.value?.tags || fallbackTags.value || []
})

const renderedContent = computed(() => {
  const content = entry.value?.content || ''
  return content ? md.render(content) : ''
})

const renderedFallbackSummary = computed(() => {
  const summary = fallbackSummary.value
  return summary ? md.render(summary) : ''
})

const showFallbackNotice = computed(() => {
  return loadFailed.value && (!!fallbackSummary.value || !!fallbackTitle.value)
})

function parseEntryId(raw: unknown): number | null {
  const parsed = Number(raw)
  if (!Number.isFinite(parsed) || parsed <= 0) return null
  return parsed
}

function decodeText(raw: unknown): string {
  if (typeof raw !== 'string') return ''
  try {
    return decodeURIComponent(raw)
  } catch {
    return raw
  }
}

function parseScore(raw: unknown): number | null {
  const parsed = Number(raw)
  if (!Number.isFinite(parsed) || parsed < 0) return null
  return parsed
}

function parseTags(raw: unknown): KnowledgeTag[] {
  if (typeof raw !== 'string') return []
  try {
    const decoded = decodeURIComponent(raw)
    const parsed = JSON.parse(decoded)
    if (Array.isArray(parsed)) {
      return parsed.filter(t => t && typeof t.id === 'number' && typeof t.name === 'string')
    }
  } catch {
    // ignore
  }
  return []
}

async function loadDetail() {
  if (!entryIdStr.value) {
    loadFailed.value = true
    isLoading.value = false
    return
  }
  try {
    const data = await getKnowledgeEntryFull(entryIdStr.value)
    if (data) {
      entry.value = {
        title: data.title,
        content: data.content,
      } as any
      if (data.material_file_url) materialFileUrl.value = data.material_file_url
      if (data.material_title) materialTitle.value = data.material_title
      if (data.page_start) pageStart.value = parseInt(String(data.page_start)) || 0
      if (data.page_end) pageEnd.value = parseInt(String(data.page_end)) || 0
      loadFailed.value = false
    } else {
      loadFailed.value = true
    }
  } catch {
    loadFailed.value = true
  }
  isLoading.value = false
}

onLoad((options: any) => {
  entryIdStr.value = decodeURIComponent(options?.entry_id || options?.id || '')
  fallbackTitle.value = decodeURIComponent(options?.title || '')
  fallbackSummary.value = decodeURIComponent(options?.summary || '')
  fallbackScore.value = parseFloat(options?.score || '0') || 0
  materialFileUrl.value = decodeURIComponent(options?.material_file_url || '')
  materialTitle.value = decodeURIComponent(options?.material_title || '')
  loadDetail()
})
function openOriginalFile() {
  let pdfUrl: string
  const ttl = encodeURIComponent(
    materialTitle.value || fallbackTitle.value || '原始文件'
  )

  if (pageStart.value > 0 && materialFileUrl.value) {
    const file = materialFileUrl.value.split('/').pop() || ''
    const endPage = pageEnd.value || (pageStart.value + 4)
    pdfUrl = encodeURIComponent(
      '/api/materials/slice?file=' + file + '&start=' + pageStart.value + '&end=' + endPage
    )
  } else if (materialFileUrl.value) {
    pdfUrl = encodeURIComponent(materialFileUrl.value)
  } else {
    return
  }

  uni.navigateTo({
    url: '/pages/viewer/pdf?url=' + pdfUrl + '&title=' + ttl
  })
}
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

.knowledge-detail-page {
  min-height: 100vh;
  padding: 16px;
  background: linear-gradient(180deg, #eef4f3 0%, #f6f8f7 100%);
}

.loading-state {
  padding-top: 48px;
  text-align: center;

  .loading-title {
    font: $text-body-medium;
    color: $neutral-50;
  }
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero-card {
  padding: 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, $primary 0%, #05857d 100%);
  color: #ffffff;

  .hero-label {
    display: block;
    font: $text-label-medium;
    opacity: 0.86;
    margin-bottom: 6px;
  }

  .hero-title {
    display: block;
    font: $text-title-large;
    line-height: 1.45;
  }

  .hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }

  .meta-chip {
    padding: 4px 10px;
    border-radius: 999px;
    font: $text-label-small;
    background: rgba(255, 255, 255, 0.2);
  }
}

.fallback-notice {
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(0, 106, 100, 0.06);

  text {
    font: $text-label-medium;
    color: $primary;
  }
}

.tags-section {
  .tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .tag-item {
    padding: 4px 10px;
    border-radius: 999px;
    font: $text-label-small;
    background: rgba(0, 106, 100, 0.1);
    color: $primary;
  }
}

.detail-card {
  padding: 16px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(23, 29, 28, 0.06);
}

.plain-content {
  text {
    font: $text-body-medium;
    color: $neutral-20;
    line-height: 1.7;
    white-space: pre-wrap;
  }
}

.markdown-body {
  font-size: 14px;
  line-height: 1.7;
  color: $neutral-20;
  word-break: break-word;

  :deep(> *:first-child) { margin-top: 0 !important; }
  :deep(> *:last-child) { margin-bottom: 0 !important; }

  :deep(p) { margin: 0 0 10px 0; }

  :deep(h1), :deep(h2), :deep(h3), :deep(h4) {
    margin: 14px 0 8px 0;
    line-height: 1.45;
    color: #005a55;
    font-weight: 600;
  }

  :deep(h1) { font-size: 18px; }
  :deep(h2) { font-size: 16px; }
  :deep(h3) { font-size: 15px; }

  :deep(ul), :deep(ol) {
    margin: 8px 0;
    padding-left: 18px;
  }

  :deep(li) {
    margin: 4px 0;
  }

  :deep(code) {
    background: rgba(0, 106, 100, 0.1);
    border-radius: 4px;
    padding: 2px 5px;
    font-size: 12px;
    font-family: 'Menlo', 'Monaco', monospace;
    color: $primary;
  }

  :deep(pre) {
    background: rgba(23, 29, 28, 0.05);
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;

    :deep(code) {
      background: transparent;
      padding: 0;
      color: inherit;
    }
  }

  :deep(a) {
    color: $primary;
    text-decoration: underline;
  }

  :deep(blockquote) {
    margin: 8px 0;
    padding-left: 10px;
    border-left: 3px solid rgba(0, 106, 100, 0.35);
    color: $neutral-40;
  }
}

.view-original-btn {
  margin: 16px 16px 0;
  height: 44px;
  background: #006a64;
  color: #ffffff;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
}
</style>
