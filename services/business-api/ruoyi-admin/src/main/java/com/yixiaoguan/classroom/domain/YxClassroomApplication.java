package com.yixiaoguan.classroom.domain;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

/**
 * 空教室申请实体 - 对应 yx_classroom_application 表
 * 学生提交的空教室使用申请
 */
public class YxClassroomApplication implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 申请人 ID */
    private Long applicantId;

    /** 申请的教室 ID */
    private Long classroomId;

    /** 使用日期 */
    private Date applyDate;

    /** 开始时间 */
    private Date startTime;

    /** 结束时间 */
    private Date endTime;

    /** 用途说明 */
    private String purpose;

    /** 预计使用人数 */
    private Integer attendeeCount;

    /** 联系电话 */
    private String contactPhone;

    /** 附件 URL 列表（JSON 数组，存 COS 地址） */
    private String attachments;

    /**
     * 状态
     * 0-待审批 1-已通过 2-已拒绝 3-已取消 4-已过期
     */
    private Integer status;

    /** 备注 */
    private String remark;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 申请人真实姓名 */
    private String applicantName;

    /** 教学楼名称 */
    private String building;

    /** 教室编号 */
    private String roomNumber;

    /** 附件 URL 列表（解析后的对象列表） */
    private List<String> attachmentList;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getApplicantId() { return applicantId; }
    public void setApplicantId(Long applicantId) { this.applicantId = applicantId; }

    public Long getClassroomId() { return classroomId; }
    public void setClassroomId(Long classroomId) { this.classroomId = classroomId; }

    public Date getApplyDate() { return applyDate; }
    public void setApplyDate(Date applyDate) { this.applyDate = applyDate; }

    public Date getStartTime() { return startTime; }
    public void setStartTime(Date startTime) { this.startTime = startTime; }

    public Date getEndTime() { return endTime; }
    public void setEndTime(Date endTime) { this.endTime = endTime; }

    public String getPurpose() { return purpose; }
    public void setPurpose(String purpose) { this.purpose = purpose; }

    public Integer getAttendeeCount() { return attendeeCount; }
    public void setAttendeeCount(Integer attendeeCount) { this.attendeeCount = attendeeCount; }

    public String getContactPhone() { return contactPhone; }
    public void setContactPhone(String contactPhone) { this.contactPhone = contactPhone; }

    public String getAttachments() { return attachments; }
    public void setAttachments(String attachments) { this.attachments = attachments; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getApplicantName() { return applicantName; }
    public void setApplicantName(String applicantName) { this.applicantName = applicantName; }

    public String getBuilding() { return building; }
    public void setBuilding(String building) { this.building = building; }

    public String getRoomNumber() { return roomNumber; }
    public void setRoomNumber(String roomNumber) { this.roomNumber = roomNumber; }

    public List<String> getAttachmentList() { return attachmentList; }
    public void setAttachmentList(List<String> attachmentList) { this.attachmentList = attachmentList; }
}
