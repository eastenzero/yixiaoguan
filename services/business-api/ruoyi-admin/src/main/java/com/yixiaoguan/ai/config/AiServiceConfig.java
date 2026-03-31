package com.yixiaoguan.ai.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

/**
 * AI 服务配置类
 * 管理 Python AI 服务的连接参数
 */
@Configuration
public class AiServiceConfig {

    /**
     * AI 服务基础 URL（默认本机 8000 端口）
     */
    @Value("${yx.ai.service.url:http://127.0.0.1:8000}")
    private String baseUrl;

    /**
     * 连接超时（秒）
     */
    @Value("${yx.ai.connect-timeout:5}")
    private int connectTimeout;

    /**
     * 读取超时（秒）- 意图提取等非流式接口
     */
    @Value("${yx.ai.read-timeout:30}")
    private int readTimeout;

    /**
     * 流式读取超时（秒）- SSE 流式接口，时间较长
     */
    @Value("${yx.ai.stream-read-timeout:300}")
    private int streamReadTimeout;

    /**
     * 最大重试次数
     */
    @Value("${yx.ai.max-retries:3}")
    private int maxRetries;

    /**
     * 重试间隔（毫秒）
     */
    @Value("${yx.ai.retry-delay:1000}")
    private int retryDelayMs;

    /**
     * 是否启用熔断（简易熔断：连续失败N次后暂停调用）
     */
    @Value("${yx.ai.circuit-breaker-enabled:true}")
    private boolean circuitBreakerEnabled;

    /**
     * 熔断触发阈值（连续失败次数）
     */
    @Value("${yx.ai.circuit-breaker-threshold:5}")
    private int circuitBreakerThreshold;

    /**
     * 熔断恢复时间（秒）
     */
    @Value("${yx.ai.circuit-breaker-recovery-seconds:30}")
    private int circuitBreakerRecoverySeconds;

    // ===== Getter =====

    public String getBaseUrl() {
        return baseUrl;
    }

    public int getConnectTimeout() {
        return connectTimeout;
    }

    public int getReadTimeout() {
        return readTimeout;
    }

    public int getStreamReadTimeout() {
        return streamReadTimeout;
    }

    public int getMaxRetries() {
        return maxRetries;
    }

    public int getRetryDelayMs() {
        return retryDelayMs;
    }

    public boolean isCircuitBreakerEnabled() {
        return circuitBreakerEnabled;
    }

    public int getCircuitBreakerThreshold() {
        return circuitBreakerThreshold;
    }

    public int getCircuitBreakerRecoverySeconds() {
        return circuitBreakerRecoverySeconds;
    }
}
