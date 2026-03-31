package com.yixiaoguan.knowledge.service.impl;

import com.yixiaoguan.knowledge.domain.YxKnowledgeReview;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeReviewMapper;
import com.yixiaoguan.knowledge.service.IYxKnowledgeReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 知识审核记录 Service 实现类
 */
@Service
public class YxKnowledgeReviewServiceImpl implements IYxKnowledgeReviewService {

    @Autowired
    private YxKnowledgeReviewMapper reviewMapper;

    @Override
    public Map<String, Object> selectPage(Long entryId, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxKnowledgeReview> rows = reviewMapper.selectPage(entryId, offset, pageSize);
        long total = reviewMapper.count(entryId);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxKnowledgeReview selectById(Long id) {
        return reviewMapper.selectById(id);
    }

    @Override
    public YxKnowledgeReview selectLatestByEntryId(Long entryId) {
        return reviewMapper.selectLatestByEntryId(entryId);
    }

    @Override
    public void insert(YxKnowledgeReview review) {
        reviewMapper.insert(review);
    }
}
