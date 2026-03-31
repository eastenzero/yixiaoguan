package com.yixiaoguan.conversation.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.conversation.domain.YxMessage;
import com.yixiaoguan.conversation.mapper.YxConversationMapper;
import com.yixiaoguan.conversation.mapper.YxMessageMapper;
import com.yixiaoguan.conversation.service.IYxMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 消息 Service 实现类
 */
@Service
public class YxMessageServiceImpl implements IYxMessageService {

    @Autowired
    private YxMessageMapper messageMapper;

    @Autowired
    private YxConversationMapper conversationMapper;

    @Override
    public List<YxMessage> selectHistory(Long conversationId, Long requestUserId) {
        // 校验会话是否存在（校验归属在 ConversationService 中做，这里只做存在性校验）
        if (conversationMapper.selectById(conversationId) == null) {
            throw new ServiceException("会话不存在");
        }
        return messageMapper.selectByConversationId(conversationId);
    }

    @Override
    public Map<String, Object> selectPage(Long conversationId, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxMessage> rows = messageMapper.selectPageByConversationId(conversationId, offset, pageSize);
        long total = messageMapper.countByConversationId(conversationId);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxMessage sendMessage(YxMessage message) {
        // 保存消息
        messageMapper.insert(message);
        // 同步更新会话的最后消息时间和消息计数
        conversationMapper.updateLastMessageInfo(message.getConversationId());
        return message;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxMessage saveAiMessage(Long conversationId, String content, Long parentMessageId,
                                   BigDecimal aiConfidence,
                                   String aiSourceEntryIds, String aiSourceLinkIds) {
        YxMessage message = new YxMessage();
        message.setConversationId(conversationId);
        message.setSenderType(2);         // 2-AI
        message.setSenderId(null);        // AI 消息无发送者用户 ID
        message.setContent(content);
        message.setMessageType(2);        // 默认 Markdown 格式
        message.setParentMessageId(parentMessageId);
        message.setAiConfidence(aiConfidence);
        message.setAiSourceEntryIds(aiSourceEntryIds);
        message.setAiSourceLinkIds(aiSourceLinkIds);

        messageMapper.insert(message);
        conversationMapper.updateLastMessageInfo(conversationId);
        return message;
    }
}
