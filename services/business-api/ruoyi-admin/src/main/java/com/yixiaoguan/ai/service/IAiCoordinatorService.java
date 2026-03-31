package com.yixiaoguan.ai.service;

import org.springframework.web.socket.WebSocketSession;

/**
 * AI 协调服务接口
 * 核心网关逻辑：意图识别 + 分支调度
 */
public interface IAiCoordinatorService {

    /**
     * 处理学生发来的自然语言消息
     * 核心流程：
     * 1. 调用 /api/agent/extract 识别意图
     * 2. 如果是普通聊天 -> 调 /api/chat/stream 流式推字
     * 3. 如果是办事意图 -> 执行业务逻辑
     *
     * @param userId         用户ID
     * @param conversationId 会话ID
     * @param message        用户输入消息
     * @param session        WebSocket会话（用于流式推送）
     */
    void processStudentMessage(Long userId, Long conversationId, String message, WebSocketSession session);

    /**
     * 检查 AI 服务健康状态
     *
     * @return 是否健康
     */
    boolean isAiServiceHealthy();

    /**
     * 重置熔断器（管理用途）
     */
    void resetCircuitBreaker();
}
