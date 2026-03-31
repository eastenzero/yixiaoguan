package com.yixiaoguan.notification.service;

import com.ruoyi.common.core.page.TableDataInfo;
import com.yixiaoguan.notification.domain.YxNotification;

import java.util.List;

/**
 * 站内通知 Service 接口
 */
public interface IYxNotificationService {

    /**
     * 分页查询当前用户的通知列表
     *
     * @param isRead 是否已读（null 则不过滤）
     * @return 分页数据
     */
    TableDataInfo selectMyPage(Boolean isRead);

    /**
     * 查询当前用户的未读通知数量
     *
     * @return 未读数量
     */
    long countUnread();

    /**
     * 通过 ID 查询通知详情
     *
     * @param id 通知 ID
     * @return 通知详情
     */
    YxNotification selectById(Long id);

    /**
     * 批量新增通知
     *
     * @param notifications 通知列表
     * @return 影响行数
     */
    int batchInsert(List<YxNotification> notifications);

    /**
     * 标记通知为已读
     *
     * @param id 通知 ID
     * @return 影响行数
     */
    int markAsRead(Long id);

    /**
     * 标记当前用户的所有通知为已读
     *
     * @return 影响行数
     */
    int markAllAsRead();

    /**
     * 删除通知（软删除）
     *
     * @param id 通知 ID
     * @return 影响行数
     */
    int deleteById(Long id);
}
