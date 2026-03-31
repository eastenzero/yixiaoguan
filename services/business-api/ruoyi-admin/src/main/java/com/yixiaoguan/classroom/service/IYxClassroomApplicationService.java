package com.yixiaoguan.classroom.service;

import com.yixiaoguan.classroom.domain.YxClassroomApplication;

import java.util.List;
import java.util.Map;

/**
 * 空教室申请 Service 接口
 */
public interface IYxClassroomApplicationService {

    /**
     * 分页查询申请列表
     *
     * @param applicantId 申请人 ID（null 则不过滤）
     * @param classroomId 教室 ID（null 则不过滤）
     * @param status      状态（null 则不过滤）
     * @param pageNum     页码（从 1 开始）
     * @param pageSize    每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(Long applicantId, Long classroomId, Integer status, int pageNum, int pageSize);

    /**
     * 通过 ID 查询申请详情
     *
     * @param id 申请 ID
     * @return 申请详情
     */
    YxClassroomApplication selectById(Long id);

    /**
     * 提交申请
     *
     * @param application 申请对象
     * @param applicantId 申请人 ID
     * @return 保存后的申请对象
     */
    YxClassroomApplication submitApplication(YxClassroomApplication application, Long applicantId);

    /**
     * 审批通过
     * 将申请状态改为已通过(1)，同时在 review 表里插入一条记录
     *
     * @param applicationId 申请 ID
     * @param reviewerId    审批人 ID
     * @param opinion       审批意见
     */
    void approve(Long applicationId, Long reviewerId, String opinion);

    /**
     * 审批拒绝
     * 将申请状态改为已拒绝(2)，同时在 review 表里插入一条记录
     *
     * @param applicationId 申请 ID
     * @param reviewerId    审批人 ID
     * @param opinion       审批意见
     */
    void reject(Long applicationId, Long reviewerId, String opinion);

    /**
     * 取消申请
     * 将申请状态改为已取消(3)
     *
     * @param applicationId 申请 ID
     * @param applicantId   申请人 ID（用于校验权限）
     */
    void cancel(Long applicationId, Long applicantId);

    /**
     * 删除申请（软删除）
     *
     * @param id 申请 ID
     */
    void deleteById(Long id);
}
