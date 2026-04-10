import { request } from '@/utils/request'

export const getKnowledgeEntryFull = (entryId: string | number) => {
  return request({ url: `/api/knowledge/entries/${entryId}`, method: 'GET' })
}
