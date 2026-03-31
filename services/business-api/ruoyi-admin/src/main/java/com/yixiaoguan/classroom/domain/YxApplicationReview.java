package com.yixiaoguan.classroom.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 申请审批记录实体 - 对应 yx_application_review 表
 * 教师对空教室申请的审批操作记录
 */
public class YxApplicationReview implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 申请单 ID */
    private Long applicationId;

    /** 审批人 ID */
    private Long reviewerId;

    /**
     * 审批动作
     * 1-通过 2-拒绝
     */
    private Integer action;

    /** 审批意见 */
    private String opinion;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 审批人真实姓名 */
    private String reviewerName;

    /** 申请人真实姓名（JOIN application -> user） */
    private String applicantName;

    /** 教学楼名称 */
    private String building;

    /** 教室编号 */
    private String roomNumber;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getApplicationId() { return applicationId; }
    public void setApplicationId(Long applicationId) { this.applicationId = applicationId; }

    public Long getReviewerId() { return reviewerId; }
    public void setReviewerId(Long reviewerId) { this.reviewerId = reviewerId; }

    public Integer getAction() { return action; }
    public void setAction(Integer action) { this.action = action; }

    public String getOpinion() { return opinion; }
    public void setOpinion(String opinion) { this.opinion = opinion; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getReviewerName() { return reviewerName; }
    public void setReviewerName(String reviewerName) { this.reviewerName = reviewerName; }

    public String getApplicantName() { return applicantName; }
    public void setApplicantName(String applicantName) { this.applicantName = applicantName; }

    public String getBuilding() { return building; }
    public void setBuilding(String building) { this.building = building; }

    public String getRoomNumber() { return roomNumber; }
    public void setRoomNumber(String roomNumber) { this.roomNumber = roomNumber; }
}
