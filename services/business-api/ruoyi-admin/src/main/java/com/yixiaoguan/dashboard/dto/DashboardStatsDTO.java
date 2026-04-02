package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;

/**
 * 工作台统计概览 DTO
 */
public class DashboardStatsDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 今日处理提问 */
    private int todayQuestions;

    /** 同比昨日增长率（百分比整数，如 +12 或 -5） */
    private int todayQuestionsGrowth;

    /** 待审批事项 */
    private int pendingApprovals;

    /** 即将超时审批 */
    private int urgentApprovals;

    /** AI 自动解决率 */
    private int aiResolutionRate;

    /** 平均响应时间（分钟） */
    private int avgResponseTime;

    /** 较上周改善时间（分钟） */
    private int responseTimeImprovement;

    public int getTodayQuestions() {
        return todayQuestions;
    }

    public void setTodayQuestions(int todayQuestions) {
        this.todayQuestions = todayQuestions;
    }

    public int getTodayQuestionsGrowth() {
        return todayQuestionsGrowth;
    }

    public void setTodayQuestionsGrowth(int todayQuestionsGrowth) {
        this.todayQuestionsGrowth = todayQuestionsGrowth;
    }

    public int getPendingApprovals() {
        return pendingApprovals;
    }

    public void setPendingApprovals(int pendingApprovals) {
        this.pendingApprovals = pendingApprovals;
    }

    public int getUrgentApprovals() {
        return urgentApprovals;
    }

    public void setUrgentApprovals(int urgentApprovals) {
        this.urgentApprovals = urgentApprovals;
    }

    public int getAiResolutionRate() {
        return aiResolutionRate;
    }

    public void setAiResolutionRate(int aiResolutionRate) {
        this.aiResolutionRate = aiResolutionRate;
    }

    public int getAvgResponseTime() {
        return avgResponseTime;
    }

    public void setAvgResponseTime(int avgResponseTime) {
        this.avgResponseTime = avgResponseTime;
    }

    public int getResponseTimeImprovement() {
        return responseTimeImprovement;
    }

    public void setResponseTimeImprovement(int responseTimeImprovement) {
        this.responseTimeImprovement = responseTimeImprovement;
    }
}
