package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeCategory;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识分类 Mapper 接口 - 对应 yx_knowledge_category 表
 */
@Mapper
public interface YxKnowledgeCategoryMapper {

    /**
     * 查询全部分类列表（用于构建树形结构）
     *
     * @param status 状态过滤（null 则不过滤）
     * @return 分类列表
     */
    List<YxKnowledgeCategory> selectAll(@Param("status") Integer status);

    /**
     * 通过主键查询分类
     *
     * @param id 分类 ID
     * @return 分类详情
     */
    YxKnowledgeCategory selectById(@Param("id") Long id);

    /**
     * 新增分类
     *
     * @param category 分类对象
     * @return 影响行数
     */
    int insert(YxKnowledgeCategory category);

    /**
     * 更新分类
     *
     * @param category 分类对象
     * @return 影响行数
     */
    int update(YxKnowledgeCategory category);

    /**
     * 软删除分类
     *
     * @param id 分类 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
