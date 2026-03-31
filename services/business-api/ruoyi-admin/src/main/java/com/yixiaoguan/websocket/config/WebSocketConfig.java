package com.yixiaoguan.websocket.config;

import com.ruoyi.common.constant.CacheConstants;
import com.ruoyi.common.constant.Constants;
import com.ruoyi.common.core.domain.model.LoginUser;
import com.ruoyi.common.core.redis.RedisCache;
import com.yixiaoguan.websocket.handler.YxChatWebSocketHandler;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.http.server.ServletServerHttpRequest;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import org.springframework.web.socket.server.HandshakeInterceptor;

import java.util.Map;

/**
 * WebSocket 配置类
 * 注册端点：/ws/chat/{conversationId}
 *
 * 鉴权方式：
 *   HandshakeInterceptor 在握手阶段从 URL Query Param ?token=xxx 提取 JWT，
 *   解析出 uuid 后从 Redis (login_tokens:{uuid}) 读取 LoginUser，
 *   失败则拒绝握手（返回 false → 前端收到 HTTP 403）。
 *
 * 说明：
 *   Spring WebSocket 握手时处于 Servlet 容器上下文，但 WebSocket 帧本身脱离 Servlet 请求上下文，
 *   因此不能在 handler 中通过 SecurityContextHolder 获取当前用户。
 *   鉴权结果通过 Session Attributes 传递给 Handler。
 */
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private static final Logger log = LoggerFactory.getLogger(WebSocketConfig.class);

    @Autowired
    private YxChatWebSocketHandler chatWebSocketHandler;

    @Autowired
    private RedisCache redisCache;

    /** JWT 签名密钥（与 application.yml 中 token.secret 保持一致） */
    @Value("${token.secret}")
    private String jwtSecret;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry
            .addHandler(chatWebSocketHandler, "/ws/chat/**")
            // 允许跨域（生产环境建议改为明确的域名白名单）
            .setAllowedOriginPatterns("*")
            .addInterceptors(new WsAuthHandshakeInterceptor(redisCache, jwtSecret));
    }

    /**
     * WebSocket 握手鉴权拦截器（内部类）
     *
     * 流程：
     *   1. 从 Query Param 提取 ?token=xxx（前端连接时携带）
     *   2. 从路径 /ws/chat/{conversationId} 提取会话 ID
     *   3. 解析 JWT 得到 Redis key（uuid），从 Redis 读取 LoginUser
     *   4. 将 LoginUser 和 conversationId 存入 WebSocketSession Attributes
     */
    static class WsAuthHandshakeInterceptor implements HandshakeInterceptor {

        private static final Logger log = LoggerFactory.getLogger(WsAuthHandshakeInterceptor.class);

        private final RedisCache redisCache;
        private final String jwtSecret;

        WsAuthHandshakeInterceptor(RedisCache redisCache, String jwtSecret) {
            this.redisCache = redisCache;
            this.jwtSecret = jwtSecret;
        }

        @Override
        public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response,
                                       WebSocketHandler wsHandler, Map<String, Object> attributes) {
            if (!(request instanceof ServletServerHttpRequest)) {
                log.warn("[WsAuth] 非 Servlet 请求，拒绝握手");
                return false;
            }

            ServletServerHttpRequest servletRequest = (ServletServerHttpRequest) request;

            // 第一步：从 Query Param 提取 token
            String token = servletRequest.getServletRequest().getParameter("token");
            if (token == null || token.isBlank()) {
                log.warn("[WsAuth] 缺少 token 参数，拒绝握手 uri:{}", request.getURI());
                return false;
            }

            // 第二步：从路径中提取 conversationId（/ws/chat/123 → 123）
            String path = request.getURI().getPath();
            Long conversationId = extractConversationId(path);
            if (conversationId == null) {
                log.warn("[WsAuth] 无法从路径提取 conversationId，路径：{}", path);
                return false;
            }

            // 第三步：解析 JWT，提取 uuid，从 Redis 获取 LoginUser
            LoginUser loginUser;
            try {
                // 移除 Bearer 前缀（如果前端携带了前缀）
                if (token.startsWith(Constants.TOKEN_PREFIX)) {
                    token = token.replace(Constants.TOKEN_PREFIX, "");
                }
                Claims claims = Jwts.parser()
                        .setSigningKey(jwtSecret)
                        .parseClaimsJws(token)
                        .getBody();
                String uuid = (String) claims.get(Constants.LOGIN_USER_KEY);
                String userKey = CacheConstants.LOGIN_TOKEN_KEY + uuid;
                loginUser = redisCache.getCacheObject(userKey);
            } catch (Exception e) {
                log.warn("[WsAuth] Token 解析失败: {}", e.getMessage());
                return false;
            }

            if (loginUser == null || loginUser.getYxUser() == null) {
                log.warn("[WsAuth] Token 无效或用户不存在（Redis 已过期），拒绝握手");
                return false;
            }

            // 第四步：将鉴权结果注入 WebSocketSession Attributes
            attributes.put(YxChatWebSocketHandler.ATTR_LOGIN_USER, loginUser);
            attributes.put(YxChatWebSocketHandler.ATTR_CONVERSATION_ID, conversationId);

            log.info("[WsAuth] 握手鉴权通过 - 用户:{} ({}) 会话:{}",
                    loginUser.getYxUser().getId(), loginUser.getYxUser().getRealName(), conversationId);
            return true;
        }

        @Override
        public void afterHandshake(ServerHttpRequest request, ServerHttpResponse response,
                                   WebSocketHandler wsHandler, Exception exception) {
            // 握手后无需额外操作
        }

        /**
         * 从路径中解析 conversationId
         * 路径示例：/ws/chat/123 → 123
         */
        private Long extractConversationId(String path) {
            try {
                String[] segments = path.split("/");
                String last = segments[segments.length - 1];
                return Long.parseLong(last);
            } catch (NumberFormatException e) {
                return null;
            }
        }
    }
}
