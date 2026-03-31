package com.yixiaoguan.classroom.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.classroom.domain.YxClassroomApplication;
import com.yixiaoguan.classroom.service.IYxClassroomApplicationService;
import com.yixiaoguan.common.core.domain.YxUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 空教室申请 Controller
 * 路由前缀：/api/v1/classroom-applications
 */
@RestController
@RequestMapping("/api/v1/classroom-applications")
public class ClassroomApplicationController extends BaseController {

    @Autowired
    private IYxClassroomApplicationService applicationService;

    /**
     * 申请列表查询（分页）
     * GET /api/v1/classroom-applications?applicantId=1&status=0&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) Long applicantId,
            @RequestParam(required = false) Long classroomId,
            @RequestParam(required = false) Integer status,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        startPage();
        Map<String, Object> result = applicationService.selectPage(applicantId, classroomId, status, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取申请详情
     * GET /api/v1/classroom-applications/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(applicationService.selectById(id));
    }

    /**
     * 申请提交接口
     * POST /api/v1/classroom-applications
     */
    @PostMapping
    public AjaxResult submit(@RequestBody YxClassroomApplication application) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        YxClassroomApplication saved = applicationService.submitApplication(application, currentUser.getId());
        return AjaxResult.success(saved);
    }

    /**
     * 教师审批接口 - 通过
     * PUT /api/v1/classroom-applications/{id}/approve
     * Body: { "opinion": "批准使用" }
     */
    @PutMapping("/{id}/approve")
    public AjaxResult approve(@PathVariable Long id, @RequestBody(required = false) Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String opinion = (body != null) ? body.get("opinion") : null;
        applicationService.approve(id, currentUser.getId(), opinion);
        return AjaxResult.success();
    }

    /**
     * 教师审批接口 - 拒绝
     * PUT /api/v1/classroom-applications/{id}/reject
     * Body: { "opinion": "该时段已被占用" }
     */
    @PutMapping("/{id}/reject")
    public AjaxResult reject(@PathVariable Long id, @RequestBody Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String opinion = body.get("opinion");
        applicationService.reject(id, currentUser.getId(), opinion);
        return AjaxResult.success();
    }

    /**
     * 取消申请
     * PUT /api/v1/classroom-applications/{id}/cancel
     */
    @PutMapping("/{id}/cancel")
    public AjaxResult cancel(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        applicationService.cancel(id, currentUser.getId());
        return AjaxResult.success();
    }

    /**
     * 删除申请
     * DELETE /api/v1/classroom-applications/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        applicationService.deleteById(id);
        return AjaxResult.success();
    }
}
