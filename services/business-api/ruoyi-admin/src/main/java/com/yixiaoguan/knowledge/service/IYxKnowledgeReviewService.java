package com.yixiaoguan.knowledge.service;

import com.yixiaoguan.knowledge.domain.YxKnowledgeReview;

import java.util.Map;

/**
 * 知识审核记录 Service 接口
 */
public interface IYxKnowledgeReviewService {

    /**
     * 分页查询审核记录
     *
     * @param entryId  条目 ID（null 则不过滤）
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(Long entryId, int pageNum, int pageSize);

    /**
     * 通过 ID 查询审核记录
     *
     * @param id 记录 ID
     * @return 审核记录详情
     */
    YxKnowledgeReview selectById(Long id);

    /**
     * 查询指定条目的最新审核记录
     *
     * @param entryId 条目 ID
     * @return 最新审核记录
     */
    YxKnowledgeReview selectLatestByEntryId(Long entryId);

    /**
     * 新增审核记录
     *
     * @param review 审核记录对象
     */
    void insert(YxKnowledgeReview review);
}
