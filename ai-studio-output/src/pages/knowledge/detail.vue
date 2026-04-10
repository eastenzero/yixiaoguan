<template>
  <view class="knowledge-detail-page" v-if="detail">
    <view class="hero-card">
      <view class="header-info">
        <text class="entry-id">编号: {{ detail.id || entryId }}</text>
        <view class="score-badge" v-if="score">
          相关度 {{ Math.round(Number(score) * 100) }}%
        </view>
      </view>
      <text class="title">{{ detail.title || title }}</text>
      <view class="category" v-if="detail.category">
        <text class="icon">📁</text>
        <text>{{ detail.category }}</text>
      </view>
    </view>

    <view class="tags-section" v-if="detail.tags && detail.tags.length">
      <view class="tag-pill" v-for="tag in detail.tags" :key="tag">
        {{ tag }}
      </view>
    </view>

    <view class="content-section">
      <view class="markdown-body" v-html="renderMarkdown(detail.content || summary)"></view>
    </view>

    <view class="bottom-bar" v-if="materialFileUrl">
      <button class="view-pdf-btn" @click="viewPdf">
        <text class="icon">📄</text>
        <text>查看原始文件</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import MarkdownIt from 'markdown-it'
import { getKnowledgeEntryFull } from '@/api/knowledge'

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true
})

const renderMarkdown = (content: string) => {
  if (!content) return ''
  return md.render(content)
}

const detail = ref<any>(null)
const entryId = ref('')
const title = ref('')
const summary = ref('')
const score = ref('')
const materialFileUrl = ref('')

onLoad((options: any) => {
  if (options.entry_id) entryId.value = decodeURIComponent(options.entry_id)
  if (options.title) title.value = decodeURIComponent(options.title)
  if (options.summary) summary.value = decodeURIComponent(options.summary)
  if (options.score) score.value = options.score
  if (options.material_file_url) materialFileUrl.value = decodeURIComponent(options.material_file_url)

  if (entryId.value) {
    loadDetail(entryId.value)
  } else {
    // Fallback to passed data
    detail.value = {
      title: title.value,
      content: summary.value
    }
  }
})

const loadDetail = async (id: string) => {
  try {
    const res = await getKnowledgeEntryFull(id)
    detail.value = res.data
  } catch (error) {
    console.error('Failed to load knowledge detail', error)
    // Fallback to passed data on error
    if (!detail.value) {
      detail.value = {
        title: title.value,
        content: summary.value
      }
    }
  }
}

const viewPdf = () => {
  if (materialFileUrl.value) {
    uni.navigateTo({
      url: `/pages/viewer/pdf?url=${encodeURIComponent(materialFileUrl.value)}&title=${encodeURIComponent(title.value || '原始文件')}`
    })
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.knowledge-detail-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

.hero-card {
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  padding: 48rpx $spacing-md 64rpx;
  color: $text-inverse;
  border-radius: 0 0 $radius-lg $radius-lg;
  box-shadow: $elevation-2;

  .header-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-sm;

    .entry-id {
      font-size: 24rpx;
      opacity: 0.8;
    }

    .score-badge {
      background: rgba(255, 255, 255, 0.2);
      padding: 4rpx 16rpx;
      border-radius: $radius-chip;
      font-size: 24rpx;
      border: 1px solid rgba(255, 255, 255, 0.4);
    }
  }

  .title {
    font-size: 40rpx;
    font-weight: 700;
    line-height: 1.4;
    margin-bottom: $spacing-sm;
    display: block;
  }

  .category {
    display: flex;
    align-items: center;
    gap: 8rpx;
    font-size: 28rpx;
    opacity: 0.9;
  }
}

.tags-section {
  padding: $spacing-md;
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;

  .tag-pill {
    background: $primary-95;
    color: $primary-40;
    padding: 8rpx 24rpx;
    border-radius: $radius-chip;
    font-size: 24rpx;
    border: 1px solid $primary-80;
  }
}

.content-section {
  padding: $spacing-md;
  background: $bg-card;
  margin: 0 $spacing-md;
  border-radius: $radius-lg;
  box-shadow: $elevation-1;
  min-height: 400rpx;
}

.markdown-body {
  font-size: 30rpx;
  line-height: 1.8;
  color: $text-primary;

  :deep(p) { margin: 0 0 16rpx 0; }
  :deep(strong) { font-weight: 600; color: $primary-40; }
  :deep(h1), :deep(h2), :deep(h3) { font-weight: 600; margin: 24rpx 0 16rpx; }
  :deep(ul), :deep(ol) { padding-left: 40rpx; margin-bottom: 16rpx; }
  :deep(li) { margin-bottom: 8rpx; }
  :deep(code) {
    background: rgba(124, 58, 237, 0.1);
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
    color: $primary-40;
  }
  :deep(pre) {
    background: $bg-secondary;
    padding: 24rpx;
    border-radius: 16rpx;
    overflow-x: auto;
    margin-bottom: 16rpx;
  }
  :deep(blockquote) {
    border-left: 8rpx solid $primary-40;
    padding-left: 16rpx;
    color: $text-secondary;
    background: $primary-95;
    padding: 16rpx;
    border-radius: 0 $radius-md $radius-md 0;
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: $bg-card;
  padding: $spacing-sm $spacing-md;
  padding-bottom: calc($spacing-sm + env(safe-area-inset-bottom));
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);

  .view-pdf-btn {
    height: 88rpx;
    border-radius: $radius-pill;
    background: linear-gradient(90deg, $primary-40 0%, $primary-50 100%);
    color: $text-inverse;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12rpx;

    &:active {
      transform: scale(0.98);
    }
  }
}
</style>
