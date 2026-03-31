package com.yixiaoguan.knowledge.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.knowledge.domain.YxKnowledgeEntry;
import com.yixiaoguan.knowledge.domain.YxKnowledgeEntryTag;
import com.yixiaoguan.knowledge.domain.YxKnowledgeReview;
import com.yixiaoguan.knowledge.domain.YxKnowledgeTag;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeEntryMapper;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeEntryTagMapper;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeReviewMapper;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeTagMapper;
import com.yixiaoguan.knowledge.service.IYxKnowledgeEntryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.CollectionUtils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 知识条目 Service 实现类
 * 包含完整的一级审核状态机流转逻辑
 */
@Service
public class YxKnowledgeEntryServiceImpl implements IYxKnowledgeEntryService {

    @Autowired
    private YxKnowledgeEntryMapper entryMapper;

    @Autowired
    private YxKnowledgeEntryTagMapper entryTagMapper;

    @Autowired
    private YxKnowledgeReviewMapper reviewMapper;

    @Autowired
    private YxKnowledgeTagMapper tagMapper;

    @Override
    public Map<String, Object> selectPage(Long categoryId, Integer status, String title, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxKnowledgeEntry> rows = entryMapper.selectPage(categoryId, status, title, offset, pageSize);
        long total = entryMapper.count(categoryId, status, title);

        // 批量填充标签
        if (!CollectionUtils.isEmpty(rows)) {
            for (YxKnowledgeEntry entry : rows) {
                fillTags(entry);
            }
        }

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxKnowledgeEntry selectById(Long id) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        fillTags(entry);
        return entry;
    }

    /**
     * 填充条目的标签信息
     */
    private void fillTags(YxKnowledgeEntry entry) {
        List<YxKnowledgeEntryTag> entryTags = entryTagMapper.selectByEntryId(entry.getId());
        if (!CollectionUtils.isEmpty(entryTags)) {
            List<YxKnowledgeTag> tags = entryTags.stream()
                    .map(et -> {
                        YxKnowledgeTag tag = new YxKnowledgeTag();
                        tag.setId(et.getTagId());
                        tag.setName(et.getTagName());
                        return tag;
                    })
                    .collect(Collectors.toList());
            List<Long> tagIds = entryTags.stream()
                    .map(YxKnowledgeEntryTag::getTagId)
                    .collect(Collectors.toList());
            entry.setTags(tags);
            entry.setTagIds(tagIds);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxKnowledgeEntry saveDraft(YxKnowledgeEntry entry, Long authorId) {
        if (entry.getId() == null) {
            // 新建草稿
            entry.setStatus(0); // 草稿
            entry.setVersion(1);
            entry.setAuthorId(authorId);
            entryMapper.insert(entry);
        } else {
            // 更新草稿
            YxKnowledgeEntry exist = entryMapper.selectById(entry.getId());
            if (exist == null) {
                throw new ServiceException("知识条目不存在");
            }
            // 只允许编辑草稿(0)或审核拒绝(4)或已下线(3)的条目
            if (exist.getStatus() != 0 && exist.getStatus() != 3 && exist.getStatus() != 4) {
                throw new ServiceException("当前状态不允许编辑，仅草稿、已下线、审核拒绝状态可修改");
            }
            // 版本号 +1（每次编辑 +1）
            entry.setVersion(exist.getVersion() + 1);
            entryMapper.update(entry);
        }

        // 同步标签关联
        syncEntryTags(entry.getId(), entry.getTagIds());

        return entryMapper.selectById(entry.getId());
    }

    /**
     * 同步条目与标签的关联关系
     *
     * @param entryId 条目 ID
     * @param tagIds  标签 ID 列表
     */
    private void syncEntryTags(Long entryId, List<Long> tagIds) {
        entryTagMapper.deleteByEntryId(entryId);
        if (!CollectionUtils.isEmpty(tagIds)) {
            entryTagMapper.batchInsert(entryId, tagIds);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void submitForReview(Long id, Long operator) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        // 仅草稿(0)或退回修改后的草稿(0)可提审
        if (entry.getStatus() != 0) {
            throw new ServiceException("仅草稿状态可发起提审");
        }
        entryMapper.updateStatus(id, 1, entry.getVersion());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void approve(Long id, Long reviewerId, String opinion) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        // 仅待审核(1)可通过
        if (entry.getStatus() != 1) {
            throw new ServiceException("仅待审核状态可执行通过操作");
        }

        int newVersion = entry.getVersion() + 1;
        // 更新为已发布(2)，版本号+1，并记录发布时间
        entryMapper.updatePublishInfo(id, 2, newVersion);

        // 写入审核记录
        YxKnowledgeReview review = new YxKnowledgeReview();
        review.setEntryId(id);
        review.setReviewerId(reviewerId);
        review.setAction(1); // 通过
        review.setOpinion(opinion);
        review.setEntryVersion(entry.getVersion());
        reviewMapper.insert(review);

        // TODO: 审核通过后，通过 HTTP 调用 ai-service 进行向量化入库（本阶段暂不实现）
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void reject(Long id, Long reviewerId, String opinion) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        if (entry.getStatus() != 1) {
            throw new ServiceException("仅待审核状态可执行拒绝操作");
        }

        entryMapper.updateStatus(id, 4, entry.getVersion());

        YxKnowledgeReview review = new YxKnowledgeReview();
        review.setEntryId(id);
        review.setReviewerId(reviewerId);
        review.setAction(2); // 拒绝
        review.setOpinion(opinion);
        review.setEntryVersion(entry.getVersion());
        reviewMapper.insert(review);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void returnForEdit(Long id, Long reviewerId, String opinion) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        if (entry.getStatus() != 1) {
            throw new ServiceException("仅待审核状态可执行退回修改操作");
        }

        entryMapper.updateStatus(id, 0, entry.getVersion());

        YxKnowledgeReview review = new YxKnowledgeReview();
        review.setEntryId(id);
        review.setReviewerId(reviewerId);
        review.setAction(3); // 退回修改
        review.setOpinion(opinion);
        review.setEntryVersion(entry.getVersion());
        reviewMapper.insert(review);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void offline(Long id, Long operator) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        if (entry.getStatus() != 2) {
            throw new ServiceException("仅已发布状态可执行下线操作");
        }
        entryMapper.updateStatus(id, 3, entry.getVersion());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxKnowledgeEntry entry = entryMapper.selectById(id);
        if (entry == null) {
            throw new ServiceException("知识条目不存在");
        }
        entryMapper.deleteById(id);
        entryTagMapper.deleteByEntryId(id);
    }
}
