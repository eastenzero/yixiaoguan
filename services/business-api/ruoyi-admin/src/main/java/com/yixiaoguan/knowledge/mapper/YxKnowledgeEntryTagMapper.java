package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeEntryTag;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识条目-标签关联 Mapper 接口 - 对应 yx_knowledge_entry_tag 表
 */
@Mapper
public interface YxKnowledgeEntryTagMapper {

    /**
     * 批量插入条目-标签关联
     *
     * @param entryId 条目 ID
     * @param tagIds  标签 ID 列表
     * @return 影响行数
     */
    int batchInsert(@Param("entryId") Long entryId, @Param("tagIds") List<Long> tagIds);

    /**
     * 通过条目 ID 删除全部关联
     *
     * @param entryId 条目 ID
     * @return 影响行数
     */
    int deleteByEntryId(@Param("entryId") Long entryId);

    /**
     * 查询条目关联的标签列表
     *
     * @param entryId 条目 ID
     * @return 标签关联列表
     */
    List<YxKnowledgeEntryTag> selectByEntryId(@Param("entryId") Long entryId);

    /**
     * 查询条目关联的标签 ID 列表
     *
     * @param entryId 条目 ID
     * @return 标签 ID 列表
     */
    List<Long> selectTagIdsByEntryId(@Param("entryId") Long entryId);
}
