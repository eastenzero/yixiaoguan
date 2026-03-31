package com.yixiaoguan.knowledge.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.knowledge.domain.YxKnowledgeSource;
import com.yixiaoguan.knowledge.service.IYxKnowledgeSourceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 知识来源记录 Controller
 * 路由前缀：/api/v1/knowledge/sources
 */
@RestController
@RequestMapping("/api/v1/knowledge/sources")
public class KnowledgeSourceController {

    @Autowired
    private IYxKnowledgeSourceService sourceService;

    /**
     * 分页查询来源记录
     * GET /api/v1/knowledge/sources?fileName=xxx&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) String fileName,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = sourceService.selectPage(fileName, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取来源记录详情
     * GET /api/v1/knowledge/sources/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(sourceService.selectById(id));
    }

    /**
     * 新增来源记录
     * POST /api/v1/knowledge/sources
     */
    @PostMapping
    public AjaxResult add(@RequestBody YxKnowledgeSource source) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        source.setUploaderId(currentUser.getId());
        sourceService.insert(source);
        return AjaxResult.success();
    }

    /**
     * 更新来源记录
     * PUT /api/v1/knowledge/sources/{id}
     */
    @PutMapping("/{id}")
    public AjaxResult update(@PathVariable Long id, @RequestBody YxKnowledgeSource source) {
        source.setId(id);
        sourceService.update(source);
        return AjaxResult.success();
    }

    /**
     * 删除来源记录（软删除）
     * DELETE /api/v1/knowledge/sources/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        sourceService.deleteById(id);
        return AjaxResult.success();
    }
}
