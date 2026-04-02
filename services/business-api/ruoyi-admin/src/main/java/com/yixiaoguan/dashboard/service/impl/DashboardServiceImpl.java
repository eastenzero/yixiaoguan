package com.yixiaoguan.dashboard.service.impl;

import com.yixiaoguan.dashboard.dto.*;
import com.yixiaoguan.dashboard.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Dashboard 工作台聚合服务实现类
 */
@Service
public class DashboardServiceImpl implements DashboardService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private static final String[] AVATAR_COLORS = {
            "#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"
    };

    @Override
    public DashboardStatsDTO getDashboardStats() {
        DashboardStatsDTO stats = new DashboardStatsDTO();

        // 1. 今日提问数
        Integer todayQuestions = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE",
                Integer.class);
        stats.setTodayQuestions(todayQuestions != null ? todayQuestions : 0);

        // 2. 昨日提问数及增长率
        Integer yesterdayQuestions = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '1 day' AND created_at < CURRENT_DATE",
                Integer.class);
        int yq = yesterdayQuestions != null ? yesterdayQuestions : 0;
        if (yq > 0) {
            stats.setTodayQuestionsGrowth((int) Math.round(((double) stats.getTodayQuestions() - yq) / yq * 100));
        } else {
            stats.setTodayQuestionsGrowth(0);
        }

        // 3. 待审批数
        Integer pendingApprovals = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_classroom_application WHERE is_deleted = FALSE AND status = 0",
                Integer.class);
        stats.setPendingApprovals(pendingApprovals != null ? pendingApprovals : 0);

        // 4. 超48小时未审批（紧急）
        Integer urgentApprovals = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_classroom_application WHERE is_deleted = FALSE AND status = 0 AND created_at < NOW() - INTERVAL '48 hours'",
                Integer.class);
        stats.setUrgentApprovals(urgentApprovals != null ? urgentApprovals : 0);

        // 5. AI 自动解决率 = AI回复数 / 学生提问总数 * 100
        Integer aiReplies = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_message WHERE is_deleted = FALSE AND sender_type = 2",
                Integer.class);
        Integer studentQuestions = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM yx_message WHERE is_deleted = FALSE AND sender_type = 1",
                Integer.class);
        int ai = aiReplies != null ? aiReplies : 0;
        int sq = studentQuestions != null ? studentQuestions : 0;
        stats.setAiResolutionRate(sq > 0 ? (int) Math.round((double) ai / sq * 100) : 0);

        // 6. 平均响应时间（分钟）
        Double avgResponseTime = jdbcTemplate.queryForObject(
                "SELECT AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60) FROM yx_escalation WHERE is_deleted = FALSE AND status = 2 AND resolved_at IS NOT NULL",
                Double.class);
        stats.setAvgResponseTime(avgResponseTime != null ? (int) Math.round(avgResponseTime) : 0);

        // 7. 响应时间改善 = 上周平均 - 本周平均（正数表示提升/缩短）
        Double thisWeekAvg = jdbcTemplate.queryForObject(
                "SELECT AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60) FROM yx_escalation " +
                        "WHERE is_deleted = FALSE AND status = 2 AND resolved_at IS NOT NULL AND resolved_at >= CURRENT_DATE - INTERVAL '7 days'",
                Double.class);
        Double lastWeekAvg = jdbcTemplate.queryForObject(
                "SELECT AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60) FROM yx_escalation " +
                        "WHERE is_deleted = FALSE AND status = 2 AND resolved_at IS NOT NULL AND resolved_at >= CURRENT_DATE - INTERVAL '14 days' AND resolved_at < CURRENT_DATE - INTERVAL '7 days'",
                Double.class);
        double tw = thisWeekAvg != null ? thisWeekAvg : 0;
        double lw = lastWeekAvg != null ? lastWeekAvg : 0;
        if (lw > 0 && tw > 0) {
            stats.setResponseTimeImprovement((int) Math.round(lw - tw));
        } else if (lw > 0 && tw == 0) {
            stats.setResponseTimeImprovement((int) Math.round(lw));
        } else {
            stats.setResponseTimeImprovement(0);
        }

        return stats;
    }

    @Override
    public Map<String, Object> getTodayQuestions(int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;

        String countSql = "SELECT COUNT(*) FROM yx_escalation e LEFT JOIN yx_user u ON e.student_id = u.id " +
                "WHERE e.is_deleted = FALSE AND e.created_at >= CURRENT_DATE";
        Long total = jdbcTemplate.queryForObject(countSql, Long.class);

        String sql = "SELECT e.id, e.created_at, e.question_summary, e.status, e.teacher_id, e.trigger_type, " +
                "u.real_name AS student_name, u.class_name AS student_class, e.student_id " +
                "FROM yx_escalation e LEFT JOIN yx_user u ON e.student_id = u.id " +
                "WHERE e.is_deleted = FALSE AND e.created_at >= CURRENT_DATE " +
                "ORDER BY e.created_at DESC LIMIT ? OFFSET ?";

        List<TodayQuestionDTO> rows = jdbcTemplate.query(sql, new RowMapper<TodayQuestionDTO>() {
            @Override
            public TodayQuestionDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
                TodayQuestionDTO dto = new TodayQuestionDTO();
                dto.setId(rs.getLong("id"));
                Timestamp ts = rs.getTimestamp("created_at");
                if (ts != null) {
                    dto.setTime(ts.toLocalDateTime().format(DateTimeFormatter.ofPattern("HH:mm")));
                }
                dto.setStudentName(rs.getString("student_name"));
                dto.setStudentClass(rs.getString("student_class"));
                Long studentId = rs.getLong("student_id");
                dto.setAvatarColor(AVATAR_COLORS[(int) (studentId % AVATAR_COLORS.length)]);
                dto.setTitle(rs.getString("question_summary"));
                dto.setCategory(resolveCategory(rs.getString("question_summary")));

                int status = rs.getInt("status");
                Long teacherId = rs.getObject("teacher_id", Long.class);
                if (status == 2) {
                    dto.setAiStatus("resolved");
                } else if (status == 1 || (status == 0 && teacherId != null)) {
                    dto.setAiStatus("handled");
                } else {
                    dto.setAiStatus("pending");
                }

                int triggerType = rs.getInt("trigger_type");
                dto.setAiText(triggerType == 2 ? "AI 判断无法回答，已上报" : "学生主动呼叫老师");
                dto.setNeedHandle(status == 0 || status == 1);
                return dto;
            }
        }, pageSize, offset);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total != null ? total : 0L);
        result.put("rows", rows);
        return result;
    }

    @Override
    public List<HotQuestionDTO> getHotQuestions(int limit) {
        String totalSql = "SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE";
        Long total = jdbcTemplate.queryForObject(totalSql, Long.class);
        long t = total != null ? total : 0L;

        String sql = "SELECT question_summary, COUNT(*) AS cnt FROM yx_escalation " +
                "WHERE is_deleted = FALSE GROUP BY question_summary ORDER BY cnt DESC LIMIT ?";

        return jdbcTemplate.query(sql, new RowMapper<HotQuestionDTO>() {
            @Override
            public HotQuestionDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
                HotQuestionDTO dto = new HotQuestionDTO();
                dto.setName(rs.getString("question_summary"));
                int cnt = rs.getInt("cnt");
                dto.setCount(cnt);
                dto.setPercent(t > 0 ? (int) Math.round((double) cnt / t * 100) : 0);
                return dto;
            }
        }, limit);
    }

    @Override
    public List<PendingApprovalDTO> getPendingApprovals(int limit) {
        String sql = "SELECT a.id, a.apply_date, a.start_time, a.end_time, a.purpose, a.created_at, " +
                "c.building, c.room_number " +
                "FROM yx_classroom_application a LEFT JOIN yx_classroom c ON a.classroom_id = c.id " +
                "WHERE a.is_deleted = FALSE AND a.status = 0 ORDER BY a.created_at DESC LIMIT ?";

        return jdbcTemplate.query(sql, new RowMapper<PendingApprovalDTO>() {
            @Override
            public PendingApprovalDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
                PendingApprovalDTO dto = new PendingApprovalDTO();
                dto.setId(String.valueOf(rs.getLong("id")));
                dto.setType("教室申请");

                String building = rs.getString("building");
                String roomNumber = rs.getString("room_number");
                String purpose = rs.getString("purpose");
                if (building != null && roomNumber != null) {
                    dto.setTitle(building + roomNumber + "教室申请");
                } else {
                    dto.setTitle(purpose != null ? purpose : "教室申请");
                }

                java.sql.Date applyDate = rs.getDate("apply_date");
                java.sql.Time startTime = rs.getTime("start_time");
                java.sql.Time endTime = rs.getTime("end_time");
                if (applyDate != null && startTime != null && endTime != null) {
                    dto.setTimeRange(applyDate.toLocalDate() + " " + startTime.toLocalTime() + "~" + endTime.toLocalTime());
                } else {
                    dto.setTimeRange("");
                }

                Timestamp createdAt = rs.getTimestamp("created_at");
                boolean urgent = createdAt != null && createdAt.toLocalDateTime().isBefore(LocalDateTime.now().minusHours(48));
                dto.setUrgent(urgent);
                dto.setRemainingTime(urgent ? "已超48小时" : null);
                return dto;
            }
        }, limit);
    }

    @Override
    public List<AIWarningDTO> getAIWarnings() {
        // 简单实现：近 7 日 vs 前 7 日按关键词统计，增长超过 100% 即预警
        String sql = "SELECT keyword, cur_cnt, pre_cnt FROM ( " +
                "  SELECT '奖学金' AS keyword, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%奖学金%') AS cur_cnt, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '14 days' AND created_at < CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%奖学金%') AS pre_cnt " +
                "  UNION ALL " +
                "  SELECT '选课' AS keyword, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%选课%') AS cur_cnt, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '14 days' AND created_at < CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%选课%') AS pre_cnt " +
                "  UNION ALL " +
                "  SELECT '宿舍' AS keyword, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%宿舍%') AS cur_cnt, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '14 days' AND created_at < CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%宿舍%') AS pre_cnt " +
                "  UNION ALL " +
                "  SELECT '成绩' AS keyword, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%成绩%') AS cur_cnt, " +
                "    (SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE AND created_at >= CURRENT_DATE - INTERVAL '14 days' AND created_at < CURRENT_DATE - INTERVAL '7 days' AND question_summary LIKE '%成绩%') AS pre_cnt " +
                ") t WHERE cur_cnt > 0 AND (pre_cnt = 0 OR cur_cnt > pre_cnt)";

        return jdbcTemplate.query(sql, new RowMapper<AIWarningDTO>() {
            @Override
            public AIWarningDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
                AIWarningDTO dto = new AIWarningDTO();
                dto.setTopic(rs.getString("keyword"));
                int cur = rs.getInt("cur_cnt");
                int pre = rs.getInt("pre_cnt");
                if (pre == 0) {
                    dto.setIncreasePercent(cur > 0 ? 100 : 0);
                } else {
                    dto.setIncreasePercent((int) Math.round(((double) cur - pre) / pre * 100));
                }
                dto.setSuggestion("建议关注该话题的相关政策解读");
                return dto;
            }
        });
    }

    @Override
    public DashboardOverviewDTO getDashboardOverview() {
        DashboardOverviewDTO overview = new DashboardOverviewDTO();
        overview.setStats(getDashboardStats());
        @SuppressWarnings("unchecked")
        Map<String, Object> questionsMap = getTodayQuestions(1, 10);
        overview.setQuestions((List<TodayQuestionDTO>) questionsMap.get("rows"));
        overview.setHotQuestions(getHotQuestions(5));
        overview.setPendingApprovals(getPendingApprovals(5));
        List<AIWarningDTO> warnings = getAIWarnings();
        overview.setAiWarning(warnings.isEmpty() ? null : warnings.get(0));
        return overview;
    }

    /**
     * 根据问题摘要映射分类
     */
    private String resolveCategory(String summary) {
        if (summary == null) {
            return "学业咨询";
        }
        String s = summary.toLowerCase();
        if (s.contains("奖学") || s.contains("助学金") || s.contains("贷款")) {
            return "奖助学金";
        }
        if (s.contains("选课") || s.contains("课程") || s.contains("学分") || s.contains("成绩")) {
            return "学业教务";
        }
        if (s.contains("宿舍") || s.contains("住宿") || s.contains("寝室") || s.contains("水电")) {
            return "住宿生活";
        }
        if (s.contains("教室") || s.contains("自习") || s.contains("图书馆")) {
            return "场地资源";
        }
        if (s.contains("请假") || s.contains("销假") || s.contains("辅导员")) {
            return "日常事务";
        }
        return "学业咨询";
    }
}
