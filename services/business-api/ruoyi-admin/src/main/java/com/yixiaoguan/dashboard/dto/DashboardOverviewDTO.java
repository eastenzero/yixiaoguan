package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;
import java.util.List;

/**
 * 工作台聚合总览 DTO
 */
public class DashboardOverviewDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 统计概览 */
    private DashboardStatsDTO stats;

    /** 今日提问列表 */
    private List<TodayQuestionDTO> questions;

    /** 高频问题统计 */
    private List<HotQuestionDTO> hotQuestions;

    /** 待审批事项列表 */
    private List<PendingApprovalDTO> pendingApprovals;

    /** AI 舆情预警（可为 null） */
    private AIWarningDTO aiWarning;

    public DashboardStatsDTO getStats() {
        return stats;
    }

    public void setStats(DashboardStatsDTO stats) {
        this.stats = stats;
    }

    public List<TodayQuestionDTO> getQuestions() {
        return questions;
    }

    public void setQuestions(List<TodayQuestionDTO> questions) {
        this.questions = questions;
    }

    public List<HotQuestionDTO> getHotQuestions() {
        return hotQuestions;
    }

    public void setHotQuestions(List<HotQuestionDTO> hotQuestions) {
        this.hotQuestions = hotQuestions;
    }

    public List<PendingApprovalDTO> getPendingApprovals() {
        return pendingApprovals;
    }

    public void setPendingApprovals(List<PendingApprovalDTO> pendingApprovals) {
        this.pendingApprovals = pendingApprovals;
    }

    public AIWarningDTO getAiWarning() {
        return aiWarning;
    }

    public void setAiWarning(AIWarningDTO aiWarning) {
        this.aiWarning = aiWarning;
    }
}
