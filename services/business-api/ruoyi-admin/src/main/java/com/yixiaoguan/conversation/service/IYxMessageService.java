package com.yixiaoguan.conversation.service;

import com.yixiaoguan.conversation.domain.YxMessage;

import java.util.List;
import java.util.Map;

/**
 * 消息 Service 接口
 */
public interface IYxMessageService {

    /**
     * 查询会话的全量历史消息（正序，初次加载使用）
     * 注意：若消息量极大，建议改用分页接口
     *
     * @param conversationId 会话 ID
     * @param requestUserId  当前登录用户 ID（校验会话归属）
     * @return 消息列表（按 created_at 正序）
     */
    List<YxMessage> selectHistory(Long conversationId, Long requestUserId);

    /**
     * 分页查询历史消息（逆序，用于"查看更多"翻页）
     *
     * @param conversationId 会话 ID
     * @param pageNum        页码（从 1 开始）
     * @param pageSize       每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(Long conversationId, int pageNum, int pageSize);

    /**
     * 发送并保存消息（学生、教师均通过此方法入库）
     * 同时更新所属会话的 last_message_at 和 message_count
     *
     * @param message 消息对象（需含 conversationId、senderType、senderId、content、messageType）
     * @return 保存后的消息对象（含自增 ID 和 createdAt）
     */
    YxMessage sendMessage(YxMessage message);

    /**
     * 保存 AI 回复消息（ai-service 回调时使用，sender_type=2，sender_id=null）
     *
     * @param conversationId    会话 ID
     * @param content           AI 回复内容
     * @param parentMessageId   对应的学生提问消息 ID
     * @param aiConfidence      AI 置信度
     * @param aiSourceEntryIds  命中知识条目 ID（JSON 数组字符串）
     * @param aiSourceLinkIds   推荐快捷链接 ID（JSON 数组字符串）
     * @return 保存后的消息对象
     */
    YxMessage saveAiMessage(Long conversationId, String content, Long parentMessageId,
                            java.math.BigDecimal aiConfidence,
                            String aiSourceEntryIds, String aiSourceLinkIds);
}
