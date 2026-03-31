package com.yixiaoguan.pushtask.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 主动推送任务实体 - 对应 yx_push_task 表
 * 教师手动创建的群发推送任务（一期仅支持手动发送）
 */
public class YxPushTask implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 推送标题 */
    private String title;

    /** 推送内容 */
    private String content;

    /**
     * 目标类型
     * 1-全体学生 2-指定班级 3-指定用户
     */
    private Integer targetType;

    /** 目标筛选条件（JSON，如班级列表、用户 ID 列表） */
    private String targetFilter;

    /**
     * 状态
     * 0-草稿 1-已发送 2-已取消
     */
    private Integer status;

    /** 发起教师 ID */
    private Long senderId;

    /** 实际发送时间 */
    private Date sentAt;

    /** 接收人数 */
    private Integer recipientCount;

    /** 已读人数 */
    private Integer readCount;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 发送者姓名 */
    private String senderName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public Integer getTargetType() { return targetType; }
    public void setTargetType(Integer targetType) { this.targetType = targetType; }

    public String getTargetFilter() { return targetFilter; }
    public void setTargetFilter(String targetFilter) { this.targetFilter = targetFilter; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Long getSenderId() { return senderId; }
    public void setSenderId(Long senderId) { this.senderId = senderId; }

    public Date getSentAt() { return sentAt; }
    public void setSentAt(Date sentAt) { this.sentAt = sentAt; }

    public Integer getRecipientCount() { return recipientCount; }
    public void setRecipientCount(Integer recipientCount) { this.recipientCount = recipientCount; }

    public Integer getReadCount() { return readCount; }
    public void setReadCount(Integer readCount) { this.readCount = readCount; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getSenderName() { return senderName; }
    public void setSenderName(String senderName) { this.senderName = senderName; }
}
