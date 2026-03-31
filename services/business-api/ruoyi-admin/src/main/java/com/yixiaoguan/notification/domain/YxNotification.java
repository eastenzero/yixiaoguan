package com.yixiaoguan.notification.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 站内通知实体 - 对应 yx_notification 表
 * 面向用户的站内消息推送（审批结果、主动推送等）
 */
public class YxNotification implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 接收人 ID */
    private Long userId;

    /** 通知标题 */
    private String title;

    /** 通知正文 */
    private String content;

    /**
     * 通知类型
     * 1-系统通知 2-审批通知 3-推送消息 4-申请结果
     */
    private Integer type;

    /** 关联业务类型（application / escalation / knowledge） */
    private String bizType;

    /** 关联业务记录 ID */
    private Long bizId;

    /** 是否已读 */
    private Boolean isRead;

    /** 阅读时间 */
    private Date readAt;

    /** 发送者 ID（系统发送时为 NULL） */
    private Long senderId;

    /** 关联的推送任务 ID */
    private Long pushTaskId;

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

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public Integer getType() { return type; }
    public void setType(Integer type) { this.type = type; }

    public String getBizType() { return bizType; }
    public void setBizType(String bizType) { this.bizType = bizType; }

    public Long getBizId() { return bizId; }
    public void setBizId(Long bizId) { this.bizId = bizId; }

    public Boolean getIsRead() { return isRead; }
    public void setIsRead(Boolean isRead) { this.isRead = isRead; }

    public Date getReadAt() { return readAt; }
    public void setReadAt(Date readAt) { this.readAt = readAt; }

    public Long getSenderId() { return senderId; }
    public void setSenderId(Long senderId) { this.senderId = senderId; }

    public Long getPushTaskId() { return pushTaskId; }
    public void setPushTaskId(Long pushTaskId) { this.pushTaskId = pushTaskId; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getSenderName() { return senderName; }
    public void setSenderName(String senderName) { this.senderName = senderName; }
}
