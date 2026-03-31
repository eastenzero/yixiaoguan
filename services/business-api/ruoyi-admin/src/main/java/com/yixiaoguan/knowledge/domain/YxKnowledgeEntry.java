package com.yixiaoguan.knowledge.domain;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

/**
 * 知识条目实体 - 对应 yx_knowledge_entry 表
 * 标准化知识内容，拥有完整的生命周期状态
 */
public class YxKnowledgeEntry implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 所属分类 ID */
    private Long categoryId;

    /** 知识标题 */
    private String title;

    /** 知识内容（Markdown 格式） */
    private String content;

    /** 摘要（用于搜索结果展示） */
    private String summary;

    /**
     * 状态
     * 0-草稿 1-待审核 2-已发布 3-已下线 4-审核拒绝
     */
    private Integer status;

    /** 版本号（每次编辑 +1） */
    private Integer version;

    /** 关联的来源记录 ID */
    private Long sourceId;

    /** 创建者 ID */
    private Long authorId;

    /** 发布时间 */
    private Date publishedAt;

    /** 过期时间（可选） */
    private Date expiredAt;

    /** 被查看次数 */
    private Integer viewCount;

    /** AI 问答命中次数 */
    private Integer hitCount;

    /** 备注 */
    private String remark;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 分类名称 */
    private String categoryName;

    /** 创建者真实姓名 */
    private String authorName;

    /** 来源文件名 */
    private String sourceFileName;

    /** 关联标签列表 */
    private List<YxKnowledgeTag> tags;

    /** 关联标签 ID 列表（用于入参/出参） */
    private List<Long> tagIds;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getCategoryId() { return categoryId; }
    public void setCategoryId(Long categoryId) { this.categoryId = categoryId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getSummary() { return summary; }
    public void setSummary(String summary) { this.summary = summary; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }

    public Long getSourceId() { return sourceId; }
    public void setSourceId(Long sourceId) { this.sourceId = sourceId; }

    public Long getAuthorId() { return authorId; }
    public void setAuthorId(Long authorId) { this.authorId = authorId; }

    public Date getPublishedAt() { return publishedAt; }
    public void setPublishedAt(Date publishedAt) { this.publishedAt = publishedAt; }

    public Date getExpiredAt() { return expiredAt; }
    public void setExpiredAt(Date expiredAt) { this.expiredAt = expiredAt; }

    public Integer getViewCount() { return viewCount; }
    public void setViewCount(Integer viewCount) { this.viewCount = viewCount; }

    public Integer getHitCount() { return hitCount; }
    public void setHitCount(Integer hitCount) { this.hitCount = hitCount; }

    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getCategoryName() { return categoryName; }
    public void setCategoryName(String categoryName) { this.categoryName = categoryName; }

    public String getAuthorName() { return authorName; }
    public void setAuthorName(String authorName) { this.authorName = authorName; }

    public String getSourceFileName() { return sourceFileName; }
    public void setSourceFileName(String sourceFileName) { this.sourceFileName = sourceFileName; }

    public List<YxKnowledgeTag> getTags() { return tags; }
    public void setTags(List<YxKnowledgeTag> tags) { this.tags = tags; }

    public List<Long> getTagIds() { return tagIds; }
    public void setTagIds(List<Long> tagIds) { this.tagIds = tagIds; }
}
