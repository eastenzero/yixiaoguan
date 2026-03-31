package com.yixiaoguan.auditlog.service;

import com.yixiaoguan.auditlog.domain.YxAuditLog;
import com.ruoyi.common.core.page.TableDataInfo;

import java.util.List;

/**
 * 审计日志 Service 接口
 */
public interface IYxAuditLogService {

    /**
     * 分页查询审计日志列表
     *
     * @param userId   操作人 ID（null 则不过滤）
     * @param module   功能模块（null 则不过滤）
     * @param action   操作类型（null 则不过滤）
     * @return 分页数据
     */
    TableDataInfo selectPage(Long userId, String module, String action);

    /**
     * 通过 ID 查询审计日志详情
     *
     * @param id 日志 ID
     * @return 日志详情
     */
    YxAuditLog selectById(Long id);

    /**
     * 新增审计日志（同步）
     *
     * @param auditLog 日志对象
     * @return 影响行数
     */
    int insert(YxAuditLog auditLog);

    /**
     * 异步保存审计日志
     *
     * @param auditLog 日志对象
     */
    void saveAsync(YxAuditLog auditLog);

    /**
     * 批量新增审计日志
     *
     * @param list 日志列表
     * @return 影响行数
     */
    int batchInsert(List<YxAuditLog> list);
}
