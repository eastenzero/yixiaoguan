package com.yixiaoguan.knowledge.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.knowledge.domain.YxKnowledgeCategory;
import com.yixiaoguan.knowledge.mapper.YxKnowledgeCategoryMapper;
import com.yixiaoguan.knowledge.service.IYxKnowledgeCategoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

/**
 * 知识分类 Service 实现类
 */
@Service
public class YxKnowledgeCategoryServiceImpl implements IYxKnowledgeCategoryService {

    @Autowired
    private YxKnowledgeCategoryMapper categoryMapper;

    @Override
    public List<YxKnowledgeCategory> selectAll(Integer status) {
        return categoryMapper.selectAll(status);
    }

    @Override
    public List<YxKnowledgeCategory> buildTree(Integer status) {
        List<YxKnowledgeCategory> all = categoryMapper.selectAll(status);
        return buildTreeRecursive(all, 0L);
    }

    /**
     * 递归构建树形结构
     *
     * @param all      全部分类列表
     * @param parentId 当前父节点 ID
     * @return 当前层级的分类列表
     */
    private List<YxKnowledgeCategory> buildTreeRecursive(List<YxKnowledgeCategory> all, Long parentId) {
        List<YxKnowledgeCategory> children = new ArrayList<>();
        for (YxKnowledgeCategory category : all) {
            if (parentId.equals(category.getParentId())) {
                category.setChildren(buildTreeRecursive(all, category.getId()));
                children.add(category);
            }
        }
        return children;
    }

    @Override
    public YxKnowledgeCategory selectById(Long id) {
        YxKnowledgeCategory category = categoryMapper.selectById(id);
        if (category == null) {
            throw new ServiceException("分类不存在");
        }
        return category;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void insert(YxKnowledgeCategory category) {
        if (category.getParentId() == null) {
            category.setParentId(0L);
        }
        if (category.getStatus() == null) {
            category.setStatus(1);
        }
        if (category.getSortOrder() == null) {
            category.setSortOrder(0);
        }
        categoryMapper.insert(category);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(YxKnowledgeCategory category) {
        YxKnowledgeCategory exist = categoryMapper.selectById(category.getId());
        if (exist == null) {
            throw new ServiceException("分类不存在");
        }
        categoryMapper.update(category);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxKnowledgeCategory exist = categoryMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("分类不存在");
        }
        // 简单校验：若存在子分类则不允许删除（实际可扩展为级联删除）
        List<YxKnowledgeCategory> all = categoryMapper.selectAll(null);
        for (YxKnowledgeCategory c : all) {
            if (id.equals(c.getParentId())) {
                throw new ServiceException("该分类下存在子分类，无法删除");
            }
        }
        categoryMapper.deleteById(id);
    }
}
