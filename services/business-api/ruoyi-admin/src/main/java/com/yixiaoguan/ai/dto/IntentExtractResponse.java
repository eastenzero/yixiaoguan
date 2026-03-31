package com.yixiaoguan.ai.dto;

import com.yixiaoguan.ai.enums.IntentType;

import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * 意图提取响应 DTO
 * 接收 Python AI 服务 /api/agent/extract 的返回结果
 */
public class IntentExtractResponse {

    /**
     * 状态码，0 表示成功
     */
    private Integer code;

    /**
     * 消息说明
     */
    private String msg;

    /**
     * 响应数据体
     */
    private Data data;

    /**
     * 内部数据类
     */
    public static class Data {
        /**
         * 识别出的意图类型（如 book_classroom）
         */
        private String intent;

        /**
         * 置信度 0-1
         */
        private Float confidence;

        /**
         * 是否办事意图（非普通聊天）
         */
        private Boolean isServiceIntent;

        /**
         * 提取的参数键值对
         */
        private Map<String, Object> parameters;

        /**
         * 缺失的必填参数列表
         */
        private List<String> missingRequired;

        /**
         * 给用户的追问/确认语句
         */
        private String replyToUser;

        // ===== Getter / Setter =====

        public String getIntent() {
            return intent;
        }

        public void setIntent(String intent) {
            this.intent = intent;
        }

        public Float getConfidence() {
            return confidence;
        }

        public void setConfidence(Float confidence) {
            this.confidence = confidence;
        }

        public Boolean getIsServiceIntent() {
            return isServiceIntent;
        }

        public void setIsServiceIntent(Boolean serviceIntent) {
            isServiceIntent = serviceIntent;
        }

        public Map<String, Object> getParameters() {
            return parameters;
        }

        public void setParameters(Map<String, Object> parameters) {
            this.parameters = parameters;
        }

        public List<String> getMissingRequired() {
            return missingRequired == null ? Collections.emptyList() : missingRequired;
        }

        public void setMissingRequired(List<String> missingRequired) {
            this.missingRequired = missingRequired;
        }

        public String getReplyToUser() {
            return replyToUser;
        }

        public void setReplyToUser(String replyToUser) {
            this.replyToUser = replyToUser;
        }
    }

    // ===== 业务辅助方法 =====

    /**
     * 判断是否成功
     */
    public boolean isSuccess() {
        return code != null && code == 0 && data != null;
    }

    /**
     * 获取意图枚举
     */
    public IntentType getIntentType() {
        if (data == null || data.intent == null) {
            return IntentType.UNKNOWN;
        }
        return IntentType.fromCode(data.intent);
    }

    /**
     * 判断是否为办事意图
     */
    public boolean isServiceIntent() {
        return data != null && data.isServiceIntent != null && data.isServiceIntent;
    }

    /**
     * 获取提取的参数
     */
    public Map<String, Object> getParameters() {
        return data == null || data.parameters == null 
            ? Collections.emptyMap() 
            : data.parameters;
    }

    /**
     * 获取缺失的必填参数
     */
    public List<String> getMissingRequired() {
        return data == null 
            ? Collections.emptyList() 
            : data.getMissingRequired();
    }

    /**
     * 是否有缺失的必填参数
     */
    public boolean hasMissingRequired() {
        return !getMissingRequired().isEmpty();
    }

    /**
     * 获取给用户的追问语句
     */
    public String getReplyToUser() {
        return data == null ? null : data.replyToUser;
    }

    // ===== Getter / Setter =====

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }
}
