package com.yixiaoguan.websocket.handler;

import com.alibaba.fastjson2.JSON;
import com.ruoyi.common.core.domain.model.LoginUser;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.conversation.domain.YxConversation;
import com.yixiaoguan.conversation.domain.YxMessage;
import com.yixiaoguan.conversation.service.IYxConversationService;
import com.yixiaoguan.conversation.service.IYxMessageService;
import com.yixiaoguan.websocket.domain.WsMessagePacket;
import com.yixiaoguan.websocket.session.WsSessionManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.Set;

/**
 * 医小管核心 WebSocket 消息处理器
 * 端点路径：/ws/chat/{conversationId}
 *
 * 鉴权方式：握手阶段由 WsAuthHandshakeInterceptor 从 URL ?token= 提取 JWT，
 *           验证通过后将 LoginUser 存入 WebSocketSession Attributes。
 *
 * 支持的指令类型（WsMessagePacket.type）：
 *   TEACHER_JOIN   - 教师加入会话，更新 DB 状态，通知学生
 *   TEACHER_LEAVE  - 教师离开，恢复 AI 接管，通知学生
 *   CHAT_MESSAGE   - 聊天消息，存库，转发至对端
 *   PING           - 心跳保活，应答 PONG
 */
@Component
public class YxChatWebSocketHandler extends TextWebSocketHandler {

    private static final Logger log = LoggerFactory.getLogger(YxChatWebSocketHandler.class);

    /** Session Attributes 中存储鉴权用户信息的 Key（由 HandshakeInterceptor 写入） */
    public static final String ATTR_LOGIN_USER = "loginUser";
    /** Session Attributes 中存储会话 ID 的 Key */
    public static final String ATTR_CONVERSATION_ID = "conversationId";

    @Autowired
    private WsSessionManager sessionManager;

    @Autowired
    private IYxConversationService conversationService;

    @Autowired
    private IYxMessageService messageService;

    // ========================= 连接生命周期 =========================

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        LoginUser loginUser = getLoginUser(session);
        Long conversationId = getConversationId(session);
        if (loginUser == null || conversationId == null) {
            closeSession(session, CloseStatus.POLICY_VIOLATION);
            return;
        }
        YxUser yxUser = loginUser.getYxUser();
        sessionManager.addSession(yxUser.getId(), conversationId, session);
        log.info("[WS] 连接建立 - 用户:{} 会话:{} sessionId:{}", yxUser.getId(), conversationId, session.getId());

