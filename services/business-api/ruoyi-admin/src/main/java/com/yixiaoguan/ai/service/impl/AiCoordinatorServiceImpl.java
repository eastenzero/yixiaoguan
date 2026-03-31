package com.yixiaoguan.ai.service.impl;

import com.alibaba.fastjson2.JSON;
import com.yixiaoguan.ai.client.AiServiceClient;
import com.yixiaoguan.ai.dto.*;
import com.yixiaoguan.ai.enums.IntentType;
import com.yixiaoguan.ai.service.IAiCoordinatorService;
import com.yixiaoguan.classroom.domain.YxClassroomApplication;
import com.yixiaoguan.classroom.service.IYxClassroomApplicationService;
import com.yixiaoguan.conversation.domain.YxMessage;
import com.yixiaoguan.conversation.service.IYxMessageService;
import com.yixiaoguan.websocket.domain.WsMessagePacket;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.CompletableFuture;

/**
 * AI 协调服务实现
 * 智能网关：意图识别 + 分支调度 + 流式推送
 */
@Service
public class AiCoordinatorServiceImpl implements IAiCoordinatorService {

    private static final Logger log = LoggerFactory.getLogger(AiCoordinatorServiceImpl.class);

    @Autowired
    private AiServiceClient aiClient;

    @Autowired
    private IYxMessageService messageService;

    @Autowired
    private IYxClassroomApplicationService classroomAppService;

    // ==================== 核心入口 ====================

    @Override
    public void processStudentMessage(Long userId, Long conversationId, String message, WebSocketSession session) {
        log.info("[AiCoordinator] 处理学生消息 - userId:{}, conversationId:{}, message:{}",
                userId, conversationId, message.substring(0, Math.min(50, message.length())));

        try {
            // ========== 步骤1：意图提取 ==========
            IntentExtractResponse intentResponse = aiClient.extractIntent(message);

            if (!intentResponse.isSuccess()) {
                log.warn("[AiCoordinator] 意图提取失败: {}", intentResponse.getMsg());
                sendErrorToUser(session, conversationId, "服务暂时不可用，请稍后重试");
                return;
            }

            IntentType intentType = intentResponse.getIntentType();
            log.info("[AiCoordinator] 识别意图: {}, 置信度: {}",
                    intentType, intentResponse.getData() != null ? intentResponse.getData().getConfidence() : "N/A");

            // ========== 步骤2：分支处理 ==========
            if (!intentResponse.isServiceIntent() || intentType == IntentType.CHAT) {
                // ===== 分支 A：普通聊天 -> 流式 RAG =====
                handleChatIntent(userId, conversationId, message, session);
            } else {
                // ===== 分支 B：办事意图 =====
                handleServiceIntent(userId, conversationId, message, intentResponse, session);
            }

        } catch (Exception e) {
            log.error("[AiCoordinator] 处理消息异常: {}", e.getMessage(), e);
            sendErrorToUser(session, conversationId, "处理消息时出现错误，请稍后重试");
        }
    }

    // ==================== 分支 A：普通聊天（流式 RAG）====================

    /**
     * 处理普通聊天意图：调用 /api/chat/stream 并流式推送到 WebSocket
     */
    private void handleChatIntent(Long userId, Long conversationId, String query, WebSocketSession session) {
        log.info("[AiCoordinator] 进入聊天分支 - conversationId:{}", conversationId);

        // 构造请求（可扩展传入历史记录）
        ChatStreamRequest request = new ChatStreamRequest(query);

        // 先落库用户消息
        saveMessage(conversationId, 1, userId, query, 1);

        // 创建 AI 回复消息占位（存库后获取ID用于后续更新或关联）
        YxMessage aiMessage = new YxMessage();
        aiMessage.setConversationId(conversationId);
        aiMessage.setSenderType(2); // 2-AI
        aiMessage.setSenderId(0L);  // AI 无用户ID
        aiMessage.setContent("");   // 先空，流式接收
        aiMessage.setMessageType(1);
        YxMessage savedAiMessage = messageService.sendMessage(aiMessage);

        // 向客户端发送"AI开始回复"标记
        sendTypingIndicator(session, conversationId, savedAiMessage.getId(), true);

        // 累积完整回复内容
        StringBuilder fullResponse = new StringBuilder();
        List<SourceItemDTO> sources = new ArrayList<>();

        // 调用流式接口
        CompletableFuture<Void> future = aiClient.streamChat(request, chunk -> {
            if (chunk.hasError()) {
                log.error("[AiCoordinator] 流式响应错误: {}", chunk.getError());
                sendErrorToUser(session, conversationId, "AI生成回复时出现错误");
                return;
            }

            if (chunk.isEnd()) {
                // 流结束，更新数据库中的完整内容
                updateAiMessage(savedAiMessage.getId(), fullResponse.toString());
                sendTypingIndicator(session, conversationId, savedAiMessage.getId(), false);
                log.info("[AiCoordinator] 流式回复完成 - 总长度:{}", fullResponse.length());
                return;
            }

            // 累积内容
            fullResponse.append(chunk.getChunk());

            // 首次收到 sources 时保存
            if (!chunk.getSources().isEmpty() && sources.isEmpty()) {
                sources.addAll(chunk.getSources());
            }

            // 实时推送到客户端（打字机效果）
            sendStreamChunk(session, conversationId, savedAiMessage.getId(),
                    chunk.getChunk(), sources, false);
        });

        // 可选：等待完成（异步场景下通常不需要阻塞）
        // future.join();
    }

