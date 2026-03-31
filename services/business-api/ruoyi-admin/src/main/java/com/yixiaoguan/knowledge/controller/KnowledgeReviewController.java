package com.yixiaoguan.knowledge.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.knowledge.service.IYxKnowledgeEntryService;
import com.yixiaoguan.knowledge.service.IYxKnowledgeReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 知识审核记录 Controller
 * 路由前缀：/api/v1/knowledge/reviews
 */
@RestController
@RequestMapping("/api/v1/knowledge/reviews")
public class KnowledgeReviewController {

    @Autowired
    private IYxKnowledgeReviewService reviewService;

    @Autowired
    private IYxKnowledgeEntryService entryService;

    /**
     * 分页查询审核记录
     * GET /api/v1/knowledge/reviews?entryId=1&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) Long entryId,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = reviewService.selectPage(entryId, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取审核记录详情
     * GET /api/v1/knowledge/reviews/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(reviewService.selectById(id));
    }

    /**
     * 审核通过
     * POST /api/v1/knowledge/reviews/{entryId}/approve
     * Body: { "opinion": "内容准确，准予发布" }
     */
    @PostMapping("/{entryId}/approve")
    public AjaxResult approve(@PathVariable Long entryId, @RequestBody(required = false) Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String opinion = (body != null) ? body.get("opinion") : null;
        entryService.approve(entryId, currentUser.getId(), opinion);
        return AjaxResult.success();
    }

    /**
     * 审核拒绝
     * POST /api/v1/knowledge/reviews/{entryId}/reject
     * Body: { "opinion": "内容有误，请修改后重新提交" }
     */
    @PostMapping("/{entryId}/reject")
    public AjaxResult reject(@PathVariable Long entryId, @RequestBody Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String opinion = body.get("opinion");
        entryService.reject(entryId, currentUser.getId(), opinion);
        return AjaxResult.success();
    }

    /**
     * 退回修改
     * POST /api/v1/knowledge/reviews/{entryId}/return
     * Body: { "opinion": "请补充相关政策依据" }
     */
    @PostMapping("/{entryId}/return")
    public AjaxResult returnForEdit(@PathVariable Long entryId, @RequestBody Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String opinion = body.get("opinion");
        entryService.returnForEdit(entryId, currentUser.getId(), opinion);
        return AjaxResult.success();
    }
}
