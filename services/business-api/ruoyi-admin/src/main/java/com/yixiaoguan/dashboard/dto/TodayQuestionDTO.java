package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;

/**
 * 今日提问项 DTO
 */
public class TodayQuestionDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 提问 ID */
    private Long id;

    /** 时间（HH:mm 格式） */
    private String time;

    /** 学生姓名 */
    private String studentName;

    /** 学生班级 */
    private String studentClass;

    /** 头像颜色 */
    private String avatarColor;

    /** 问题标题 */
    private String title;

    /** 问题分类 */
    private String category;

    /** AI 处理状态：resolved / pending / handled */
    private String aiStatus;

    /** AI 状态文本 */
    private String aiText;

    /** 是否需要处理 */
    private boolean needHandle;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getStudentName() {
        return studentName;
    }

    public void setStudentName(String studentName) {
        this.studentName = studentName;
    }

    public String getStudentClass() {
        return studentClass;
    }

    public void setStudentClass(String studentClass) {
        this.studentClass = studentClass;
    }

    public String getAvatarColor() {
        return avatarColor;
    }

    public void setAvatarColor(String avatarColor) {
        this.avatarColor = avatarColor;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getAiStatus() {
        return aiStatus;
    }

    public void setAiStatus(String aiStatus) {
        this.aiStatus = aiStatus;
    }

    public String getAiText() {
        return aiText;
    }

    public void setAiText(String aiText) {
        this.aiText = aiText;
    }

    public boolean isNeedHandle() {
        return needHandle;
    }

    public void setNeedHandle(boolean needHandle) {
        this.needHandle = needHandle;
    }
}
