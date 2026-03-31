package com.yixiaoguan.auditlog.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 审计日志实体 - 对应 yx_audit_log 表
 * 记录所有关键操作，不可修改、不做软删除
 */
public class YxAuditLog implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 操作人 ID */
    private Long userId;

    /** 操作人用户名（冗余，便于查询） */
    private String username;

    /** 功能模块（user / knowledge / application / …） */
    private String module;

    /** 操作类型（create / update / delete / login / export / …） */
    private String action;

    /** 操作对象类型 */
    private String targetType;

    /** 操作对象 ID */
    private Long targetId;

    /** 操作描述 */
    private String description;

    /** HTTP 请求方式 */
    private String requestMethod;

    /** 请求 URL */
    private String requestUrl;

    /** 请求来源 IP */
    private String requestIp;

    /** 请求参数（脱敏后） */
    private String requestParams;

    /** 响应状态码 */
    private Integer responseCode;

    /** 耗时（ms） */
    private Long costTime;

    /**
     * 状态
     * 0-失败 1-成功
     */
    private Integer status;

    /** 错误信息 */
    private String errorMsg;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记（审计日志始终为 FALSE，不允许删除） */
    private Boolean isDeleted;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getModule() { return module; }
    public void setModule(String module) { this.module = module; }

    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }

    public String getTargetType() { return targetType; }
    public void setTargetType(String targetType) { this.targetType = targetType; }

    public Long getTargetId() { return targetId; }
    public void setTargetId(Long targetId) { this.targetId = targetId; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getRequestMethod() { return requestMethod; }
    public void setRequestMethod(String requestMethod) { this.requestMethod = requestMethod; }

    public String getRequestUrl() { return requestUrl; }
    public void setRequestUrl(String requestUrl) { this.requestUrl = requestUrl; }

    public String getRequestIp() { return requestIp; }
    public void setRequestIp(String requestIp) { this.requestIp = requestIp; }

    public String getRequestParams() { return requestParams; }
    public void setRequestParams(String requestParams) { this.requestParams = requestParams; }

    public Integer getResponseCode() { return responseCode; }
    public void setResponseCode(Integer responseCode) { this.responseCode = responseCode; }

    public Long getCostTime() { return costTime; }
    public void setCostTime(Long costTime) { this.costTime = costTime; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public String getErrorMsg() { return errorMsg; }
    public void setErrorMsg(String errorMsg) { this.errorMsg = errorMsg; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }
}
