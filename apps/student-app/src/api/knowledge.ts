import { request } from '@/utils/request'
import type { KnowledgeEntry } from '@/types/knowledge'

/**
 * 获取知识条目详情
 * 静默处理 404 错误，返回 null 让调用方展示 fallback
 */
export async function getKnowledgeEntryDetail(id: number): Promise<KnowledgeEntry | null> {
  try {
    const entry = await request<KnowledgeEntry>({
      url: `/api/v1/knowledge/entries/${id}`,
      method: 'GET'
    })
    return entry
  } catch (error: any) {
    // 静默处理 404，让 detail.vue 展示 fallback
    if (error?.message?.includes('404') || error?.message?.includes('资源不存在')) {
      return null
    }
    // 其他错误继续抛出
    throw error
  }
}
