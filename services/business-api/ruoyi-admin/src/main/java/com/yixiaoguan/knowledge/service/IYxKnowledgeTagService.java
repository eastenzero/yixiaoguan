package com.yixiaoguan.knowledge.service;

import com.yixiaoguan.knowledge.domain.YxKnowledgeTag;

import java.util.List;

/**
 * 知识标签 Service 接口
 */
public interface IYxKnowledgeTagService {

    /**
     * 查询全部标签
     *
     * @return 标签列表
     */
    List<YxKnowledgeTag> selectAll();

    /**
     * 通过 ID 查询标签
     *
     * @param id 标签 ID
     * @return 标签详情
     */
    YxKnowledgeTag selectById(Long id);

    /**
     * 新增标签
     *
     * @param tag 标签对象
     */
    void insert(YxKnowledgeTag tag);

    /**
     * 更新标签
     *
     * @param tag 标签对象
     */
    void update(YxKnowledgeTag tag);

    /**
     * 软删除标签
     *
     * @param id 标签 ID
     */
    void deleteById(Long id);
}
