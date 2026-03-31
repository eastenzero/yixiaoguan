package com.yixiaoguan.aipersona.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.aipersona.domain.YxAiPersona;
import com.yixiaoguan.aipersona.service.IYxAiPersonaService;
import com.yixiaoguan.common.annotation.YxLog;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * AI 人设配置 Controller
 * 路由前缀：/api/v1/ai-personas
 */
@RestController
@RequestMapping("/api/v1/ai-personas")
public class YxAiPersonaController extends BaseController {

    @Autowired
    private IYxAiPersonaService aiPersonaService;

    /**
     * 分页查询 AI 人设列表
     * GET /api/v1/ai-personas?teacherId=1&status=1&pageNum=1&pageSize=10
     */
    @GetMapping
    @YxLog(module = "aiPersona", action = "query")
    public AjaxResult list(
            @RequestParam(required = false) Long teacherId,
            @RequestParam(required = false) Integer status) {
        TableDataInfo result = aiPersonaService.selectPage(teacherId, status);
        return AjaxResult.success(result);
    }

    /**
     * 获取 AI 人设详情
     * GET /api/v1/ai-personas/{id}
     */
    @GetMapping("/{id}")
    @YxLog(module = "aiPersona", action = "query")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(aiPersonaService.selectById(id));
    }

    /**
     * 获取教师的 AI 人设
     * GET /api/v1/ai-personas/teacher/{teacherId}
     */
    @GetMapping("/teacher/{teacherId}")
    @YxLog(module = "aiPersona", action = "query")
    public AjaxResult getByTeacherId(@PathVariable Long teacherId) {
        return AjaxResult.success(aiPersonaService.selectByTeacherId(teacherId));
    }

    /**
     * 获取系统默认人设
     * GET /api/v1/ai-personas/default
     */
    @GetMapping("/default")
    @YxLog(module = "aiPersona", action = "query")
    public AjaxResult getDefault() {
        return AjaxResult.success(aiPersonaService.selectDefault());
    }

    /**
     * 新增 AI 人设
     * POST /api/v1/ai-personas
     */
    @PostMapping
    @YxLog(module = "aiPersona", action = "create", description = "新增 AI 人设")
    public AjaxResult add(@RequestBody YxAiPersona persona) {
        int rows = aiPersonaService.insert(persona);
        return rows > 0 ? AjaxResult.success(persona) : AjaxResult.error("创建失败");
    }

    /**
     * 更新 AI 人设
     * PUT /api/v1/ai-personas
     */
    @PutMapping
    @YxLog(module = "aiPersona", action = "update", description = "更新 AI 人设")
    public AjaxResult edit(@RequestBody YxAiPersona persona) {
        int rows = aiPersonaService.update(persona);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("更新失败");
    }

    /**
     * 更新 AI 人设状态
     * POST /api/v1/ai-personas/{id}/status?status=0
     */
    @PostMapping("/{id}/status")
    @YxLog(module = "aiPersona", action = "update", description = "更新 AI 人设状态")
    public AjaxResult updateStatus(@PathVariable Long id, @RequestParam Integer status) {
        int rows = aiPersonaService.updateStatus(id, status);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("更新失败");
    }

    /**
     * 删除 AI 人设（软删除）
     * DELETE /api/v1/ai-personas/{id}
     */
    @DeleteMapping("/{id}")
    @YxLog(module = "aiPersona", action = "delete")
    public AjaxResult delete(@PathVariable Long id) {
        int rows = aiPersonaService.deleteById(id);
        return rows > 0 ? AjaxResult.success() : AjaxResult.error("删除失败");
    }
}
