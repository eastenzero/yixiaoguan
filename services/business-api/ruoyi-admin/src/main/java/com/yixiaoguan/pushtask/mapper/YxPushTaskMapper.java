package com.yixiaoguan.pushtask.mapper;

import com.yixiaoguan.pushtask.domain.YxPushTask;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 主动推送任务 Mapper 接口 - 对应 yx_push_task 表
 */
@Mapper
public interface YxPushTaskMapper {

    /**
     * 分页查询推送任务列表
     *
     * @param status   状态（null 则不过滤）
     * @param offset   分页偏移量
     * @param limit    每页条数
     * @return 任务列表
     */
    List<YxPushTask> selectPage(
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计任务总数
     *
     * @param status 状态（null 则不过滤）
     * @return 总条数
     */
    long count(@Param("status") Integer status);

    /**
     * 通过主键查询任务详情
     *
     * @param id 任务 ID
     * @return 任务详情
     */
    YxPushTask selectById(@Param("id") Long id);

    /**
     * 新增推送任务
     *
     * @param task 任务对象
     * @return 影响行数
     */
    int insert(YxPushTask task);

    /**
     * 更新推送任务状态为已发送
     *
     * @param id             任务 ID
     * @param recipientCount 接收人数
     * @return 影响行数
     */
    int updateSentStatus(@Param("id") Long id, @Param("recipientCount") Integer recipientCount);

    /**
     * 更新推送任务状态为已取消
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int updateCancelStatus(@Param("id") Long id);

    /**
     * 更新已读人数
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int incrementReadCount(@Param("id") Long id);

    /**
     * 软删除推送任务
     *
     * @param id 任务 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
