package com.yixiaoguan.notification.service.impl;

import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.utils.PageUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.notification.domain.YxNotification;
import com.yixiaoguan.notification.mapper.YxNotificationMapper;
import com.yixiaoguan.notification.service.IYxNotificationService;
import com.yixiaoguan.pushtask.mapper.YxPushTaskMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

/**
 * 站内通知 Service 实现
 */
@Service
public class YxNotificationServiceImpl implements IYxNotificationService {

    @Autowired
    private YxNotificationMapper notificationMapper;

    @Autowired
    private YxPushTaskMapper pushTaskMapper;

    @Override
    public TableDataInfo selectMyPage(Boolean isRead) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long userId = currentUser != null ? currentUser.getId() : null;

        // 若依分页规范：显式调用 startPage
        PageUtils.startPage();
        int offset = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() <= 0 ? 0 
                : (com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() - 1) * com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();
        int limit = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();

        List<YxNotification> list = notificationMapper.selectPage(userId, isRead, offset, limit);
        long total = notificationMapper.count(userId, isRead);

        TableDataInfo result = new TableDataInfo();
        result.setCode(200);
        result.setMsg("查询成功");
        result.setRows(list);
        result.setTotal(total);
        return result;
    }

    @Override
    public long countUnread() {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long userId = currentUser != null ? currentUser.getId() : null;
        if (userId == null) {
            return 0;
        }
        return notificationMapper.countUnread(userId);
    }

    @Override
    public YxNotification selectById(Long id) {
        YxNotification notification = notificationMapper.selectById(id);
        if (notification != null && !notification.getIsRead()) {
            // 自动标记为已读
            markAsRead(id);
            notification.setIsRead(true);
            notification.setReadAt(new Date());
        }
        return notification;
    }

    @Override
    public int batchInsert(List<YxNotification> notifications) {
        if (notifications == null || notifications.isEmpty()) {
            return 0;
        }
        return notificationMapper.batchInsert(notifications);
    }

    @Override
    public int markAsRead(Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long userId = currentUser != null ? currentUser.getId() : null;
        if (userId == null) {
            return 0;
        }
        int rows = notificationMapper.markAsRead(id, userId);
        // 更新推送任务的已读数
        if (rows > 0) {
            YxNotification notification = notificationMapper.selectById(id);
            if (notification != null && notification.getPushTaskId() != null) {
                pushTaskMapper.incrementReadCount(notification.getPushTaskId());
            }
        }
        return rows;
    }

    @Override
    public int markAllAsRead() {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long userId = currentUser != null ? currentUser.getId() : null;
        if (userId == null) {
            return 0;
        }
        return notificationMapper.markAllAsRead(userId);
    }

    @Override
    public int deleteById(Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Long userId = currentUser != null ? currentUser.getId() : null;
        if (userId == null) {
            return 0;
        }
        return notificationMapper.deleteById(id, userId);
    }
}
