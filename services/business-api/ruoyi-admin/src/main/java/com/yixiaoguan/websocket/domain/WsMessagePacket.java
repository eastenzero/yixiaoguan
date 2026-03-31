package com.yixiaoguan.websocket.domain;

/**
 * WebSocket 统一指令帧 POJO
 * 客户端（学生/教师）和服务端之间通信的标准数据包格式，使用 JSON 序列化传输。
 *
 * 指令类型（type）约定：
 *   TEACHER_JOIN    - 教师加入会话（教师→服务端）
 *   TEACHER_LEAVE   - 教师离开会话（教师→服务端）
 *   CHAT_MESSAGE    - 聊天消息（双向）
 *   SYSTEM_NOTIFY   - 系统通知（服务端→客户端，不需要客户端回传）
 *   PING            - 心跳保活（客户端→服务端）
 *   PONG            - 心跳应答（服务端→客户端）
 */
public class WsMessagePacket {

    /** 指令类型（必填） */
    private String type;

    /** 关联的会话 ID */
    private Long conversationId;

    /** 消息内容（CHAT_MESSAGE / SYSTEM_NOTIFY 时使用） */
    private String content;

    /**
     * 消息内容类型：1-纯文本 2-Markdown 3-卡片 4-系统提示
     * 默认 1
     */
    private Integer messageType;

    /** 发送者用户 ID（服务端填充，客户端上行时可不填） */
    private Long senderId;

    /** 发送者真实姓名（服务端填充，方便前端直接展示） */
    private String senderName;

    /**
     * 发送者类型：1-学生 2-AI 3-教师 4-系统
     * 服务端根据鉴权结果自动填充
     */
    private Integer senderType;

    /** 关联的上游消息 ID（回复场景） */
    private Long parentMessageId;

    /** 服务端下行的消息数据库 ID（存库后填充，客户端可用于幂等判断） */
    private Long messageId;

    /** 附加信息（如 SYSTEM_NOTIFY 带的业务码，可扩展） */
    private String extra;

    // ===== Getter / Setter =====

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public Long getConversationId() { return conversationId; }
    public void setConversationId(Long conversationId) { this.conversationId = conversationId; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public Integer getMessageType() { return messageType; }
    public void setMessageType(Integer messageType) { this.messageType = messageType; }

    public Long getSenderId() { return senderId; }
    public void setSenderId(Long senderId) { this.senderId = senderId; }

    public String getSenderName() { return senderName; }
    public void setSenderName(String senderName) { this.senderName = senderName; }

    public Integer getSenderType() { return senderType; }
    public void setSenderType(Integer senderType) { this.senderType = senderType; }

    public Long getParentMessageId() { return parentMessageId; }
    public void setParentMessageId(Long parentMessageId) { this.parentMessageId = parentMessageId; }

    public Long getMessageId() { return messageId; }
    public void setMessageId(Long messageId) { this.messageId = messageId; }

    public String getExtra() { return extra; }
    public void setExtra(String extra) { this.extra = extra; }
}
