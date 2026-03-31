package com.yixiaoguan.ai.enums;

/**
 * 意图类型枚举
 * 对应 Python AI 服务识别的用户意图分类
 */
public enum IntentType {

    /**
     * 普通聊天意图 - 走 RAG 问答流程
     */
    CHAT("chat", "普通聊天", false),

    /**
     * 预约/借用教室 - 走业务流程
     */
    BOOK_CLASSROOM("book_classroom", "预约教室", true),

    /**
     * 提交设备报修 - 走业务流程（预留）
     */
    SUBMIT_REPAIR_REQUEST("submit_repair_request", "设备报修", true),

    /**
     * 查询办事进度 - 走业务流程（预留）
     */
    QUERY_APPLICATION_STATUS("query_application_status", "查询进度", true),

    /**
     * 未知/无法识别意图 - 降级为普通聊天
     */
    UNKNOWN("unknown", "未知意图", false);

    /** 意图编码（与Python端约定） */
    private final String code;

    /** 意图描述 */
    private final String description;

    /** 是否为办事意图（非普通聊天） */
    private final boolean serviceIntent;

    IntentType(String code, String description, boolean serviceIntent) {
        this.code = code;
        this.description = description;
        this.serviceIntent = serviceIntent;
    }

    public String getCode() {
        return code;
    }

    public String getDescription() {
        return description;
    }

    public boolean isServiceIntent() {
        return serviceIntent;
    }

    /**
     * 根据编码获取枚举
     */
    public static IntentType fromCode(String code) {
        if (code == null || code.isBlank()) {
            return UNKNOWN;
        }
        for (IntentType type : values()) {
            if (type.code.equalsIgnoreCase(code)) {
                return type;
            }
        }
        return UNKNOWN;
    }
}
