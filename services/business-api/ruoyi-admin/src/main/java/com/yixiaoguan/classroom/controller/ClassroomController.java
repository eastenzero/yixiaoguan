package com.yixiaoguan.classroom.controller;

import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.yixiaoguan.classroom.domain.YxClassroom;
import com.yixiaoguan.classroom.service.IYxClassroomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 空教室资源 Controller
 * 路由前缀：/api/v1/classrooms
 */
@RestController
@RequestMapping("/api/v1/classrooms")
public class ClassroomController extends BaseController {

    @Autowired
    private IYxClassroomService classroomService;

    /**
     * 空教室列表查询（分页）
     * GET /api/v1/classrooms?building=xxx&status=1&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult list(
            @RequestParam(required = false) String building,
            @RequestParam(required = false) Integer status,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        // 注意：不调用 startPage()，Service 已通过 LIMIT/OFFSET 手动分页
        Map<String, Object> result = classroomService.selectPage(building, status, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 查询可用空教室列表（供申请时选择）
     * GET /api/v1/classrooms/available?pageNum=1&pageSize=10
     */
    @GetMapping("/available")
    public AjaxResult availableList(
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        // 注意：不调用 startPage()，Service 已通过 LIMIT/OFFSET 手动分页
        Map<String, Object> result = classroomService.selectAvailableList(pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取教室详情
     * GET /api/v1/classrooms/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable Long id) {
        return AjaxResult.success(classroomService.selectById(id));
    }

    /**
     * 新增教室
     * POST /api/v1/classrooms
     */
    @PostMapping
    public AjaxResult add(@RequestBody YxClassroom classroom) {
        classroomService.insert(classroom);
        return AjaxResult.success();
    }

    /**
     * 更新教室
     * PUT /api/v1/classrooms
     */
    @PutMapping
    public AjaxResult update(@RequestBody YxClassroom classroom) {
        classroomService.update(classroom);
        return AjaxResult.success();
    }

    /**
     * 删除教室
     * DELETE /api/v1/classrooms/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult delete(@PathVariable Long id) {
        classroomService.deleteById(id);
        return AjaxResult.success();
    }
}
