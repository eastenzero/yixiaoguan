package com.yixiaoguan.quicklink.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.yixiaoguan.quicklink.domain.YxQuickLink;
import com.yixiaoguan.quicklink.service.IYxQuickLinkService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 快捷链接库 Controller
 * 路由前缀：/api/v1/quick-links
 */
@RestController
@RequestMapping("/api/v1/quick-links")
public class QuickLinkController extends BaseController {

    @Autowired
    private IYxQuickLinkService quickLinkService;

    /**
     * 快捷链接列表查询（分页）
     * GET /api/v1/quick-links?name=xxx&category=xxx&isActive=true&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) Boolean isActive,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        startPage();
        Map<String, Object> result = quickLinkService.selectPage(name, category, isActive, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取快捷链接详情
     * GET /api/v1/quick-links/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(quickLinkService.selectById(id));
    }

    /**
     * 新增快捷链接
     * POST /api/v1/quick-links
     */
    @PostMapping
    public AjaxResult add(@RequestBody YxQuickLink quickLink) {
        quickLinkService.insert(quickLink);
        return AjaxResult.success();
    }

    /**
     * 更新快捷链接
     * PUT /api/v1/quick-links
     */
    @PutMapping
    public AjaxResult update(@RequestBody YxQuickLink quickLink) {
        quickLinkService.update(quickLink);
        return AjaxResult.success();
    }

    /**
     * 删除快捷链接
     * DELETE /api/v1/quick-links/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        quickLinkService.deleteById(id);
        return AjaxResult.success();
    }

    /**
     * 记录链接点击
     * POST /api/v1/quick-links/{id}/click
     */
    @PostMapping("/{id}/click")
    public AjaxResult click(@PathVariable Long id) {
        quickLinkService.incrementClickCount(id);
        return AjaxResult.success();
    }
}
