package com.yixiaoguan.ai.dto;

/**
 * 知识库引用来源传输对象
 * 用于展示 RAG 检索到的相关知识片段
 */
public class SourceItemDTO {

    /**
     * 知识条目 ID
     */
    private String entryId;

    /**
     * 知识标题
     */
    private String title;

    /**
     * 知识内容摘要
     */
    private String content;

    /**
     * 相似度分数 0-1
     */
    private Float score;

    public SourceItemDTO() {
    }

    public SourceItemDTO(String entryId, String title, String content, Float score) {
        this.entryId = entryId;
        this.title = title;
        this.content = content;
        this.score = score;
    }

    // ===== Getter / Setter =====

    public String getEntryId() {
        return entryId;
    }

    public void setEntryId(String entryId) {
        this.entryId = entryId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Float getScore() {
        return score;
    }

    public void setScore(Float score) {
        this.score = score;
    }
}
