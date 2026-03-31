package com.yixiaoguan.ai.dto;

/**
 * 对话消息传输对象（与 Python 端约定格式）
 * 用于传递历史对话记录
 */
public class ChatMessageDTO {

    /**
     * 角色: system / user / assistant
     */
    private String role;

    /**
     * 消息内容
     */
    private String content;

    public ChatMessageDTO() {
    }

    public ChatMessageDTO(String role, String content) {
        this.role = role;
        this.content = content;
    }

    // ===== 快捷构造方法 =====

    public static ChatMessageDTO user(String content) {
        return new ChatMessageDTO("user", content);
    }

    public static ChatMessageDTO assistant(String content) {
        return new ChatMessageDTO("assistant", content);
    }

    public static ChatMessageDTO system(String content) {
        return new ChatMessageDTO("system", content);
    }

    // ===== Getter / Setter =====

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}
