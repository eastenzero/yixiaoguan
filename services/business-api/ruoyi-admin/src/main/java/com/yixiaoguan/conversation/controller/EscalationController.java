package com.yixiaoguan.conversation.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.conversation.domain.YxEscalation;
import com.yixiaoguan.conversation.service.IYxEscalationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 问题上报工单 Controller
 * 路由前缀：/api/v1/escalations
 */
@RestController
@RequestMapping("/api/v1/escalations")
public class EscalationController {

    @Autowired
    private IYxEscalationService escalationService;

    /**
     * 学生主动呼叫老师（上报工单，trigger_type=1）
     * POST /api/v1/escalations
     * Body: { "conversationId": 1, "messageId": 2, "questionSummary": "xxx", "priority": 1 }
     */
    @PostMapping
    public AjaxResult createEscalation(@RequestBody Map<String, Object> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long conversationId = Long.parseLong(body.get("conversationId").toString());
        Long messageId = Long.parseLong(body.get("messageId").toString());
        String questionSummary = (String) body.get("questionSummary");
        Object p = body.get("priority");
        Integer priority = p != null ? ((Number) p).intValue() : 1;

        YxEscalation escalation = escalationService.createEscalation(
                conversationId, messageId, currentUser.getId(), questionSummary, priority);
        return AjaxResult.success(escalation);
    }

    /**
     * AI 判断自动上报（trigger_type=2），供 ai-service 内部调用
     * POST /api/v1/escalations/auto
     * Body: { "conversationId": 1, "messageId": 2, "studentId": 3, "questionSummary": "xxx" }
     */
    @PostMapping("/auto")
    public AjaxResult createAutoEscalation(@RequestBody Map<String, Object> body) {
        Long conversationId = Long.parseLong(body.get("conversationId").toString());
        Long messageId = Long.parseLong(body.get("messageId").toString());
        Long studentId = Long.parseLong(body.get("studentId").toString());
        String questionSummary = (String) body.get("questionSummary");

        YxEscalation escalation = escalationService.createAutoEscalation(
                conversationId, messageId, studentId, questionSummary);
        return AjaxResult.success(escalation);
    }

    /**
     * 查询工单详情
     * GET /api/v1/escalations/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getEscalation(@PathVariable Long id) {
        return AjaxResult.success(escalationService.selectById(id));
    }

    /**
     * 学生查看自己的工单列表（分页）
     * GET /api/v1/escalations/my?status=0&pageNum=1&pageSize=10
     */
    @GetMapping("/my")
    public AjaxResult listMyEscalations(
            @RequestParam(required = false) Integer status,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Map<String, Object> result = escalationService.selectPageByStudent(
                currentUser.getId(), status, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 教师查看待处理工单（status=0，未分配）
     * GET /api/v1/escalations/pending?pageNum=1&pageSize=10
     */
    @GetMapping("/pending")
    public AjaxResult listPendingEscalations(
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = escalationService.selectPendingPage(pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 教师查看已分配给自己的工单（分页）
     * GET /api/v1/escalations/assigned?status=1&pageNum=1&pageSize=10
     */
    @GetMapping("/assigned")
    public AjaxResult listAssignedEscalations(
            @RequestParam(required = false) Integer status,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Map<String, Object> result = escalationService.selectPageByTeacher(
                currentUser.getId(), status, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 教师接单（状态 0→1）
     * PUT /api/v1/escalations/{id}/assign
     */
    @PutMapping("/{id}/assign")
    public AjaxResult assignEscalation(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        escalationService.assignTeacher(id, currentUser.getId());
        return AjaxResult.success();
    }

    /**
     * 教师回复并解决工单（状态 1→2）
     * PUT /api/v1/escalations/{id}/resolve
     * Body: { "teacherReply": "xxx" }
     */
    @PutMapping("/{id}/resolve")
    public AjaxResult resolveEscalation(@PathVariable Long id,
                                         @RequestBody Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String teacherReply = body.get("teacherReply");
        escalationService.resolve(id, currentUser.getId(), teacherReply);
        return AjaxResult.success();
    }

    /**
     * 关闭工单（状态 → 3）
     * PUT /api/v1/escalations/{id}/close
     */
    @PutMapping("/{id}/close")
    public AjaxResult closeEscalation(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        escalationService.close(id, currentUser.getId());
        return AjaxResult.success();
    }
}
