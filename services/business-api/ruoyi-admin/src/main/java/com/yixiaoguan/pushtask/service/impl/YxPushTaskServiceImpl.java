package com.yixiaoguan.pushtask.service.impl;

import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.TypeReference;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.utils.PageUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.notification.domain.YxNotification;
import com.yixiaoguan.notification.service.IYxNotificationService;
import com.yixiaoguan.pushtask.domain.YxPushTask;
import com.yixiaoguan.pushtask.mapper.YxPushTaskMapper;
import com.yixiaoguan.pushtask.service.IYxPushTaskService;
import com.yixiaoguan.user.mapper.YxUserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * 主动推送任务 Service 实现
 */
@Service
public class YxPushTaskServiceImpl implements IYxPushTaskService {

    @Autowired
    private YxPushTaskMapper pushTaskMapper;

    @Autowired
    private YxUserMapper userMapper;

    @Autowired
    private IYxNotificationService notificationService;

    @Override
    public TableDataInfo selectPage(Integer status) {
        // 若依分页规范：显式调用 startPage
        PageUtils.startPage();
        int offset = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() <= 0 ? 0 
                : (com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() - 1) * com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();
        int limit = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();

        List<YxPushTask> list = pushTaskMapper.selectPage(status, offset, limit);
        long total = pushTaskMapper.count(status);

        TableDataInfo result = new TableDataInfo();
        result.setCode(200);
        result.setMsg("查询成功");
        result.setRows(list);
        result.setTotal(total);
        return result;
    }

    @Override
    public YxPushTask selectById(Long id) {
        return pushTaskMapper.selectById(id);
    }

    @Override
    public int insert(YxPushTask task) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        task.setSenderId(currentUser != null ? currentUser.getId() : null);
        task.setStatus(0); // 草稿状态
        task.setRecipientCount(0);
        task.setReadCount(0);
        return pushTaskMapper.insert(task);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int sendTask(Long id) {
        YxPushTask task = pushTaskMapper.selectById(id);
        if (task == null || task.getStatus() != 0) {
            throw new RuntimeException("任务不存在或状态不正确");
        }

        // 查询目标用户列表
        List<Long> userIds = selectTargetUserIds(task.getTargetType(), task.getTargetFilter());
        if (userIds == null || userIds.isEmpty()) {
            throw new RuntimeException("未找到目标用户");
        }

        // 批量生成通知记录
        List<YxNotification> notifications = new ArrayList<>();
        for (Long userId : userIds) {
            YxNotification notification = new YxNotification();
            notification.setUserId(userId);
            notification.setTitle(task.getTitle());
            notification.setContent(task.getContent());
            notification.setType(3); // 推送消息
            notification.setIsRead(false);
            notification.setSenderId(task.getSenderId());
            notification.setPushTaskId(task.getId());
            notification.setCreatedAt(new Date());
            notification.setUpdatedAt(new Date());
            notification.setIsDeleted(false);
            notifications.add(notification);
        }

        // 批量插入通知
        notificationService.batchInsert(notifications);

        // 更新任务状态为已发送
        return pushTaskMapper.updateSentStatus(id, userIds.size());
    }

    @Override
    public int cancelTask(Long id) {
        YxPushTask task = pushTaskMapper.selectById(id);
        if (task == null || task.getStatus() != 0) {
            throw new RuntimeException("任务不存在或状态不正确");
        }
        return pushTaskMapper.updateCancelStatus(id);
    }

    @Override
    public int deleteById(Long id) {
        return pushTaskMapper.deleteById(id);
    }

    @Override
    public List<Long> selectTargetUserIds(Integer targetType, String targetFilter) {
        if (targetType == null) {
            return new ArrayList<>();
        }

        // 1-全体学生 2-指定班级 3-指定用户
        switch (targetType) {
            case 1:
                // 全体学生（查询所有 status=1 且未删除的用户）
                return userMapper.selectAllStudentIds();
            case 2:
                // 指定班级
                if (targetFilter == null || targetFilter.isEmpty()) {
                    return new ArrayList<>();
                }
                try {
                    List<String> classNames = JSON.parseObject(targetFilter, new TypeReference<List<String>>() {});
                    return userMapper.selectIdsByClassNames(classNames);
                } catch (Exception e) {
                    return new ArrayList<>();
                }
            case 3:
                // 指定用户
                if (targetFilter == null || targetFilter.isEmpty()) {
                    return new ArrayList<>();
                }
                try {
                    return JSON.parseObject(targetFilter, new TypeReference<List<Long>>() {});
                } catch (Exception e) {
                    return new ArrayList<>();
                }
            default:
                return new ArrayList<>();
        }
    }
}
