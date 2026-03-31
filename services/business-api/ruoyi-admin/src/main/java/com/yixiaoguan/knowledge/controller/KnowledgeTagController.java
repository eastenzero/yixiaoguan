package com.yixiaoguan.knowledge.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.yixiaoguan.knowledge.domain.YxKnowledgeTag;
import com.yixiaoguan.knowledge.service.IYxKnowledgeTagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 知识标签 Controller
 * 路由前缀：/api/v1/knowledge/tags
 */
@RestController
@RequestMapping("/api/v1/knowledge/tags")
public class KnowledgeTagController {

    @Autowired
    private IYxKnowledgeTagService tagService;

    /**
     * 获取全部标签
     * GET /api/v1/knowledge/tags
     */
    @GetMapping
    public AjaxResult list() {
        return AjaxResult.success(tagService.selectAll());
    }

    /**
     * 获取标签详情
     * GET /api/v1/knowledge/tags/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(tagService.selectById(id));
    }

    /**
     * 新增标签
     * POST /api/v1/knowledge/tags
     */
    @PostMapping
    public AjaxResult add(@RequestBody YxKnowledgeTag tag) {
        tagService.insert(tag);
        return AjaxResult.success();
    }

    /**
     * 更新标签
     * PUT /api/v1/knowledge/tags/{id}
     */
    @PutMapping("/{id}")
    public AjaxResult update(@PathVariable Long id, @RequestBody YxKnowledgeTag tag) {
        tag.setId(id);
        tagService.update(tag);
        return AjaxResult.success();
    }

    /**
     * 删除标签（软删除）
     * DELETE /api/v1/knowledge/tags/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        tagService.deleteById(id);
        return AjaxResult.success();
    }
}
