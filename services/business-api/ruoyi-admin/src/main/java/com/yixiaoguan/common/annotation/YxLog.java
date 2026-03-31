package com.yixiaoguan.common.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 医小管自定义审计日志注解
 * 用于标记需要记录审计日志的方法
 * 
 * 使用示例：
 * @YxLog(module = "knowledge", action = "create", targetType = "entry", description = "创建知识条目")
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface YxLog {

    /**
     * 功能模块
     * 如：user / knowledge / application / notification / pushTask / aiPersona 等
     */
    String module();

    /**
     * 操作类型
     * 如：create / update / delete / query / export / login / logout 等
     */
    String action();

    /**
     * 操作对象类型（可选）
     * 如：entry / category / application / classroom 等
     */
    String targetType() default "";

    /**
     * 操作描述（可选）
     * 用于记录更详细的操作说明
     */
    String description() default "";
}
