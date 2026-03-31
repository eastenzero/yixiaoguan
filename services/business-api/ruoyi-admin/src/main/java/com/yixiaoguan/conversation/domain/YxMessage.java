package com.yixiaoguan.conversation.domain;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 消息实体 - 对应 yx_message 表
 * 会话中的每条消息，区分学生/AI/教师/系统四种发送者身份
 */
public class YxMessage implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 所属会话 ID */
    private Long conversationId;

    /**
     * 发送者类型
     * 1-学生 2-AI 3-教师 4-系统
     */
    private Integer senderType;

    /** 发送者用户 ID（AI / 系统时为 NULL） */
    private Long senderId;

    /** 消息内容 */
    private String content;

    /**
     * 消息内容类型
     * 1-纯文本 2-富文本/Markdown 3-卡片 4-系统提示
     */
    private Integer messageType;

    /** 关联的上游消息 ID（如学生提问 → AI 回答关联学生的那条） */
    private Long parentMessageId;

    /** AI 回答的置信度（0.0000~1.0000） */
    private BigDecimal aiConfidence;

    /** AI 命中的知识条目 ID 列表（JSON 数组字符串） */
    private String aiSourceEntryIds;

    /** AI 推荐的快捷链接 ID 列表（JSON 数组字符串） */
    private String aiSourceLinkIds;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 发送者真实姓名（JOIN yx_user） */
    private String senderRealName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getConversationId() { return conversationId; }
    public void setConversationId(Long conversationId) { this.conversationId = conversationId; }

    public Integer getSenderType() { return senderType; }
    public void setSenderType(Integer senderType) { this.senderType = senderType; }

    public Long getSenderId() { return senderId; }
    public void setSenderId(Long senderId) { this.senderId = senderId; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public Integer getMessageType() { return messageType; }
    public void setMessageType(Integer messageType) { this.messageType = messageType; }

    public Long getParentMessageId() { return parentMessageId; }
    public void setParentMessageId(Long parentMessageId) { this.parentMessageId = parentMessageId; }

    public BigDecimal getAiConfidence() { return aiConfidence; }
    public void setAiConfidence(BigDecimal aiConfidence) { this.aiConfidence = aiConfidence; }

    public String getAiSourceEntryIds() { return aiSourceEntryIds; }
    public void setAiSourceEntryIds(String aiSourceEntryIds) { this.aiSourceEntryIds = aiSourceEntryIds; }

    public String getAiSourceLinkIds() { return aiSourceLinkIds; }
    public void setAiSourceLinkIds(String aiSourceLinkIds) { this.aiSourceLinkIds = aiSourceLinkIds; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getSenderRealName() { return senderRealName; }
    public void setSenderRealName(String senderRealName) { this.senderRealName = senderRealName; }
}
