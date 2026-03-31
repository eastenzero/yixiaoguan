package com.yixiaoguan.notification.mapper;

import com.yixiaoguan.notification.domain.YxNotification;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 站内通知 Mapper 接口 - 对应 yx_notification 表
 */
@Mapper
public interface YxNotificationMapper {

    /**
     * 分页查询用户的通知列表
     *
     * @param userId   用户 ID
     * @param isRead   是否已读（null 则不过滤）
     * @param offset   分页偏移量
     * @param limit    每页条数
     * @return 通知列表
     */
    List<YxNotification> selectPage(
            @Param("userId") Long userId,
            @Param("isRead") Boolean isRead,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计通知总数
     *
     * @param userId   用户 ID
     * @param isRead   是否已读（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("userId") Long userId,
            @Param("isRead") Boolean isRead
    );

    /**
     * 统计用户未读通知数量
     *
     * @param userId 用户 ID
     * @return 未读数量
     */
    long countUnread(@Param("userId") Long userId);

    /**
     * 通过主键查询通知详情
     *
     * @param id 通知 ID
     * @return 通知详情
     */
    YxNotification selectById(@Param("id") Long id);

    /**
     * 批量新增通知
     *
     * @param notifications 通知列表
     * @return 影响行数
     */
    int batchInsert(@Param("list") List<YxNotification> notifications);

    /**
     * 更新通知为已读
     *
     * @param id     通知 ID
     * @param userId 用户 ID（用于校验权限）
     * @return 影响行数
     */
    int markAsRead(@Param("id") Long id, @Param("userId") Long userId);

    /**
     * 批量更新用户的所有未读通知为已读
     *
     * @param userId 用户 ID
     * @return 影响行数
     */
    int markAllAsRead(@Param("userId") Long userId);

    /**
     * 软删除通知
     *
     * @param id     通知 ID
     * @param userId 用户 ID（用于校验权限）
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id, @Param("userId") Long userId);
}
