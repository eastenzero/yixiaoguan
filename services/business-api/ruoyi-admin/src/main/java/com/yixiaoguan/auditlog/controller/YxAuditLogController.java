package com.yixiaoguan.auditlog.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.auditlog.domain.YxAuditLog;
import com.yixiaoguan.auditlog.service.IYxAuditLogService;
import com.yixiaoguan.common.annotation.YxLog;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 审计日志 Controller
 * 路由前缀：/api/v1/audit-logs
 * 
 * 注意：审计日志只提供查询接口，不提供增删改接口
 */
@RestController
@RequestMapping("/api/v1/audit-logs")
public class YxAuditLogController extends BaseController {

    @Autowired
    private IYxAuditLogService auditLogService;

    /**
     * 分页查询审计日志列表
     * GET /api/v1/audit-logs?userId=1&module=knowledge&action=create&pageNum=1&pageSize=10
     */
    @GetMapping
    @YxLog(module = "auditLog", action = "query")
    public AjaxResult list(
            @RequestParam(required = false) Long userId,
            @RequestParam(required = false) String module,
            @RequestParam(required = false) String action) {
        TableDataInfo result = auditLogService.selectPage(userId, module, action);
        return AjaxResult.success(result);
    }

    /**
     * 获取审计日志详情
     * GET /api/v1/audit-logs/{id}
     */
    @GetMapping("/{id}")
    @YxLog(module = "auditLog", action = "query")
    public AjaxResult getById(@PathVariable Long id) {
        YxAuditLog auditLog = auditLogService.selectById(id);
        return AjaxResult.success(auditLog);
    }
}
