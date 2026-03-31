package com.yixiaoguan.ai.dto;

import java.util.Collections;
import java.util.List;

/**
 * 流式对话请求 DTO
 * 发往 Python AI 服务 /api/chat/stream
 */
public class ChatStreamRequest {

    /**
     * 用户问题（必填）
     */
    private String query;

    /**
     * 历史对话记录
     */
    private List<ChatMessageDTO> history;

    /**
     * 是否使用知识库增强（默认 true）
     */
    private Boolean useKb = true;

    public ChatStreamRequest() {
    }

    public ChatStreamRequest(String query) {
        this.query = query;
        this.history = Collections.emptyList();
    }

    public ChatStreamRequest(String query, List<ChatMessageDTO> history) {
        this.query = query;
        this.history = history;
    }

    // ===== Getter / Setter =====

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public List<ChatMessageDTO> getHistory() {
        return history == null ? Collections.emptyList() : history;
    }

    public void setHistory(List<ChatMessageDTO> history) {
        this.history = history;
    }

    public Boolean getUseKb() {
        return useKb;
    }

    public void setUseKb(Boolean useKb) {
        this.useKb = useKb;
    }
}
