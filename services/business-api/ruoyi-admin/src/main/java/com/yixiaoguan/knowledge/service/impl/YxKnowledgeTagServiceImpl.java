package com.yixiaoguan.knowledge.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.knowledge.domain.YxKnowledgeTag;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeTagMapper;
import com.yixiaoguan.knowledge.service.IYxKnowledgeTagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 知识标签 Service 实现类
 */
@Service
public class YxKnowledgeTagServiceImpl implements IYxKnowledgeTagService {

    @Autowired
    private YxKnowledgeTagMapper tagMapper;

    @Override
    public List<YxKnowledgeTag> selectAll() {
        return tagMapper.selectAll();
    }

    @Override
    public YxKnowledgeTag selectById(Long id) {
        YxKnowledgeTag tag = tagMapper.selectById(id);
        if (tag == null) {
            throw new ServiceException("标签不存在");
        }
        return tag;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void insert(YxKnowledgeTag tag) {
        YxKnowledgeTag exist = tagMapper.selectByName(tag.getName());
        if (exist != null) {
            throw new ServiceException("标签名称已存在");
        }
        if (tag.getSortOrder() == null) {
            tag.setSortOrder(0);
        }
        tagMapper.insert(tag);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(YxKnowledgeTag tag) {
        YxKnowledgeTag exist = tagMapper.selectById(tag.getId());
        if (exist == null) {
            throw new ServiceException("标签不存在");
        }
        // 若修改了名称，需校验唯一性
        if (!exist.getName().equals(tag.getName())) {
            YxKnowledgeTag nameExist = tagMapper.selectByName(tag.getName());
            if (nameExist != null) {
                throw new ServiceException("标签名称已存在");
            }
        }
        tagMapper.update(tag);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxKnowledgeTag exist = tagMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("标签不存在");
        }
        tagMapper.deleteById(id);
    }
}
