package com.yixiaoguan.pushtask.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.common.annotation.YxLog;
import com.yixiaoguan.pushtask.domain.YxPushTask;
import com.yixiaoguan.pushtask.service.IYxPushTaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 主动推送任务 Controller
 * 路由前缀：/api/v1/push-tasks
 */
@RestController
@RequestMapping("/api/v1/push-tasks")
public class YxPushTaskController extends BaseController {

    @Autowired
    private IYxPushTaskService pushTaskService;

    /**
     * 分页查询推送任务列表
     * GET /api/v1/push-tasks?status=0&pageNum=1&pageSize=10
     */
    @GetMapping
    @YxLog(module = "pushTask", action = "query")
    public AjaxResult list(@RequestParam(required = false) Integer status) {
        TableDataInfo result = pushTaskService.selectPage(status);
        return AjaxResult.success(result);
    }

    /**
     * 获取推送任务详情
     * GET /api/v1/push-tasks/{id}
     */
    @GetMapping("/{id}")
    @YxLog(module = "pushTask", action = "query")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(pushTaskService.selectById(id));
    }

    /**
     * 创建推送任务（草稿）
     * POST /api/v1/push-tasks
     */
    @PostMapping
    @YxLog(module = "pushTask", action = "create", description = "创建推送任务")
    public AjaxResult add(@RequestBody YxPushTask task) {
        int rows = pushTaskService.insert(task);
        return rows > 0 ? AjaxResult.success(task) : AjaxResult.error("创建失败");
    }

    /**
     * 发送推送任务
     * POST /api/v1/push-tasks/{id}/send
     */
    @PostMapping("/{id}/send")
    @YxLog(module = "pushTask", action = "update", description = "发送推送任务")
    public AjaxResult send(@PathVariable Long id) {
        try {
            int rows = pushTaskService.sendTask(id);
            return rows > 0 ? AjaxResult.success("发送成功") : AjaxResult.error("发送失败");
        } catch (RuntimeException e) {
            return AjaxResult.error(e.getMessage());
        }
    }

    /**
     * 取消推送任务
     * POST /api/v1/push-tasks/{id}/cancel
     */
    @PostMapping("/{id}/cancel")
    @YxLog(module = "pushTask", action = "update", description = "取消推送任务")
    public AjaxResult cancel(@PathVariable Long id) {
        try {
            int rows = pushTaskService.cancelTask(id);
            return rows > 0 ? AjaxResult.success("取消成功") : AjaxResult.error("取消失败");
        } catch (RuntimeException e) {
            return AjaxResult.error(e.getMessage());
        }
    }

    /**
     * 删除推送任务（软删除）
     * DELETE /api/v1/push-tasks/{id}
     */
    @DeleteMapping("/{id}")
    @YxLog(module = "pushTask", action = "delete")
    public AjaxResult delete(@PathVariable Long id) {
        int rows = pushTaskService.deleteById(id);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("删除失败");
    }
}
