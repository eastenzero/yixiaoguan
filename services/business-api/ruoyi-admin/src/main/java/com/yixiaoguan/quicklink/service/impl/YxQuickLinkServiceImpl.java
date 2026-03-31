package com.yixiaoguan.quicklink.service.impl;

import com.alibaba.fastjson2.JSON;
import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.quicklink.domain.YxQuickLink;
import com.yixiaoguan.quicklink.mapper.YxQuickLinkMapper;
import com.yixiaoguan.quicklink.service.IYxQuickLinkService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 快捷链接 Service 实现类
 */
@Service
public class YxQuickLinkServiceImpl implements IYxQuickLinkService {

    @Autowired
    private YxQuickLinkMapper quickLinkMapper;

    @Override
    public Map<String, Object> selectPage(String name, String category, Boolean isActive, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxQuickLink> rows = quickLinkMapper.selectPage(name, category, isActive, offset, pageSize);

        for (YxQuickLink row : rows) {
            parseTags(row);
        }

        long total = quickLinkMapper.count(name, category, isActive);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxQuickLink selectById(Long id) {
        YxQuickLink quickLink = quickLinkMapper.selectById(id);
        if (quickLink == null) {
            throw new ServiceException("快捷链接不存在");
        }
        parseTags(quickLink);
        return quickLink;
    }

    /**
     * 解析标签 JSON 字符串为列表
     */
    private void parseTags(YxQuickLink quickLink) {
        if (StringUtils.hasText(quickLink.getTags())) {
            try {
                List<String> tagList = JSON.parseArray(quickLink.getTags(), String.class);
                quickLink.setTagList(tagList);
            } catch (Exception e) {
                quickLink.setTagList(null);
            }
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void insert(YxQuickLink quickLink) {
        if (quickLink.getIsActive() == null) {
            quickLink.setIsActive(true);
        }
        if (quickLink.getSortOrder() == null) {
            quickLink.setSortOrder(0);
        }
        if (quickLink.getTagList() != null && !quickLink.getTagList().isEmpty()) {
            quickLink.setTags(JSON.toJSONString(quickLink.getTagList()));
        }
        quickLinkMapper.insert(quickLink);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(YxQuickLink quickLink) {
        YxQuickLink exist = quickLinkMapper.selectById(quickLink.getId());
        if (exist == null) {
            throw new ServiceException("快捷链接不存在");
        }

        if (quickLink.getTagList() != null && !quickLink.getTagList().isEmpty()) {
            quickLink.setTags(JSON.toJSONString(quickLink.getTagList()));
        }

        quickLinkMapper.update(quickLink);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxQuickLink exist = quickLinkMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("快捷链接不存在");
        }
        quickLinkMapper.deleteById(id);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void incrementClickCount(Long id) {
        YxQuickLink exist = quickLinkMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("快捷链接不存在");
        }
        quickLinkMapper.incrementClickCount(id);
    }
}
