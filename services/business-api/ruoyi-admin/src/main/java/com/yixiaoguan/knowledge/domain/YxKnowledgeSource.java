package com.yixiaoguan.knowledge.domain;

import java.io.Serializable;
import java.util.Date;

/**
 * 知识来源记录实体 - 对应 yx_knowledge_source 表
 * 关联到 raw 层的原始材料文件，实现来源追溯
 */
public class YxKnowledgeSource implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 原始文件名 */
    private String fileName;

    /** 原始文件路径（raw/ 目录下的相对路径） */
    private String filePath;

    /** COS 存储 URL（如已上传） */
    private String fileUrl;

    /** 文件类型（pdf / docx / md / …） */
    private String fileType;

    /** 文件大小（bytes） */
    private Long fileSize;

    /** 来源描述 */
    private String description;

    /** 上传人 ID */
    private Long uploaderId;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除标记 */
    private Boolean isDeleted;

    // ===== 连表扩展字段（不入库，仅查询时填充）=====

    /** 上传人真实姓名 */
    private String uploaderName;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public String getFileUrl() { return fileUrl; }
    public void setFileUrl(String fileUrl) { this.fileUrl = fileUrl; }

    public String getFileType() { return fileType; }
    public void setFileType(String fileType) { this.fileType = fileType; }

    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public Long getUploaderId() { return uploaderId; }
    public void setUploaderId(Long uploaderId) { this.uploaderId = uploaderId; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public String getUploaderName() { return uploaderName; }
    public void setUploaderName(String uploaderName) { this.uploaderName = uploaderName; }
}
