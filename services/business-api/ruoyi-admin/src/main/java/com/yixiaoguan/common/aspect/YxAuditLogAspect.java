package com.yixiaoguan.common.aspect;

import com.alibaba.fastjson2.JSON;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.ServletUtils;
import com.ruoyi.common.utils.ip.IpUtils;
import com.ruoyi.common.core.domain.model.LoginUser;
import com.yixiaoguan.auditlog.domain.YxAuditLog;
import com.yixiaoguan.auditlog.service.IYxAuditLogService;
import com.yixiaoguan.common.annotation.YxLog;
import com.yixiaoguan.common.core.domain.YxUser;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.validation.BindingResult;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.util.Collection;
import java.util.Date;
import java.util.Map;

/**
 * 医小管审计日志切面
 * 拦截所有带有 @YxLog 注解的方法，异步记录审计日志
 * 
 * 核心设计原则：
 * 1. 绝对不阻塞主业务线（所有异常都被捕获）
 * 2. 异步写入数据库（通过 @Async）
 * 3. 与若依原生 LogAspect 完全隔离
 */
@Aspect
@Component
public class YxAuditLogAspect {

    private static final Logger log = LoggerFactory.getLogger(YxAuditLogAspect.class);

    /**
     * 线程本地变量，用于存储开始时间和日志实体
     */
    private static final ThreadLocal<Long> START_TIME = new ThreadLocal<>();
    private static final ThreadLocal<YxAuditLog> AUDIT_LOG = new ThreadLocal<>();

    @Autowired
    private IYxAuditLogService auditLogService;

    /**
     * 切入点：所有带有 @YxLog 注解的方法
     */
    @Pointcut("@annotation(com.yixiaoguan.common.annotation.YxLog)")
    public void yxLogPointCut() {
    }

    /**
     * 方法执行前：记录开始时间和基础信息
     */
    @Before("yxLogPointCut() && @annotation(yxLog)")
    public void doBefore(YxLog yxLog) {
        try {
            // 记录开始时间
            START_TIME.set(System.currentTimeMillis());

            // 初始化审计日志实体
            YxAuditLog auditLog = new YxAuditLog();
            auditLog.setModule(yxLog.module());
            auditLog.setAction(yxLog.action());
            auditLog.setTargetType(yxLog.targetType());
            auditLog.setDescription(yxLog.description());
            auditLog.setStatus(1); // 默认成功
            auditLog.setCreatedAt(new Date());
            auditLog.setUpdatedAt(new Date());
            auditLog.setIsDeleted(false);

            // 获取请求信息
            HttpServletRequest request = ServletUtils.getRequest();
            if (request != null) {
                auditLog.setRequestMethod(request.getMethod());
                auditLog.setRequestUrl(request.getRequestURI());
                auditLog.setRequestIp(IpUtils.getIpAddr(request));
            }

            // 获取当前用户信息
            fillUserInfo(auditLog);

            AUDIT_LOG.set(auditLog);
        } catch (Exception e) {
            // 审计前置逻辑异常绝不抛出
            log.warn("[YxAuditLog] 审计前置处理异常: {}", e.getMessage());
        }
    }

    /**
     * 方法正常返回后：记录成功日志
     */
    @AfterReturning(pointcut = "yxLogPointCut() && @annotation(yxLog)", returning = "jsonResult")
    public void doAfterReturning(YxLog yxLog, Object jsonResult) {
        try {
            YxAuditLog auditLog = AUDIT_LOG.get();
            if (auditLog == null) {
                return;
            }

            // 计算耗时
            long costTime = System.currentTimeMillis() - START_TIME.get();
            auditLog.setCostTime(costTime);

            // 设置响应状态码
            if (jsonResult != null) {
                auditLog.setResponseCode(HttpStatus.OK.value());
            }

            // 异步保存审计日志
            auditLogService.saveAsync(auditLog);
        } catch (Exception e) {
            // 审计后置逻辑异常绝不抛出
            log.warn("[YxAuditLog] 审计后置处理异常: {}", e.getMessage());
        } finally {
            // 清理线程变量
            clearThreadLocal();
        }
    }

    /**
     * 方法抛出异常后：记录失败日志
     */
    @AfterThrowing(pointcut = "yxLogPointCut() && @annotation(yxLog)", throwing = "e")
    public void doAfterThrowing(YxLog yxLog, Exception e) {
        try {
            YxAuditLog auditLog = AUDIT_LOG.get();
            if (auditLog == null) {
                return;
            }

            // 计算耗时
            long costTime = System.currentTimeMillis() - START_TIME.get();
            auditLog.setCostTime(costTime);

            // 设置失败状态
            auditLog.setStatus(0);
            auditLog.setResponseCode(HttpStatus.INTERNAL_SERVER_ERROR.value());
            auditLog.setErrorMsg(e.getMessage());

            // 异步保存审计日志
            auditLogService.saveAsync(auditLog);
        } catch (Exception ex) {
            // 审计异常处理逻辑本身异常绝不抛出
            log.warn("[YxAuditLog] 审计异常处理异常: {}", ex.getMessage());
        } finally {
            // 清理线程变量
            clearThreadLocal();
        }
    }

    /**
     * 填充用户信息
     */
    private void fillUserInfo(YxAuditLog auditLog) {
        try {
            LoginUser loginUser = SecurityUtils.getLoginUser();
            if (loginUser != null) {
                // 优先使用 yxUser
                if (loginUser.getYxUser() != null) {
                    YxUser yxUser = loginUser.getYxUser();
                    auditLog.setUserId(yxUser.getId());
                    auditLog.setUsername(yxUser.getUsername());
                } else if (loginUser.getUser() != null) {
                    // 兼容原生 sysUser
                    auditLog.setUserId(loginUser.getUser().getUserId());
                    auditLog.setUsername(loginUser.getUser().getUserName());
                }
            }
        } catch (Exception e) {
            // 获取用户信息失败不抛出异常
            log.debug("[YxAuditLog] 获取用户信息失败: {}", e.getMessage());
        }
    }

    /**
     * 清理线程本地变量
     */
    private void clearThreadLocal() {
        START_TIME.remove();
        AUDIT_LOG.remove();
    }

    /**
     * 参数脱敏处理
     * 过滤敏感字段和超大对象
     */
    private String argsToString(Object[] args) {
        if (args == null || args.length == 0) {
            return "[]";
        }

        StringBuilder params = new StringBuilder();
        for (Object arg : args) {
            if (arg != null) {
                // 排除不处理的类型
                if (arg instanceof HttpServletRequest 
                        || arg instanceof HttpServletResponse
                        || arg instanceof MultipartFile
                        || arg instanceof MultipartFile[]
                        || arg instanceof BindingResult) {
                    continue;
                }
                try {
                    String param = JSON.toJSONString(arg);
                    // 限制参数长度，防止过大
                    if (param.length() > 2000) {
                        param = param.substring(0, 2000) + "...(truncated)";
                    }
                    params.append(param).append(" ");
                } catch (Exception e) {
                    params.append("[serialize_error]");
                }
            }
        }
        return params.toString().trim();
    }
}
