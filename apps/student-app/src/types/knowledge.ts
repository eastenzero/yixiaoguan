export interface KnowledgeTag {
  id: number
  name: string
}

export interface KnowledgeEntry {
  id: number
  categoryId?: number
  categoryName?: string
  title: string
  content?: string
  summary?: string
  status?: number
  version?: number
  sourceId?: number
  sourceFileName?: string
  authorId?: number
  authorName?: string
  publishedAt?: string
  expiredAt?: string
  viewCount?: number
  hitCount?: number
  remark?: string
  createdAt?: string
  updatedAt?: string
  tags?: KnowledgeTag[]
  tagIds?: number[]
}
