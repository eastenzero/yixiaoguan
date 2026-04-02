package com.yixiaoguan.dashboard.service;

import com.yixiaoguan.dashboard.dto.*;

import java.util.List;
import java.util.Map;

/**
 * Dashboard 工作台聚合服务接口
 */
public interface DashboardService {

    /**
     * 获取工作台统计概览
     */
    DashboardStatsDTO getDashboardStats();

    /**
     * 获取今日提问列表（分页）
     *
     * @param pageNum  页码
     * @param pageSize 每页条数
     * @return { total, rows }
     */
    Map<String, Object> getTodayQuestions(int pageNum, int pageSize);

    /**
     * 获取高频问题统计
     *
     * @param limit 条数限制
     * @return 热度列表
     */
    List<HotQuestionDTO> getHotQuestions(int limit);

    /**
     * 获取待审批事项列表
     *
     * @param limit 条数限制
     * @return 待审批列表
     */
    List<PendingApprovalDTO> getPendingApprovals(int limit);

    /**
     * 获取 AI 舆情预警
     *
     * @return 预警列表（当前版本简单实现）
     */
    List<AIWarningDTO> getAIWarnings();

    /**
     * 获取工作台聚合总览
     *
     * @return 聚合数据
     */
    DashboardOverviewDTO getDashboardOverview();
}
