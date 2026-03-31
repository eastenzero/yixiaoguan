package com.yixiaoguan.knowledge.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.knowledge.domain.YxKnowledgeEntry;
import com.yixiaoguan.knowledge.service.IYxKnowledgeEntryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 知识条目 Controller
 * 路由前缀：/api/v1/knowledge/entries
 */
@RestController
@RequestMapping("/api/v1/knowledge/entries")
public class KnowledgeEntryController {

    @Autowired
    private IYxKnowledgeEntryService entryService;

    /**
     * 分页查询知识条目
     * GET /api/v1/knowledge/entries?categoryId=1&status=0&title=xxx&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) Integer status,
            @RequestParam(required = false) String title,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = entryService.selectPage(categoryId, status, title, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取知识条目详情
     * GET /api/v1/knowledge/entries/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(entryService.selectById(id));
    }

    /**
     * 新增/保存草稿
     * POST /api/v1/knowledge/entries/draft
     */
    @PostMapping("/draft")
    public AjaxResult saveDraft(@RequestBody YxKnowledgeEntry entry) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        YxKnowledgeEntry saved = entryService.saveDraft(entry, currentUser.getId());
        return AjaxResult.success(saved);
    }

    /**
     * 发起提审
     * POST /api/v1/knowledge/entries/{id}/submit
     */
    @PostMapping("/{id}/submit")
    public AjaxResult submitForReview(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        entryService.submitForReview(id, currentUser.getId());
        return AjaxResult.success();
    }

    /**
     * 下线条目
     * POST /api/v1/knowledge/entries/{id}/offline
     */
    @PostMapping("/{id}/offline")
    public AjaxResult offline(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        entryService.offline(id, currentUser.getId());
        return AjaxResult.success();
    }

    /**
     * 删除条目（软删除）
     * DELETE /api/v1/knowledge/entries/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        entryService.deleteById(id);
        return AjaxResult.success();
    }
}
