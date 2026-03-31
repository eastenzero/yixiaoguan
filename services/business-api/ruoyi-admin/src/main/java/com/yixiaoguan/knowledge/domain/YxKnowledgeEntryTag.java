package com.yixiaoguan.knowledge.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 知识条目-标签关联实体 - 对应 yx_knowledge_entry_tag 表
 */
public class YxKnowledgeEntryTag implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 知识条目 ID */
    private Long entryId;

    /** 标签 ID */
    private Long tagId;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 标签名称 */
    private String tagName;

    // ===== Getter / Setter =====

    public Long getEntryId() { return entryId; }
    public void setEntryId(Long entryId) { this.entryId = entryId; }

    public Long getTagId() { return tagId; }
    public void setTagId(Long tagId) { this.tagId = tagId; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getTagName() { return tagName; }
    public void setTagName(String tagName) { this.tagName = tagName; }
}
