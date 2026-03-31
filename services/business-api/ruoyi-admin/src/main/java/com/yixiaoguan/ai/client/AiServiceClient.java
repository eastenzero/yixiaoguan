package com.yixiaoguan.ai.client;

import com.alibaba.fastjson2.JSON;
import com.yixiaoguan.ai.config.AiServiceConfig;
import com.yixiaoguan.ai.dto.*;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Flow;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Consumer;

/**
 * AI 服务 HTTP 客户端
 * 封装对 Python AI 服务（端口 8000）的远程调用
 * 特性：JDK 21 HttpClient + 熔断 + 重试
 */
@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    @Autowired
    private AiServiceConfig config;

    private HttpClient httpClient;
    private HttpClient streamHttpClient;

    // ===== 熔断器状态 =====
    private final AtomicInteger consecutiveFailures = new AtomicInteger(0);
    private final AtomicLong circuitOpenTime = new AtomicLong(0);
    private volatile boolean circuitOpen = false;

    @PostConstruct
    public void init() {
        // 普通请求客户端
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(config.getConnectTimeout()))
                .build();

        // 流式请求客户端（更长的超时）
        this.streamHttpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(config.getConnectTimeout()))
                .build();

        log.info("[AiServiceClient] 初始化完成，目标地址: {}", config.getBaseUrl());
    }

    // ==================== 意图提取接口 ====================

    /**
     * 调用 /api/agent/extract 提取用户意图
     *
     * @param text 用户输入文本
     * @return 意图提取响应
     */
    public IntentExtractResponse extractIntent(String text) {
        checkCircuitBreaker();

        String url = config.getBaseUrl() + "/api/agent/extract";
        IntentExtractRequest request = new IntentExtractRequest(text);
        String jsonBody = JSON.toJSONString(request);

        return executeWithRetry(() -> {
            HttpRequest httpRequest = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Content-Type", "application/json")
                    .timeout(Duration.ofSeconds(config.getReadTimeout()))
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> response = httpClient.send(
                    httpRequest, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));

            if (response.statusCode() == 200) {
                IntentExtractResponse result = JSON.parseObject(response.body(), IntentExtractResponse.class);
                recordSuccess();
                return result;
            } else {
                throw new RuntimeException("AI服务返回非200状态码: " + response.statusCode());
            }
        }, "意图提取");
    }

    // ==================== 流式对话接口 ====================

    /**
     * 调用 /api/chat/stream 进行流式 RAG 问答
     *
     * @param request  流式对话请求
     * @param onChunk  每个片段的回调
     * @return CompletableFuture 用于异步处理完成
     */
    public CompletableFuture<Void> streamChat(ChatStreamRequest request, Consumer<ChatStreamChunk> onChunk) {
        checkCircuitBreaker();

        String url = config.getBaseUrl() + "/api/chat/stream";
        String jsonBody = JSON.toJSONString(request);

        HttpRequest httpRequest = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .header("Accept", "text/event-stream")
                .timeout(Duration.ofSeconds(config.getStreamReadTimeout()))
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody, StandardCharsets.UTF_8))
                .build();

        return streamHttpClient.sendAsync(httpRequest, HttpResponse.BodyHandlers.ofInputStream())
                .thenAccept(response -> {
                    if (response.statusCode() != 200) {
                        throw new RuntimeException("AI流式服务返回非200状态码: " + response.statusCode());
                    }

                    try (BufferedReader reader = new BufferedReader(
                            new InputStreamReader(response.body(), StandardCharsets.UTF_8))) {

                        String line;
                        while ((line = reader.readLine()) != null) {
                            // SSE 格式: data: {...}
                            if (line.startsWith("data: ")) {
                                String json = line.substring(6);
                                if (!json.isEmpty()) {
                                    ChatStreamChunk chunk = JSON.parseObject(json, ChatStreamChunk.class);
                                    onChunk.accept(chunk);

                                    if (chunk.isEnd()) {
                                        break;
                                    }
                                }
                            } else if (line.isEmpty()) {
                                // SSE 空行，忽略
                                continue;
                            }
                        }
                        recordSuccess();
                    } catch (Exception e) {
                        throw new RuntimeException("解析SSE流失败: " + e.getMessage(), e);
                    }
                })
                .exceptionally(throwable -> {
                    recordFailure();
                    log.error("[AiServiceClient] 流式对话失败: {}", throwable.getMessage());
                    onChunk.accept(ChatStreamChunk.error("AI服务调用失败: " + throwable.getMessage()));
                    return null;
                });
    }

    // ==================== 熔断器逻辑 ====================

    private void checkCircuitBreaker() {
        if (!config.isCircuitBreakerEnabled()) {
            return;
        }

        if (circuitOpen) {
            long openDuration = (System.currentTimeMillis() - circuitOpenTime.get()) / 1000;
            if (openDuration >= config.getCircuitBreakerRecoverySeconds()) {
                // 尝试恢复
                log.info("[AiServiceClient] 熔断器尝试恢复...");
                circuitOpen = false;
                consecutiveFailures.set(0);
            } else {
                throw new RuntimeException("AI服务熔断器已开启，请" +
                        (config.getCircuitBreakerRecoverySeconds() - openDuration) + "秒后重试");
            }
        }
    }

    private void recordSuccess() {
        if (!config.isCircuitBreakerEnabled()) {
            return;
        }
        consecutiveFailures.set(0);
    }

    private void recordFailure() {
        if (!config.isCircuitBreakerEnabled()) {
            return;
        }
        int failures = consecutiveFailures.incrementAndGet();
        if (failures >= config.getCircuitBreakerThreshold()) {
            circuitOpen = true;
            circuitOpenTime.set(System.currentTimeMillis());
            log.error("[AiServiceClient] 熔断器已开启！连续失败 {} 次", failures);
        }
    }

    // ==================== 重试逻辑 ====================

    @FunctionalInterface
    private interface RequestSupplier<T> {
        T execute() throws Exception;
    }

    private <T> T executeWithRetry(RequestSupplier<T> supplier, String operationName) {
        int maxRetries = config.getMaxRetries();
        int delayMs = config.getRetryDelayMs();

        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                T result = supplier.execute();
                if (attempt > 1) {
                    log.info("[AiServiceClient] {} 第{}次重试成功", operationName, attempt);
                }
                return result;
            } catch (Exception e) {
                recordFailure();
                if (attempt == maxRetries) {
                    log.error("[AiServiceClient] {} 失败，已重试{}次: {}",
                            operationName, maxRetries, e.getMessage());
                    throw new RuntimeException(operationName + "失败: " + e.getMessage(), e);
                }
                log.warn("[AiServiceClient] {} 第{}次尝试失败，{}ms后重试: {}",
                        operationName, attempt, delayMs, e.getMessage());
                try {
                    Thread.sleep(delayMs);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("重试被中断", ie);
                }
            }
        }
        throw new RuntimeException(operationName + "失败: 未知错误");
    }

    // ==================== 健康检查 ====================

    /**
     * 检查 AI 服务是否可用
     */
    public boolean isHealthy() {
        if (circuitOpen) {
            return false;
        }
        try {
            String url = config.getBaseUrl() + "/api/agent/health";
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .timeout(Duration.ofSeconds(3))
                    .GET()
                    .build();
            HttpResponse<String> response = httpClient.send(
                    request, HttpResponse.BodyHandlers.ofString());
            return response.statusCode() == 200;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * 手动重置熔断器（管理接口用）
     */
    public void resetCircuitBreaker() {
        circuitOpen = false;
        consecutiveFailures.set(0);
        log.info("[AiServiceClient] 熔断器已手动重置");
    }

    /**
     * 获取熔断器状态
     */
    public String getCircuitStatus() {
        return circuitOpen ? "OPEN" : "CLOSED";
    }
}
