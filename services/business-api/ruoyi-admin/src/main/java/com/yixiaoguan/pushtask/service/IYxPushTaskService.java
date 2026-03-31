package com.yixiaoguan.pushtask.service;

import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.pushtask.domain.YxPushTask;

import java.util.List;

/**
 * 主动推送任务 Service 接口
 */
public interface IYxPushTaskService {

    /**
     * 分页查询推送任务列表
     *
     * @param status 状态（null 则不过滤）
     * @return 分页数据
     */
    TableDataInfo selectPage(Integer status);

    /**
     * 通过 ID 查询任务详情
     *
     * @param id 任务 ID
     * @return 任务详情
     */
    YxPushTask selectById(Long id);

    /**
     * 新增推送任务（草稿状态）
     *
     * @param task 任务对象
     * @return 影响行数
     */
    int insert(YxPushTask task);

    /**
     * 发送推送任务
     * 将任务状态改为已发送，并批量生成通知记录
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int sendTask(Long id);

    /**
     * 取消推送任务
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int cancelTask(Long id);

    /**
     * 删除推送任务（软删除）
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int deleteById(Long id);

    /**
     * 查询目标用户 ID 列表
     * 根据 targetType 和 targetFilter 查询符合条件的用户
     *
     * @param targetType   目标类型
     * @param targetFilter 目标筛选条件（JSON）
     * @return 用户 ID 列表
     */
    List<Long> selectTargetUserIds(Integer targetType, String targetFilter);
}