        // 向当前用户推送连接成功通知
        sendPacket(session, buildSystemNotify(conversationId,
                "连接成功，会话已就绪", "CONNECTED"));
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        LoginUser loginUser = getLoginUser(session);
        Long conversationId = getConversationId(session);
        if (loginUser != null && conversationId != null) {
            YxUser yxUser = loginUser.getYxUser();
            sessionManager.removeSession(yxUser.getId(), conversationId);
            log.info("[WS] 连接关闭 - 用户:{} 会话:{} status:{}", yxUser.getId(), conversationId, status);
        }
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) {
        log.error("[WS] 传输异常 sessionId:{} error:{}", session.getId(), exception.getMessage());
        closeSession(session, CloseStatus.SERVER_ERROR);
    }

    // ========================= 消息处理路由 =========================

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        String payload = message.getPayload();
        log.debug("[WS] 收到消息: {}", payload);

        WsMessagePacket packet;
        try {
            packet = JSON.parseObject(payload, WsMessagePacket.class);
        } catch (Exception e) {
            log.warn("[WS] 消息解析失败: {}", payload);
            sendPacket(session, buildSystemNotify(null, "消息格式错误，请发送 JSON", "ERROR"));
            return;
        }

        if (packet.getType() == null) {
            sendPacket(session, buildSystemNotify(null, "缺少 type 字段", "ERROR"));
            return;
        }

        switch (packet.getType()) {
            case "TEACHER_JOIN":
                handleTeacherJoin(session, packet);
                break;
            case "TEACHER_LEAVE":
                handleTeacherLeave(session, packet);
                break;
            case "CHAT_MESSAGE":
                handleChatMessage(session, packet);
                break;
            case "PING":
                sendPacket(session, buildPong());
                break;
            default:
                sendPacket(session, buildSystemNotify(packet.getConversationId(),
                        "未知指令类型: " + packet.getType(), "ERROR"));
        }
    }

    // ========================= 各指令处理方法 =========================

    /**
     * 处理教师加入会话指令
     * 1. 校验发起者角色必须为 teacher
     * 2. 调用 Service 更新 DB 会话状态 → 2
     * 3. 向会话内所有学生推送系统通知
     */
    private void handleTeacherJoin(WebSocketSession session, WsMessagePacket packet) {
        LoginUser loginUser = getLoginUser(session);
        YxUser yxUser = loginUser.getYxUser();
        Long conversationId = packet.getConversationId();

        // 校验角色：必须是 teacher 或 admin
        if (!hasRole(loginUser, "teacher") && !hasRole(loginUser, "admin")) {
            sendPacket(session, buildSystemNotify(conversationId, "无权限：仅教师可加入会话", "FORBIDDEN"));
            return;
        }

        try {
            conversationService.teacherJoin(conversationId, yxUser.getId());
            // 注册当前教师到会话
            sessionManager.addSession(yxUser.getId(), conversationId, session);

            // 通知会话内的学生
            String notifyContent = "教师「" + yxUser.getRealName() + "」已加入，正在为您解答";
            broadcastToConversation(conversationId, yxUser.getId(),
                    buildSystemNotify(conversationId, notifyContent, "TEACHER_JOINED"));

            // 给教师自己返回确认
            sendPacket(session, buildSystemNotify(conversationId, "您已成功加入会话", "TEACHER_JOIN_OK"));
            log.info("[WS] 教师 {} 加入会话 {}", yxUser.getId(), conversationId);
        } catch (Exception e) {
            log.error("[WS] 教师加入会话失败: {}", e.getMessage());
            sendPacket(session, buildSystemNotify(conversationId, "加入失败: " + e.getMessage(), "ERROR"));
        }
    }

    /**
     * 处理教师离开会话指令
     * 1. 更新 DB 会话状态 → 1（进行中）
     * 2. 通知学生 AI 已恢复接管
     */
    private void handleTeacherLeave(WebSocketSession session, WsMessagePacket packet) {
        LoginUser loginUser = getLoginUser(session);
        YxUser yxUser = loginUser.getYxUser();
        Long conversationId = packet.getConversationId();

        try {
            conversationService.teacherLeave(conversationId, yxUser.getId());

            // 通知学生
            broadcastToConversation(conversationId, yxUser.getId(),
                    buildSystemNotify(conversationId, "教师已离开，AI 助手继续为您服务", "TEACHER_LEFT"));

            sendPacket(session, buildSystemNotify(conversationId, "您已离开会话", "TEACHER_LEAVE_OK"));
            log.info("[WS] 教师 {} 离开会话 {}", yxUser.getId(), conversationId);
        } catch (Exception e) {
            log.error("[WS] 教师离开会话失败: {}", e.getMessage());
            sendPacket(session, buildSystemNotify(conversationId, "操作失败: " + e.getMessage(), "ERROR"));
        }
    }

    /**
     * 处理聊天消息指令
     * 1. 确定 senderType（根据会话状态和用户角色）
     * 2. 存库（调用 MessageService）
     * 3. 将消息转发给会话内的对端（学生 → 教师 | 教师 → 学生）
     */
    private void handleChatMessage(WebSocketSession session, WsMessagePacket packet) {
        LoginUser loginUser = getLoginUser(session);
        YxUser yxUser = loginUser.getYxUser();
        Long conversationId = packet.getConversationId();

        if (conversationId == null || packet.getContent() == null || packet.getContent().isBlank()) {
            sendPacket(session, buildSystemNotify(conversationId, "消息内容不能为空", "ERROR"));
            return;
        }

        try {
            // 判断 senderType
            int senderType = determineSenderType(loginUser);

            // 构建消息并存库
            YxMessage message = new YxMessage();
            message.setConversationId(conversationId);
            message.setSenderType(senderType);
            message.setSenderId(yxUser.getId());
            message.setContent(packet.getContent());
            message.setMessageType(packet.getMessageType() != null ? packet.getMessageType() : 1);
            message.setParentMessageId(packet.getParentMessageId());
            YxMessage saved = messageService.sendMessage(message);

            // 组装下行数据包
            WsMessagePacket outPacket = new WsMessagePacket();
            outPacket.setType("CHAT_MESSAGE");
            outPacket.setConversationId(conversationId);
            outPacket.setMessageId(saved.getId());
            outPacket.setContent(saved.getContent());
            outPacket.setMessageType(saved.getMessageType());
            outPacket.setSenderId(yxUser.getId());
            outPacket.setSenderName(yxUser.getRealName());
            outPacket.setSenderType(senderType);
            outPacket.setParentMessageId(saved.getParentMessageId());

            // 转发给会话内其他用户
            broadcastToConversation(conversationId, yxUser.getId(), outPacket);
            // 给发送方回传消息（含 messageId，前端可做已发成功确认）
            sendPacket(session, outPacket);

        } catch (Exception e) {
            log.error("[WS] 发送消息失败: {}", e.getMessage());
            sendPacket(session, buildSystemNotify(conversationId, "发送失败: " + e.getMessage(), "ERROR"));
        }
    }

    // ========================= 工具方法 =========================

    /** 向会话内除 excludeUserId 之外的所有在线用户广播消息 */
    private void broadcastToConversation(Long conversationId, Long excludeUserId, WsMessagePacket packet) {
        Set<Long> users = sessionManager.getUsersInConversation(conversationId);
        for (Long uid : users) {
            if (uid.equals(excludeUserId)) continue;
            WebSocketSession targetSession = sessionManager.getSession(uid);
            if (targetSession != null && targetSession.isOpen()) {
                sendPacket(targetSession, packet);
            }
        }
    }

    /** 发送 JSON 数据包到指定 Session */
    private void sendPacket(WebSocketSession session, WsMessagePacket packet) {
        if (session == null || !session.isOpen()) return;
        try {
            synchronized (session) {
                session.sendMessage(new TextMessage(JSON.toJSONString(packet)));
            }
        } catch (IOException e) {
            log.error("[WS] 发送消息异常 sessionId:{} error:{}", session.getId(), e.getMessage());
        }
    }

    /** 构建系统通知指令帧 */
    private WsMessagePacket buildSystemNotify(Long conversationId, String content, String extra) {
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType("SYSTEM_NOTIFY");
        packet.setConversationId(conversationId);
        packet.setContent(content);
        packet.setSenderType(4); // 4-系统
        packet.setExtra(extra);
        return packet;
    }

    /** 构建心跳应答帧 */
    private WsMessagePacket buildPong() {
        WsMessagePacket packet = new WsMessagePacket();
        packet.setType("PONG");
        return packet;
    }

    /** 从 Session Attributes 获取登录用户信息 */
    private LoginUser getLoginUser(WebSocketSession session) {
        return (LoginUser) session.getAttributes().get(ATTR_LOGIN_USER);
    }

    /** 从 Session Attributes 获取会话 ID */
    private Long getConversationId(WebSocketSession session) {
        Object val = session.getAttributes().get(ATTR_CONVERSATION_ID);
        return val != null ? Long.parseLong(val.toString()) : null;
    }

    /** 判断用户是否拥有指定角色 */
    private boolean hasRole(LoginUser loginUser, String roleKey) {
        if (loginUser.getYxUser() == null || loginUser.getYxUser().getRoles() == null) {
            return false;
        }
        return loginUser.getYxUser().getRoles().stream()
                .anyMatch(r -> roleKey.equals(r.getRoleKey()));
    }

    /** 根据登录用户角色判断 senderType */
    private int determineSenderType(LoginUser loginUser) {
        if (hasRole(loginUser, "teacher") || hasRole(loginUser, "admin")) {
            return 3; // 3-教师
        }
        return 1; // 1-学生
    }

    /** 安全关闭 Session */
    private void closeSession(WebSocketSession session, CloseStatus status) {
        try {
            if (session.isOpen()) {
                session.close(status);
            }
        } catch (IOException e) {
            log.warn("[WS] 关闭 Session 异常: {}", e.getMessage());
        }
    }
}
