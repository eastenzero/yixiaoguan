package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeReview;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识审核记录 Mapper 接口 - 对应 yx_knowledge_review 表
 */
@Mapper
public interface YxKnowledgeReviewMapper {

    /**
     * 分页查询审核记录（连表带出审核人姓名、知识标题）
     *
     * @param entryId 条目 ID（null 则不过滤）
     * @param offset  分页偏移量
     * @param limit   每页条数
     * @return 审核记录列表
     */
    List<YxKnowledgeReview> selectPage(
            @Param("entryId") Long entryId,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计审核记录总数
     *
     * @param entryId 条目 ID（null 则不过滤）
     * @return 总条数
     */
    long count(@Param("entryId") Long entryId);

    /**
     * 通过主键查询审核记录
     *
     * @param id 记录 ID
     * @return 审核记录详情
     */
    YxKnowledgeReview selectById(@Param("id") Long id);

    /**
     * 查询指定条目的最新一条审核记录
     *
     * @param entryId 条目 ID
     * @return 最新审核记录
     */
    YxKnowledgeReview selectLatestByEntryId(@Param("entryId") Long entryId);

    /**
     * 新增审核记录
     *
     * @param review 审核记录对象
     * @return 影响行数
     */
    int insert(YxKnowledgeReview review);
}
