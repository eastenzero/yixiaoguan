package com.yixiaoguan.ai.dto;

/**
 * 意图提取请求 DTO
 * 发往 Python AI 服务 /api/agent/extract
 */
public class IntentExtractRequest {

    /**
     * 用户输入的自然语言文本（必填）
     */
    private String text;

    /**
     * 上下文信息（可选，用于多轮对话）
     */
    private String context;

    public IntentExtractRequest() {
    }

    public IntentExtractRequest(String text) {
        this.text = text;
    }

    public IntentExtractRequest(String text, String context) {
        this.text = text;
        this.context = context;
    }

    // ===== Getter / Setter =====

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getContext() {
        return context;
    }

    public void setContext(String context) {
        this.context = context;
    }
}