    // ==================== 分支 B：办事意图 ====================

    /**
     * 处理办事意图：根据意图类型路由到对应的业务逻辑
     */
    private void handleServiceIntent(Long userId, Long conversationId, String originalMessage,
                                     IntentExtractResponse intentResponse, WebSocketSession session) {
        IntentType intentType = intentResponse.getIntentType();
        log.info("[AiCoordinator] 进入办事分支 - intent:{}", intentType);

        switch (intentType) {
            case BOOK_CLASSROOM:
                handleBookClassroom(userId, conversationId, intentResponse, session);
                break;
            case SUBMIT_REPAIR_REQUEST:
            case QUERY_APPLICATION_STATUS:
                // 预留的其他办事意图
                sendSystemMessage(session, conversationId,
                        "该业务功能正在开发中，请先通过网页端办理。", "SERVICE_NOT_IMPLEMENTED");
                break;
            default:
                // 未知办事意图降级为聊天
                handleChatIntent(userId, conversationId, originalMessage, session);
        }
    }

    /**
     * 处理预约教室意图
     */
    private void handleBookClassroom(Long userId, Long conversationId,
                                     IntentExtractResponse intentResponse, WebSocketSession session) {
        Map<String, Object> params = intentResponse.getParameters();
        List<String> missing = intentResponse.getMissingRequired();

        log.info("[AiCoordinator] 预约教室 - params:{}, missing:{}", params, missing);

        // ========== 情况1：有缺失必填参数 -> 追问 ==========
        if (intentResponse.hasMissingRequired()) {
            String reply = intentResponse.getReplyToUser();
            if (reply == null || reply.isBlank()) {
                reply = "我需要更多信息来完成预约：" + String.join("、", missing);
            }
            // 以 AI 身份发送追问
            sendAiReply(userId, conversationId, reply, session);
            return;
        }

        // ========== 情况2：参数完整 -> 执行业务 ==========
        try {
            YxClassroomApplication application = buildApplicationFromParams(userId, params);

            // 提交申请
            YxClassroomApplication saved = classroomAppService.submitApplication(application, userId);

            // 构造成功回复
            String successReply = String.format(
                    "✅ 预约申请已提交成功！\n" +
                    "📍 教室：%s %s\n" +
                    "📅 日期：%s\n" +
                    "⏰ 时间：%s - %s\n" +
                    "📝 用途：%s\n" +
                    "申请ID：%d\n" +
                    "请耐心等待管理员审核，您可以在「我的申请」中查看进度。",
                    params.getOrDefault("building", "待分配"),
                    params.getOrDefault("room_number", ""),
                    params.getOrDefault("date", ""),
                    params.getOrDefault("start_time", ""),
                    params.getOrDefault("end_time", ""),
                    params.getOrDefault("purpose", ""),
                    saved.getId()
            );

            sendAiReply(userId, conversationId, successReply, session);

        } catch (Exception e) {
            log.error("[AiCoordinator] 提交教室申请失败: {}", e.getMessage(), e);
            sendAiReply(userId, conversationId,
                    "抱歉，提交申请时出现错误：" + e.getMessage() + "\n请稍后重试或联系管理员。", session);
        }
    }

    /**
     * 从参数构造教室申请对象
     */
    private YxClassroomApplication buildApplicationFromParams(Long userId, Map<String, Object> params)
            throws ParseException {
        YxClassroomApplication app = new YxClassroomApplication();
        app.setApplicantId(userId);

        // 用途
        if (params.containsKey("purpose")) {
            app.setPurpose((String) params.get("purpose"));
        }

        // 日期解析
        if (params.containsKey("date")) {
            String dateStr = (String) params.get("date");
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            app.setApplyDate(sdf.parse(dateStr));
        }

        // 开始时间解析
        if (params.containsKey("start_time")) {
            String timeStr = (String) params.get("start_time");
            app.setStartTime(parseTime(timeStr, app.getApplyDate()));
        }

        // 结束时间解析
        if (params.containsKey("end_time")) {
            String timeStr = (String) params.get("end_time");
            app.setEndTime(parseTime(timeStr, app.getApplyDate()));
        }

        // 人数
        if (params.containsKey("attendee_count")) {
            Object count = params.get("attendee_count");
            if (count instanceof Number) {
                app.setAttendeeCount(((Number) count).intValue());
            } else if (count instanceof String) {
                app.setAttendeeCount(Integer.parseInt((String) count));
            }
        }

        // 联系电话
        if (params.containsKey("contact_phone")) {
            app.setContactPhone((String) params.get("contact_phone"));
        }

        return app;
    }

