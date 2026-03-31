package com.yixiaoguan.conversation.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.conversation.domain.YxEscalation;
import com.yixiaoguan.conversation.mapper.YxEscalationMapper;
import com.yixiaoguan.conversation.service.IYxEscalationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 问题上报工单 Service 实现类
 */
@Service
public class YxEscalationServiceImpl implements IYxEscalationService {

    @Autowired
    private YxEscalationMapper escalationMapper;

    @Override
    public YxEscalation selectById(Long id) {
        YxEscalation escalation = escalationMapper.selectById(id);
        if (escalation == null) {
            throw new ServiceException("工单不存在");
        }
        return escalation;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxEscalation createEscalation(Long conversationId, Long messageId,
                                          Long studentId, String questionSummary, Integer priority) {
        YxEscalation escalation = new YxEscalation();
        escalation.setConversationId(conversationId);
        escalation.setMessageId(messageId);
        escalation.setStudentId(studentId);
        escalation.setQuestionSummary(questionSummary);
        escalation.setPriority(priority != null ? priority : 1); // 默认中优先级
        escalation.setTriggerType(1); // 1-学生主动呼叫
        escalationMapper.insert(escalation);
        return escalation;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxEscalation createAutoEscalation(Long conversationId, Long messageId,
                                              Long studentId, String questionSummary) {
        YxEscalation escalation = new YxEscalation();
        escalation.setConversationId(conversationId);
        escalation.setMessageId(messageId);
        escalation.setStudentId(studentId);
        escalation.setQuestionSummary(questionSummary);
        escalation.setPriority(1); // 默认中优先级
        escalation.setTriggerType(2); // 2-AI 判断上报
        escalationMapper.insert(escalation);
        return escalation;
    }

    @Override
    public Map<String, Object> selectPendingPage(int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxEscalation> rows = escalationMapper.selectPendingPage(offset, pageSize);
        long total = escalationMapper.countPending();

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public Map<String, Object> selectPageByTeacher(Long teacherId, Integer status, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxEscalation> rows = escalationMapper.selectPageByTeacherId(teacherId, status, offset, pageSize);
        long total = escalationMapper.countByTeacherId(teacherId, status);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public Map<String, Object> selectPageByStudent(Long studentId, Integer status, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxEscalation> rows = escalationMapper.selectPageByStudentId(studentId, status, offset, pageSize);
        long total = escalationMapper.countByStudentId(studentId, status);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void assignTeacher(Long id, Long teacherId) {
        YxEscalation escalation = escalationMapper.selectById(id);
        if (escalation == null) {
            throw new ServiceException("工单不存在");
        }
        if (escalation.getStatus() != 0) {
            throw new ServiceException("该工单已被处理，无法重复接单");
        }
        escalationMapper.assignTeacher(id, teacherId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void resolve(Long id, Long teacherId, String teacherReply) {
        YxEscalation escalation = escalationMapper.selectById(id);
        if (escalation == null) {
            throw new ServiceException("工单不存在");
        }
        if (!teacherId.equals(escalation.getTeacherId())) {
            throw new ServiceException("无权操作该工单");
        }
        if (escalation.getStatus() > 1) {
            throw new ServiceException("工单已结案，无法再次回复");
        }
        escalationMapper.resolve(id, teacherReply);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void close(Long id, Long operatorId) {
        YxEscalation escalation = escalationMapper.selectById(id);
        if (escalation == null) {
            throw new ServiceException("工单不存在");
        }
        if (escalation.getStatus() >= 2) {
            throw new ServiceException("工单已结案，无法关闭");
        }
        escalationMapper.updateStatus(id, 3); // 3-已关闭
    }
}
