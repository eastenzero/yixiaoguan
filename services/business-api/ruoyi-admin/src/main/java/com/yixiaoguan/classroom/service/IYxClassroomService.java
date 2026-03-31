package com.yixiaoguan.classroom.service;

import com.yixiaoguan.classroom.domain.YxClassroom;

import java.util.List;
import java.util.Map;

/**
 * 空教室资源 Service 接口
 */
public interface IYxClassroomService {

    /**
     * 分页查询空教室列表
     *
     * @param building 教学楼名称（null 则不过滤）
     * @param status   状态（null 则不过滤）
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(String building, Integer status, int pageNum, int pageSize);

    /**
     * 查询可用空教室列表（供申请时选择）
     *
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectAvailableList(int pageNum, int pageSize);

    /**
     * 通过 ID 查询教室详情
     *
     * @param id 教室 ID
     * @return 教室详情
     */
    YxClassroom selectById(Long id);

    /**
     * 新增教室
     *
     * @param classroom 教室对象
     */
    void insert(YxClassroom classroom);

    /**
     * 更新教室
     *
     * @param classroom 教室对象
     */
    void update(YxClassroom classroom);

    /**
     * 删除教室（软删除）
     *
     * @param id 教室 ID
     */
    void deleteById(Long id);
}
