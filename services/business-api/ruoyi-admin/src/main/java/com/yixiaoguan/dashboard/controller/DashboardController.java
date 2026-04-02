package com.yixiaoguan.dashboard.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.yixiaoguan.dashboard.dto.*;
import com.yixiaoguan.dashboard.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 教师工作台（仪表盘）Dashboard Controller
 * 路由前缀：/api/v1/dashboard
 */
@RestController
@RequestMapping("/api/v1/dashboard")
public class DashboardController extends BaseController {

    @Autowired
    private DashboardService dashboardService;

    /**
     * 工作台统计概览
     * GET /api/v1/dashboard/stats
     */
    @GetMapping("/stats")
    public AjaxResult stats() {
        DashboardStatsDTO dto = dashboardService.getDashboardStats();
        return AjaxResult.success(dto);
    }

    /**
     * 今日提问列表
     * GET /api/v1/dashboard/today-questions?pageNum=1&pageSize=10
     */
    @GetMapping("/today-questions")
    public AjaxResult todayQuestions(
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = dashboardService.getTodayQuestions(pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 高频问题统计
     * GET /api/v1/dashboard/hot-questions?limit=5
     */
    @GetMapping("/hot-questions")
    public AjaxResult hotQuestions(@RequestParam(defaultValue = "5") int limit) {
        List<HotQuestionDTO> list = dashboardService.getHotQuestions(limit);
        return AjaxResult.success(list);
    }

    /**
     * 待审批事项列表
     * GET /api/v1/dashboard/pending-approvals?limit=5
     */
    @GetMapping("/pending-approvals")
    public AjaxResult pendingApprovals(@RequestParam(defaultValue = "5") int limit) {
        List<PendingApprovalDTO> list = dashboardService.getPendingApprovals(limit);
        return AjaxResult.success(list);
    }

    /**
     * AI 舆情预警
     * GET /api/v1/dashboard/ai-warnings
     */
    @GetMapping("/ai-warnings")
    public AjaxResult aiWarnings() {
        List<AIWarningDTO> list = dashboardService.getAIWarnings();
        return AjaxResult.success(list);
    }

    /**
     * 工作台聚合总览
     * GET /api/v1/dashboard/overview
     */
    @GetMapping("/overview")
    public AjaxResult overview() {
        DashboardOverviewDTO dto = dashboardService.getDashboardOverview();
        return AjaxResult.success(dto);
    }
}
