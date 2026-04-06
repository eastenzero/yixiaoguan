import { request } from '@/utils/request'

export interface KnowledgeEntryFull {
  entry_id: string
  title: string
  content: string
  material_file_url: string
  material_title: string
  page_start?: string | number
  page_end?: string | number
  metadata?: Record<string, string>
}

export async function getKnowledgeEntryFull(entryId: string): Promise<KnowledgeEntryFull | null> {
  try {
    const res = await request.get('/api/knowledge/entries/' + encodeURIComponent(entryId))
    if (res.data?.code === 0) {
      return res.data.data as KnowledgeEntryFull
    }
    return null
  } catch {
    return null
  }
}
