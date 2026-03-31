package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeTag;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识标签 Mapper 接口 - 对应 yx_knowledge_tag 表
 */
@Mapper
public interface YxKnowledgeTagMapper {

    /**
     * 查询全部标签
     *
     * @return 标签列表
     */
    List<YxKnowledgeTag> selectAll();

    /**
     * 通过主键查询标签
     *
     * @param id 标签 ID
     * @return 标签详情
     */
    YxKnowledgeTag selectById(@Param("id") Long id);

    /**
     * 通过名称查询标签
     *
     * @param name 标签名称
     * @return 标签详情
     */
    YxKnowledgeTag selectByName(@Param("name") String name);

    /**
     * 新增标签
     *
     * @param tag 标签对象
     * @return 影响行数
     */
    int insert(YxKnowledgeTag tag);

    /**
     * 更新标签
     *
     * @param tag 标签对象
     * @return 影响行数
     */
    int update(YxKnowledgeTag tag);

    /**
     * 软删除标签
     *
     * @param id 标签 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
