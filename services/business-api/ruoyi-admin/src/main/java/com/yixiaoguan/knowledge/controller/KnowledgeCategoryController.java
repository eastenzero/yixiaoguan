package com.yixiaoguan.knowledge.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.yixiaoguan.knowledge.domain.YxKnowledgeCategory;
import com.yixiaoguan.knowledge.service.IYxKnowledgeCategoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 知识分类 Controller
 * 路由前缀：/api/v1/knowledge/categories
 */
@RestController
@RequestMapping("/api/v1/knowledge/categories")
public class KnowledgeCategoryController {

    @Autowired
    private IYxKnowledgeCategoryService categoryService;

    /**
     * 获取分类树形结构
     * GET /api/v1/knowledge/categories/tree?status=1
     */
    @GetMapping("/tree")
    public AjaxResult tree(@RequestParam(required = false) Integer status) {
        List<YxKnowledgeCategory> tree = categoryService.buildTree(status);
        return AjaxResult.success(tree);
    }

    /**
     * 获取全部分类（平铺列表）
     * GET /api/v1/knowledge/categories?status=1
     */
    @GetMapping
    public AjaxResult list(@RequestParam(required = false) Integer status) {
        return AjaxResult.success(categoryService.selectAll(status));
    }

    /**
     * 获取分类详情
     * GET /api/v1/knowledge/categories/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(categoryService.selectById(id));
    }

    /**
     * 新增分类
     * POST /api/v1/knowledge/categories
     */
    @PostMapping
    public AjaxResult add(@RequestBody YxKnowledgeCategory category) {
        categoryService.insert(category);
        return AjaxResult.success();
    }

    /**
     * 更新分类
     * PUT /api/v1/knowledge/categories/{id}
     */
    @PutMapping("/{id}")
    public AjaxResult update(@PathVariable Long id, @RequestBody YxKnowledgeCategory category) {
        category.setId(id);
        categoryService.update(category);
        return AjaxResult.success();
    }

    /**
     * 删除分类（软删除）
     * DELETE /api/v1/knowledge/categories/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        categoryService.deleteById(id);
        return AjaxResult.success();
    }
}
