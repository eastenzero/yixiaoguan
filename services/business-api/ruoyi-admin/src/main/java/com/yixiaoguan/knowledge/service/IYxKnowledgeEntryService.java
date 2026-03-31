package com.yixiaoguan.knowledge.service;

import com.yixiaoguan.knowledge.domain.YxKnowledgeEntry;

import java.util.List;
import java.util.Map;

/**
 * 知识条目 Service 接口
 */
public interface IYxKnowledgeEntryService {

    /**
     * 分页查询知识条目
     *
     * @param categoryId 分类 ID（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @param title      标题模糊查询（null 则不过滤）
     * @param pageNum    页码（从 1 开始）
     * @param pageSize   每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(Long categoryId, Integer status, String title, int pageNum, int pageSize);

    /**
     * 通过 ID 查询条目详情（含标签、扩展字段）
     *
     * @param id 条目 ID
     * @return 条目详情
     */
    YxKnowledgeEntry selectById(Long id);

    /**
     * 新增或更新草稿
     * 新建时 status=0, version=1；更新时 version+1
     *
     * @param entry    条目对象
     * @param authorId 当前登录用户 ID
     * @return 保存后的条目（含 ID）
     */
    YxKnowledgeEntry saveDraft(YxKnowledgeEntry entry, Long authorId);

    /**
     * 发起提审：草稿(0) / 退回修改后  → 待审核(1)
     *
     * @param id       条目 ID
     * @param operator 操作人 ID
     */
    void submitForReview(Long id, Long operator);

    /**
     * 审核通过：待审核(1) → 已发布(2)
     * 同时 version+1，记录 published_at，写入审核记录
     *
     * @param id         条目 ID
     * @param reviewerId 审核人 ID
     * @param opinion    审核意见（可为空）
     */
    void approve(Long id, Long reviewerId, String opinion);

    /**
     * 审核拒绝：待审核(1) → 审核拒绝(4)
     * 同时写入审核记录
     *
     * @param id         条目 ID
     * @param reviewerId 审核人 ID
     * @param opinion    审核意见
     */
    void reject(Long id, Long reviewerId, String opinion);

    /**
     * 退回修改：待审核(1) → 草稿(0)
     * 同时写入审核记录（action=3）
     *
     * @param id         条目 ID
     * @param reviewerId 审核人 ID
     * @param opinion    审核意见
     */
    void returnForEdit(Long id, Long reviewerId, String opinion);

    /**
     * 下线条目：已发布(2) → 已下线(3)
     *
     * @param id       条目 ID
     * @param operator 操作人 ID
     */
    void offline(Long id, Long operator);

    /**
     * 删除条目（软删除）
     *
     * @param id 条目 ID
     */
    void deleteById(Long id);
}
