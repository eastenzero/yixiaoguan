package com.yixiaoguan.knowledge.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 知识审核记录实体 - 对应 yx_knowledge_review 表
 * 每次审核操作生成一条记录（一期为一级审核）
 */
public class YxKnowledgeReview implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 审核的条目 ID */
    private Long entryId;

    /** 审核人 ID */
    private Long reviewerId;

    /**
     * 审核动作
     * 1-通过 2-拒绝 3-退回修改
     */
    private Integer action;

    /** 审核意见 */
    private String opinion;

    /** 审核时的条目版本号 */
    private Integer entryVersion;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 审核人真实姓名 */
    private String reviewerName;

    /** 知识标题 */
    private String entryTitle;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getEntryId() { return entryId; }
    public void setEntryId(Long entryId) { this.entryId = entryId; }

    public Long getReviewerId() { return reviewerId; }
    public void setReviewerId(Long reviewerId) { this.reviewerId = reviewerId; }

    public Integer getAction() { return action; }
    public void setAction(Integer action) { this.action = action; }

    public String getOpinion() { return opinion; }
    public void setOpinion(String opinion) { this.opinion = opinion; }

    public Integer getEntryVersion() { return entryVersion; }
    public void setEntryVersion(Integer entryVersion) { this.entryVersion = entryVersion; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getReviewerName() { return reviewerName; }
    public void setReviewerName(String reviewerName) { this.reviewerName = reviewerName; }

    public String getEntryTitle() { return entryTitle; }
    public void setEntryTitle(String entryTitle) { this.entryTitle = entryTitle; }
}