    private Date parseTime(String timeStr, Date baseDate) throws ParseException {
        if (timeStr == null || timeStr.isBlank()) {
            return null;
        }
        SimpleDateFormat timeSdf = new SimpleDateFormat("HH:mm");
        Date time = timeSdf.parse(timeStr);

        if (baseDate != null) {
            // 合并日期和时间
            Calendar dateCal = Calendar.getInstance();
            dateCal.setTime(baseDate);

            Calendar timeCal = Calendar.getInstance();
            timeCal.setTime(time);

            dateCal.set(Calendar.HOUR_OF_DAY, timeCal.get(Calendar.HOUR_OF_DAY));
            dateCal.set(Calendar.MINUTE, timeCal.get(Calendar.MINUTE));

            return dateCal.getTime();
        }
        return time;
    }

    // ==================== WebSocket 推送工具方法 ====================

    /**
     * 发送流式片段到客户端
     */
    private void sendStreamChunk(WebSocketSession session, Long conversationId,
                                  Long messageId, String chunk,
                                  List<SourceItemDTO> sources, boolean isEnd) {
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType("AI_STREAM_CHUNK");
        packet.setConversationId(conversationId);
        packet.setMessageId(messageId);
        packet.setContent(chunk);
        packet.setSenderType(2); // AI
        packet.setExtra(JSON.toJSONString(Map.of(
                "isEnd", isEnd,
                "sources", sources
        )));
        sendPacket(session, packet);
    }

    /**
     * 发送打字机指示器
     */
    private void sendTypingIndicator(WebSocketSession session, Long conversationId,
                                      Long messageId, boolean start) {
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType(start ? "AI_TYPING_START" : "AI_TYPING_END");
        packet.setConversationId(conversationId);
        packet.setMessageId(messageId);
        packet.setSenderType(2);
        sendPacket(session, packet);
    }

    /**
     * 发送错误消息
     */
    private void sendErrorToUser(WebSocketSession session, Long conversationId, String error) {
        sendSystemMessage(session, conversationId, error, "ERROR");
    }

    /**
     * 发送系统消息
     */
    private void sendSystemMessage(WebSocketSession session, Long conversationId,
                                    String content, String extra) {
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType("SYSTEM_NOTIFY");
        packet.setConversationId(conversationId);
        packet.setContent(content);
        packet.setSenderType(4); // 系统
        packet.setExtra(extra);
        sendPacket(session, packet);
    }

    /**
     * 发送 AI 回复（落库+推送）
     */
    private void sendAiReply(Long userId, Long conversationId, String content, WebSocketSession session) {
        // 落库
        YxMessage message = new YxMessage();
        message.setConversationId(conversationId);
        message.setSenderType(2); // AI
        message.setSenderId(0L);
        message.setContent(content);
        message.setMessageType(1);
        YxMessage saved = messageService.sendMessage(message);

        // 推送
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType("CHAT_MESSAGE");
        packet.setConversationId(conversationId);
        packet.setMessageId(saved.getId());
        packet.setContent(content);
        packet.setSenderType(2);
        packet.setSenderName("医小管");
        sendPacket(session, packet);
    }

    private void sendPacket(WebSocketSession session, WsMessagePacket packet) {
        if (session == null || !session.isOpen()) {
            return;
        }
        try {
            synchronized (session) {
                session.sendMessage(new TextMessage(JSON.toJSONString(packet)));
            }
        } catch (IOException e) {
            log.error("[AiCoordinator] WebSocket发送失败: {}", e.getMessage());
        }
    }

    // ==================== 数据库操作 ====================

    private void saveMessage(Long conversationId, int senderType, Long senderId,
                              String content, int messageType) {
        YxMessage message = new YxMessage();
        message.setConversationId(conversationId);
        message.setSenderType(senderType);
        message.setSenderId(senderId);
        message.setContent(content);
        message.setMessageType(messageType);
        messageService.sendMessage(message);
    }

    private void updateAiMessage(Long messageId, String fullContent) {
        // 这里可以更新消息内容（如果需要）
        // 目前已经在流式过程中实时推送，无需额外更新
    }

    // ==================== 管理接口 ====================

    @Override
    public boolean isAiServiceHealthy() {
        return aiClient.isHealthy();
    }

    @Override
    public void resetCircuitBreaker() {
        aiClient.resetCircuitBreaker();
    }
}
