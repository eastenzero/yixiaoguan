package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;

/**
 * 待审批项 DTO
 */
public class PendingApprovalDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 审批 ID */
    private String id;

    /** 审批类型 */
    private String type;

    /** 标题 */
    private String title;

    /** 时间范围 */
    private String timeRange;

    /** 是否紧急 */
    private boolean isUrgent;

    /** 剩余时间提示 */
    private String remainingTime;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getTimeRange() {
        return timeRange;
    }

    public void setTimeRange(String timeRange) {
        this.timeRange = timeRange;
    }

    public boolean isUrgent() {
        return isUrgent;
    }

    public void setUrgent(boolean urgent) {
        isUrgent = urgent;
    }

    public String getRemainingTime() {
        return remainingTime;
    }

    public void setRemainingTime(String remainingTime) {
        this.remainingTime = remainingTime;
    }
}
