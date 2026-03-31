package com.yixiaoguan.knowledge.domain;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

/**
 * 知识分类实体 - 对应 yx_knowledge_category 表
 * 支持树形结构（8 大域 + 子分类）
 */
public class YxKnowledgeCategory implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 父分类 ID（0 = 顶级） */
    private Long parentId;

    /** 分类名称 */
    private String name;

    /** 分类编码（如 admission、scholarship） */
    private String code;

    /** 排序 */
    private Integer sortOrder;

    /** 分类说明 */
    private String description;

    /** 图标 */
    private String icon;

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

    // ===== 树形扩展字段（不入库）=====

    /** 子分类列表 */
    private List<YxKnowledgeCategory> children;

    // ===== Getter / Setter =====

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getParentId() { return parentId; }
    public void setParentId(Long parentId) { this.parentId = parentId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }

    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public Boolean getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Boolean isDeleted) { this.isDeleted = isDeleted; }

    public List<YxKnowledgeCategory> getChildren() { return children; }
    public void setChildren(List<YxKnowledgeCategory> children) { this.children = children; }
}
