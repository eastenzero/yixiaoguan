import { get } from '@/utils/request'
import type { KnowledgeEntry } from '@/types/knowledge'

/**
 * 获取知识条目详情
 */
export function getKnowledgeEntryDetail(id: number): Promise<KnowledgeEntry> {
  return get(`/api/v1/knowledge/entries/${id}`)
}
