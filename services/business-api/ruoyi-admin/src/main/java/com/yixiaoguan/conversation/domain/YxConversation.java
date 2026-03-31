package com.yixiaoguan.conversation.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 会话实体 - 对应 yx_conversation 表
 * 管理学生与 AI/教师的对话会话，一个学生可有多个会话
 */
public class YxConversation implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 所属学生 ID */
    private Long userId;

    /** 会话标题（可由 AI 自动生成） */
    private String title;

    /**
     * 会话状态
     * 0-已关闭 1-进行中 2-教师已介入
     */
    private Integer status;

    /** 当前介入的教师 ID */
    private Long teacherId;

    /** 教师介入时间 */
    private Date teacherJoinedAt;

    /** 最后消息时间 */
    private Date lastMessageAt;

    /** 消息总数 */
    private Integer messageCount;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 学生真实姓名（JOIN yx_user） */
    private String userRealName;

    /** 教师真实姓名（JOIN yx_user） */
    private String teacherRealName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Long getTeacherId() { return teacherId; }
    public void setTeacherId(Long teacherId) { this.teacherId = teacherId; }

    public Date getTeacherJoinedAt() { return teacherJoinedAt; }
    public void setTeacherJoinedAt(Date teacherJoinedAt) { this.teacherJoinedAt = teacherJoinedAt; }

    public Date getLastMessageAt() { return lastMessageAt; }
    public void setLastMessageAt(Date lastMessageAt) { this.lastMessageAt = lastMessageAt; }

    public Integer getMessageCount() { return messageCount; }
    public void setMessageCount(Integer messageCount) { this.messageCount = messageCount; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getUserRealName() { return userRealName; }
    public void setUserRealName(String userRealName) { this.userRealName = userRealName; }

    public String getTeacherRealName() { return teacherRealName; }
    public void setTeacherRealName(String teacherRealName) { this.teacherRealName = teacherRealName; }
}
