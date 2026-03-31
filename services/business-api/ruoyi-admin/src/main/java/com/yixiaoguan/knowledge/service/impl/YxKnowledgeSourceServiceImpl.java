package com.yixiaoguan.knowledge.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.knowledge.domain.YxKnowledgeSource;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeSourceMapper;
import com.yixiaoguan.knowledge.service.IYxKnowledgeSourceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 知识来源记录 Service 实现类
 */
@Service
public class YxKnowledgeSourceServiceImpl implements IYxKnowledgeSourceService {

    @Autowired
    private YxKnowledgeSourceMapper sourceMapper;

    @Override
    public Map<String, Object> selectPage(String fileName, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxKnowledgeSource> rows = sourceMapper.selectPage(fileName, offset, pageSize);
        long total = sourceMapper.count(fileName);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxKnowledgeSource selectById(Long id) {
        YxKnowledgeSource source = sourceMapper.selectById(id);
        if (source == null) {
            throw new ServiceException("来源记录不存在");
        }
        return source;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void insert(YxKnowledgeSource source) {
        sourceMapper.insert(source);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(YxKnowledgeSource source) {
        YxKnowledgeSource exist = sourceMapper.selectById(source.getId());
        if (exist == null) {
            throw new ServiceException("来源记录不存在");
        }
        sourceMapper.update(source);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxKnowledgeSource exist = sourceMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("来源记录不存在");
        }
        sourceMapper.deleteById(id);
    }
}
