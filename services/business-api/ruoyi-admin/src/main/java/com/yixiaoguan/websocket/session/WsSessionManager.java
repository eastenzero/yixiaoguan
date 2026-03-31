package com.yixiaoguan.websocket.session;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * WebSocket Session 管理器
 * 使用 ConcurrentHashMap 维护在线用户的连接状态，线程安全。
 *
 * 数据结构：
 *   userSessions:  userId → WebSocketSession（每个用户同时只允许一个连接）
 *   conversationUsers: conversationId → Set<userId>（记录哪些用户在同一会话中）
 */
@Component
public class WsSessionManager {

    private static final Logger log = LoggerFactory.getLogger(WsSessionManager.class);

    /** 用户 ID → WebSocket 会话 */
    private final Map<Long, WebSocketSession> userSessions = new ConcurrentHashMap<>();

    /** 会话 ID → 在线用户 ID 集合 */
    private final Map<Long, Set<Long>> conversationUsers = new ConcurrentHashMap<>();

    /**
     * 用户上线，注册 Session
     *
     * @param userId         用户 ID
     * @param conversationId 加入的会话 ID
     * @param session        WebSocket 连接 Session
     */
    public void addSession(Long userId, Long conversationId, WebSocketSession session) {
        // 若用户已有旧连接，先关闭旧连接（踢下线，防止重复连接）
        WebSocketSession old = userSessions.put(userId, session);
        if (old != null && old.isOpen()) {
            try {
                old.close();
                log.info("[WsSessionManager] 用户 {} 旧连接已关闭（重复连接）", userId);
            } catch (IOException e) {
                log.warn("[WsSessionManager] 关闭用户 {} 旧连接时发生异常: {}", userId, e.getMessage());
            }
        }
        // 注册到会话用户集合
        conversationUsers.computeIfAbsent(conversationId, k -> ConcurrentHashMap.newKeySet())
                         .add(userId);
        log.info("[WsSessionManager] 用户 {} 加入会话 {}", userId, conversationId);
    }

    /**
     * 用户下线，移除 Session
     *
     * @param userId         用户 ID
     * @param conversationId 离开的会话 ID
     */
    public void removeSession(Long userId, Long conversationId) {
        userSessions.remove(userId);
        Set<Long> users = conversationUsers.get(conversationId);
        if (users != null) {
            users.remove(userId);
            // 若会话内已无用户，清理 Map
            if (users.isEmpty()) {
                conversationUsers.remove(conversationId);
            }
        }
        log.info("[WsSessionManager] 用户 {} 离开会话 {}", userId, conversationId);
    }

    /**
     * 根据用户 ID 获取 WebSocket Session
     *
     * @param userId 用户 ID
     * @return WebSocketSession，若用户不在线则返回 null
     */
    public WebSocketSession getSession(Long userId) {
        return userSessions.get(userId);
    }

    /**
     * 获取某个会话中所有在线用户 ID
     *
     * @param conversationId 会话 ID
     * @return 用户 ID 集合（可能为空）
     */
    public Set<Long> getUsersInConversation(Long conversationId) {
        return conversationUsers.getOrDefault(conversationId, ConcurrentHashMap.newKeySet());
    }

    /**
     * 查询用户是否在线
     *
     * @param userId 用户 ID
     * @return true 表示在线
     */
    public boolean isOnline(Long userId) {
        WebSocketSession session = userSessions.get(userId);
        return session != null && session.isOpen();
    }

    /**
     * 获取当前在线总人数（用于监控）
     *
     * @return 在线人数
     */
    public int getOnlineCount() {
        return userSessions.size();
    }
}
