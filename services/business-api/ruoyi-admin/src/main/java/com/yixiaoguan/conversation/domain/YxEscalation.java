package com.yixiaoguan.conversation.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 问题上报工单实体 - 对应 yx_escalation 表
 * AI 无法回答的问题上报给教师处理的工单
 */
public class YxEscalation implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 来源会话 ID */
    private Long conversationId;

    /** 触发上报的消息 ID */
    private Long messageId;

    /** 提问学生 ID */
    private Long studentId;

    /** 分配给的教师 ID */
    private Long teacherId;

    /** 问题摘要 */
    private String questionSummary;

    /**
     * 工单状态
     * 0-待处理 1-处理中 2-已解决 3-已关闭 4-已转知识库
     */
    private Integer status;

    /**
     * 优先级
     * 0-低 1-中 2-高
     */
    private Integer priority;

    /**
     * 触发方式
     * 1-学生主动呼叫 2-AI 判断上报
     */
    private Integer triggerType;

    /** 教师回复内容 */
    private String teacherReply;

    /** 解决时间 */
    private Date resolvedAt;

    /** 转为知识条目后的关联 ID */
    private Long knowledgeEntryId;

    /** 备注 */
    private String remark;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 学生真实姓名（JOIN yx_user） */
    private String studentRealName;

    /** 教师真实姓名（JOIN yx_user） */
    private String teacherRealName;

    /** 学生班级（JOIN yx_user） */
    private String studentClassName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getConversationId() { return conversationId; }
    public void setConversationId(Long conversationId) { this.conversationId = conversationId; }

    public Long getMessageId() { return messageId; }
    public void setMessageId(Long messageId) { this.messageId = messageId; }

    public Long getStudentId() { return studentId; }
    public void setStudentId(Long studentId) { this.studentId = studentId; }

    public Long getTeacherId() { return teacherId; }
    public void setTeacherId(Long teacherId) { this.teacherId = teacherId; }

    public String getQuestionSummary() { return questionSummary; }
    public void setQuestionSummary(String questionSummary) { this.questionSummary = questionSummary; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Integer getPriority() { return priority; }
    public void setPriority(Integer priority) { this.priority = priority; }

    public Integer getTriggerType() { return triggerType; }
    public void setTriggerType(Integer triggerType) { this.triggerType = triggerType; }

    public String getTeacherReply() { return teacherReply; }
    public void setTeacherReply(String teacherReply) { this.teacherReply = teacherReply; }

    public Date getResolvedAt() { return resolvedAt; }
    public void setResolvedAt(Date resolvedAt) { this.resolvedAt = resolvedAt; }

    public Long getKnowledgeEntryId() { return knowledgeEntryId; }
    public void setKnowledgeEntryId(Long knowledgeEntryId) { this.knowledgeEntryId = knowledgeEntryId; }

    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getStudentRealName() { return studentRealName; }
    public void setStudentRealName(String studentRealName) { this.studentRealName = studentRealName; }

    public String getTeacherRealName() { return teacherRealName; }
    public void setTeacherRealName(String teacherRealName) { this.teacherRealName = teacherRealName; }

    public String getStudentClassName() { return studentClassName; }
    public void setStudentClassName(String studentClassName) { this.studentClassName = studentClassName; }
}
