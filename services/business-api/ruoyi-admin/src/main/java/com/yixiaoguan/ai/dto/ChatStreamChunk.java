package com.yixiaoguan.ai.dto;

import java.util.Collections;
import java.util.List;

/**
 * 流式对话 SSE 片段 DTO
 * 接收 Python AI 服务 /api/chat/stream 的流式返回
 */
public class ChatStreamChunk {

    /**
     * 文本片段
     */
    private String chunk;

    /**
     * 是否结束标记
     */
    private Boolean isEnd;

    /**
     * 引用的知识来源（首次返回时携带）
     */
    private List<SourceItemDTO> sources;

    /**
     * 错误信息（异常时携带）
     */
    private String error;

    public ChatStreamChunk() {
    }

    // ===== 快捷构造方法 =====

    public static ChatStreamChunk text(String chunk) {
        ChatStreamChunk c = new ChatStreamChunk();
        c.chunk = chunk;
        c.isEnd = false;
        return c;
    }

    public static ChatStreamChunk end() {
        ChatStreamChunk c = new ChatStreamChunk();
        c.chunk = "";
        c.isEnd = true;
        return c;
    }

    public static ChatStreamChunk error(String errorMsg) {
        ChatStreamChunk c = new ChatStreamChunk();
        c.chunk = "";
        c.isEnd = true;
        c.error = errorMsg;
        return c;
    }

    // ===== Getter / Setter =====

    public String getChunk() {
        return chunk;
    }

    public void setChunk(String chunk) {
        this.chunk = chunk;
    }

    public Boolean getIsEnd() {
        return isEnd;
    }

    public void setIsEnd(Boolean end) {
        isEnd = end;
    }

    public List<SourceItemDTO> getSources() {
        return sources == null ? Collections.emptyList() : sources;
    }

    public void setSources(List<SourceItemDTO> sources) {
        this.sources = sources;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    // ===== 状态判断 =====

    public boolean isEnd() {
        return isEnd != null && isEnd;
    }

    public boolean hasError() {
        return error != null && !error.isEmpty();
    }
}
