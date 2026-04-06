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

export function getKnowledgeEntryFull(entryId: string): Promise<KnowledgeEntryFull | null> {
  return new Promise((resolve) => {
    uni.request({
      url: '/api/knowledge/entries/' + encodeURIComponent(entryId),
      method: 'GET',
      success: (res: any) => {
        if (res.statusCode === 200 && res.data?.code === 0) {
          resolve(res.data.data as KnowledgeEntryFull)
        } else {
          resolve(null)
        }
      },
      fail: () => resolve(null),
    })
  })
}
