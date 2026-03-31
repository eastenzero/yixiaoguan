package com.yixiaoguan.knowledge.service;

import com.yixiaoguan.knowledge.domain.YxKnowledgeCategory;

import java.util.List;

/**
 * 知识分类 Service 接口
 */
public interface IYxKnowledgeCategoryService {

    /**
     * 查询全部分类（平铺列表）
     *
     * @param status 状态过滤（null 则不过滤）
     * @return 分类列表
     */
    List<YxKnowledgeCategory> selectAll(Integer status);

    /**
     * 构建分类树形结构
     *
     * @param status 状态过滤（null 则不过滤）
     * @return 树形分类列表
     */
    List<YxKnowledgeCategory> buildTree(Integer status);

    /**
     * 通过 ID 查询分类
     *
     * @param id 分类 ID
     * @return 分类详情
     */
    YxKnowledgeCategory selectById(Long id);

    /**
     * 新增分类
     *
     * @param category 分类对象
     */
    void insert(YxKnowledgeCategory category);

    /**
     * 更新分类
     *
     * @param category 分类对象
     */
    void update(YxKnowledgeCategory category);

    /**
     * 软删除分类
     *
     * @param id 分类 ID
     */
    void deleteById(Long id);
}
