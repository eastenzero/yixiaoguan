package com.yixiaoguan.notification.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.common.annotation.YxLog;
import com.yixiaoguan.notification.service.IYxNotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 站内通知 Controller
 * 路由前缀：/api/v1/notifications
 */
@RestController
@RequestMapping("/api/v1/notifications")
public class YxNotificationController extends BaseController {

    @Autowired
    private IYxNotificationService notificationService;

    /**
     * 分页查询当前用户的通知列表
     * GET /api/v1/notifications?isRead=false&pageNum=1&pageSize=10
     */
    @GetMapping
    @YxLog(module = "notification", action = "query")
    public AjaxResult list(@RequestParam(required = false) Boolean isRead) {
        TableDataInfo result = notificationService.selectMyPage(isRead);
        return AjaxResult.success(result);
    }

    /**
     * 查询当前用户的未读通知数量
     * GET /api/v1/notifications/unread-count
     */
    @GetMapping("/unread-count")
    @YxLog(module = "notification", action = "query")
    public AjaxResult countUnread() {
        long count = notificationService.countUnread();
        return AjaxResult.success(count);
    }

    /**
     * 获取通知详情（会自动标记为已读）
     * GET /api/v1/notifications/{id}
     */
    @GetMapping("/{id}")
    @YxLog(module = "notification", action = "query")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(notificationService.selectById(id));
    }

    /**
     * 标记通知为已读
     * POST /api/v1/notifications/{id}/read
     */
    @PostMapping("/{id}/read")
    @YxLog(module = "notification", action = "update", description = "标记通知为已读")
    public AjaxResult markAsRead(@PathVariable Long id) {
        int rows = notificationService.markAsRead(id);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("标记失败或无权操作");
    }

    /**
     * 标记当前用户的所有通知为已读
     * POST /api/v1/notifications/read-all
     */
    @PostMapping("/read-all")
    @YxLog(module = "notification", action = "update", description = "标记所有通知为已读")
    public AjaxResult markAllAsRead() {
        int rows = notificationService.markAllAsRead();
        return AjaxResult.success("已标记 " + rows + " 条通知为已读");
    }

    /**
     * 删除通知（软删除）
     * DELETE /api/v1/notifications/{id}
     */
    @DeleteMapping("/{id}")
    @YxLog(module = "notification", action = "delete")
    public AjaxResult delete(@PathVariable Long id) {
        int rows = notificationService.deleteById(id);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("删除失败或无权操作");
    }
}
