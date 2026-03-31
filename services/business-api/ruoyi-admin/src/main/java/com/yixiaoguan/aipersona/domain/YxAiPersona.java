package com.yixiaoguan.aipersona.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * AI 人设配置实体 - 对应 yx_ai_persona 表
 * 存储导员自定义的 AI 名称、头像、语气风格与 Prompt
 */
public class YxAiPersona implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 所属教师 ID（NULL = 系统默认人设） */
    private Long teacherId;

    /** AI 显示名称 */
    private String name;

    /** AI 头像 URL */
    private String avatarUrl;

    /** 开场白 / 欢迎语 */
    private String greeting;

    /** 系统提示词（Prompt） */
    private String systemPrompt;

    /** 语气风格（亲切 / 正式 / 活泼） */
    private String toneStyle;

    /** 是否为系统默认人设 */
    private Boolean isDefault;

    /**
     * 状态
     * 0-停用 1-启用
     */
    private Integer status;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 教师姓名 */
    private String teacherName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getTeacherId() { return teacherId; }
    public void setTeacherId(Long teacherId) { this.teacherId = teacherId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getAvatarUrl() { return avatarUrl; }
    public void setAvatarUrl(String avatarUrl) { this.avatarUrl = avatarUrl; }

    public String getGreeting() { return greeting; }
    public void setGreeting(String greeting) { this.greeting = greeting; }

    public String getSystemPrompt() { return systemPrompt; }
    public void setSystemPrompt(String systemPrompt) { this.systemPrompt = systemPrompt; }

    public String getToneStyle() { return toneStyle; }
    public void setToneStyle(String toneStyle) { this.toneStyle = toneStyle; }

    public Boolean getIsDefault() { return isDefault; }
    public void setIsDefault(Boolean isDefault) { this.isDefault = isDefault; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getTeacherName() { return teacherName; }
    public void setTeacherName(String teacherName) { this.teacherName = teacherName; }
}
