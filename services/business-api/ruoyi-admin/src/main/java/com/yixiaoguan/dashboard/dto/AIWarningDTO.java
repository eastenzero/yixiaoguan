package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;

/**
 * AI 舆情预警 DTO
 */
public class AIWarningDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 话题 */
    private String topic;

    /** 增长百分比 */
    private int increasePercent;

    /** 建议 */
    private String suggestion;

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public int getIncreasePercent() {
        return increasePercent;
    }

    public void setIncreasePercent(int increasePercent) {
        this.increasePercent = increasePercent;
    }

    public String getSuggestion() {
        return suggestion;
    }

    public void setSuggestion(String suggestion) {
        this.suggestion = suggestion;
    }
}
