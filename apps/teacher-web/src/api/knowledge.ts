/**
 * 知识库 API 模块
 * 对应后端: KnowledgeEntryController, KnowledgeCategoryController, etc.
 * 
 * ⚠️ 字段适配说明：
 * 后端字段名 → 前端字段名映射：
 * - hitCount → likeCount (含义相同，命名不同)
 * - keywords/reviewerId/reviewerName → 后端暂无，mock 处理
 */
import request from '@/utils/request'
import type { ApiResponse, PageParams, PageResult } from './types'

// ===== 状态枚举 =====
export enum KnowledgeStatus {
  DRAFT = 0,      // 草稿
  PENDING = 1,    // 待审核
  PUBLISHED = 2,  // 已发布
  OFFLINE = 3,    // 已下线
  REJECTED = 4    // 已驳回
}

// ===== 类型定义 =====

/** 后端原始知识条目结构 */
interface RawKnowledgeEntry {
  id: number
  categoryId: number
  categoryName: string
  title: string
  content: string
  summary?: string
  status: number
  viewCount: number
  hitCount: number           // 后端字段：AI命中次数，映射到 likeCount
  authorId: number
  authorName: string
  publishedAt?: string
  createdAt: string
  updatedAt: string
  // 后端暂无可选字段
  keywords?: string
  reviewerId?: number
  reviewerName?: string
  // 扩展字段
  tags?: Array<{
    id: number
    name: string
    color: string
  }>
}

/** 知识条目（前端标准化结构） */
export interface KnowledgeEntry {
  id: number
  categoryId: number
  categoryName: string
  title: string
  content: string
  summary?: string
  keywords?: string
  status: KnowledgeStatus
  viewCount: number
  likeCount: number          // 映射自后端的 hitCount
  authorId: number
  authorName: string
  reviewerId?: number
  reviewerName?: string
  publishedAt?: string
  createdAt: string
  updatedAt: string
}

/** 知识分类 */
export interface KnowledgeCategory {
  id: number
  parentId: number
  name: string
  description?: string
  sortOrder: number
  entryCount: number
  children?: KnowledgeCategory[]
}

/** 知识标签 */
export interface KnowledgeTag {
  id: number
  name: string
  color: string
  usageCount: number
}

/** 快捷入口配置 */
export interface QuickLink {
  id: number
  name: string
  icon: string
  url: string
  bgColor: string
  color: string
  sortOrder: number
}

// ===== 字段适配器 =====

/**
 * 适配单条知识条目数据
 * 将后端字段名转换为前端标准字段名
 */
function adaptKnowledgeEntry(raw: RawKnowledgeEntry): KnowledgeEntry {
  return {
    id: raw.id,
    categoryId: raw.categoryId,
    categoryName: raw.categoryName,
    title: raw.title,
    content: raw.content,
    summary: raw.summary,
    keywords: raw.keywords,           // 后端暂无，保持透传
    status: raw.status as KnowledgeStatus,
    viewCount: raw.viewCount,
    likeCount: raw.hitCount,          // 字段映射：hitCount → likeCount
    authorId: raw.authorId,
    authorName: raw.authorName,
    reviewerId: raw.reviewerId,       // 后端暂无，保持透传
    reviewerName: raw.reviewerName,   // 后端暂无，保持透传
    publishedAt: raw.publishedAt,
    createdAt: raw.createdAt,
    updatedAt: raw.updatedAt
  }
}

/**
 * 适配分页结果
 */
function adaptPageResult<T, R>(
  raw: PageResult<T>,
  adapter: (item: T) => R
): PageResult<R> {
  return {
    total: raw.total,
    rows: raw.rows.map(adapter),
    pageNum: raw.pageNum,
    pageSize: raw.pageSize
  }
}

// ===== 接口函数 =====

/**
 * 获取知识库快捷入口
 */
export function getQuickLinks() {
  return request({
    url: '/api/v1/quicklinks',
    method: 'get'
  }) as Promise<ApiResponse<QuickLink[]>>
}

/**
 * 获取知识分类列表
 */
export function getKnowledgeCategories() {
  return request({
    url: '/api/v1/knowledge/categories',
    method: 'get'
  }) as Promise<ApiResponse<KnowledgeCategory[]>>
}

/**
 * 获取知识条目列表
 */
export async function getKnowledgeEntries(
  categoryId?: number, 
  status?: KnowledgeStatus, 
  title?: string, 
  params?: PageParams
): Promise<ApiResponse<PageResult<KnowledgeEntry>>> {
  const res = await request({
    url: '/api/v1/knowledge/entries',
    method: 'get',
    params: {
      categoryId,
      status,
      title,
      ...params
    }
  }) as ApiResponse<PageResult<RawKnowledgeEntry>>

  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptPageResult(res.data, adaptKnowledgeEntry)
    }
  }

  return res as unknown as ApiResponse<PageResult<KnowledgeEntry>>
}

/**
 * 获取知识条目详情
 */
export async function getKnowledgeEntry(id: number): Promise<ApiResponse<KnowledgeEntry>> {
  const res = await request({
    url: `/api/v1/knowledge/entries/${id}`,
    method: 'get'
  }) as ApiResponse<RawKnowledgeEntry>

  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptKnowledgeEntry(res.data)
    }
  }

  return res as unknown as ApiResponse<KnowledgeEntry>
}

/**
 * 保存草稿
 */
export function saveKnowledgeDraft(entry: Partial<KnowledgeEntry>) {
  // 字段反向映射：likeCount → hitCount
  const rawEntry: Partial<RawKnowledgeEntry> = {
    ...entry,
    hitCount: entry.likeCount
  }
  
  return request({
    url: '/api/v1/knowledge/entries/draft',
    method: 'post',
    data: rawEntry
  }) as Promise<ApiResponse<KnowledgeEntry>>
}

/**
 * 提交审核
 */
export function submitKnowledgeForReview(id: number) {
  return request({
    url: `/api/v1/knowledge/entries/${id}/submit`,
    method: 'post'
  }) as Promise<ApiResponse<null>>
}

/**
 * 下线条目
 */
export function offlineKnowledgeEntry(id: number) {
  return request({
    url: `/api/v1/knowledge/entries/${id}/offline`,
    method: 'post'
  }) as Promise<ApiResponse<null>>
}

/**
 * 删除条目
 */
export function deleteKnowledgeEntry(id: number) {
  return request({
    url: `/api/v1/knowledge/entries/${id}`,
    method: 'delete'
  }) as Promise<ApiResponse<null>>
}
