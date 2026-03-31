package com.yixiaoguan.conversation.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.conversation.domain.YxConversation;
import com.yixiaoguan.conversation.mapper.YxConversationMapper;
import com.yixiaoguan.conversation.service.IYxConversationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 会话 Service 实现类
 */
@Service
public class YxConversationServiceImpl implements IYxConversationService {

    @Autowired
    private YxConversationMapper conversationMapper;

    @Override
    public Map<String, Object> selectPageByUserId(Long userId, Integer status, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxConversation> rows = conversationMapper.selectPageByUserId(userId, status, offset, pageSize);
        long total = conversationMapper.countByUserId(userId, status);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxConversation selectById(Long id, Long userId) {
        YxConversation conversation = conversationMapper.selectById(id);
        if (conversation == null) {
            throw new ServiceException("会话不存在");
        }
        // 校验所有权：只有会话归属的学生本人或介入的教师可以查看
        if (!conversation.getUserId().equals(userId)
                && !userId.equals(conversation.getTeacherId())) {
            throw new ServiceException("无权访问该会话");
        }
        return conversation;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxConversation createConversation(Long userId, String title) {
        YxConversation conversation = new YxConversation();
        conversation.setUserId(userId);
        conversation.setTitle(title);
        conversationMapper.insert(conversation);
        return conversation;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateTitle(Long id, Long userId, String title) {
        YxConversation conversation = conversationMapper.selectById(id);
        if (conversation == null) {
            throw new ServiceException("会话不存在");
        }
        if (!conversation.getUserId().equals(userId)) {
            throw new ServiceException("无权修改该会话标题");
        }
        conversationMapper.updateTitle(id, title);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void teacherJoin(Long conversationId, Long teacherId) {
        YxConversation conversation = conversationMapper.selectById(conversationId);
        if (conversation == null) {
            throw new ServiceException("会话不存在");
        }
        // 状态为已关闭时不允许介入
        if (Integer.valueOf(0).equals(conversation.getStatus())) {
            throw new ServiceException("该会话已关闭，无法介入");
        }
        conversationMapper.updateTeacherJoin(conversationId, teacherId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void teacherLeave(Long conversationId, Long teacherId) {
        YxConversation conversation = conversationMapper.selectById(conversationId);
        if (conversation == null) {
            throw new ServiceException("会话不存在");
        }
        // 仅当前介入的教师可以执行离开操作
        if (!teacherId.equals(conversation.getTeacherId())) {
            throw new ServiceException("您未介入该会话，无法执行离开操作");
        }
        conversationMapper.updateTeacherLeave(conversationId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void closeConversation(Long id, Long userId) {
        YxConversation conversation = conversationMapper.selectById(id);
        if (conversation == null) {
            throw new ServiceException("会话不存在");
        }
        if (!conversation.getUserId().equals(userId)) {
            throw new ServiceException("无权关闭该会话");
        }
        conversationMapper.deleteById(id);
    }
}
