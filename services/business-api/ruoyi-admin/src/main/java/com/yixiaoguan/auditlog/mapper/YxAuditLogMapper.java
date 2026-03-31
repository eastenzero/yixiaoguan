package com.yixiaoguan.auditlog.mapper;

import com.yixiaoguan.auditlog.domain.YxAuditLog;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 审计日志 Mapper 接口 - 对应 yx_audit_log 表
 * 审计日志不允许修改、删除
 */
@Mapper
public interface YxAuditLogMapper {

    /**
     * 分页查询审计日志列表
     *
     * @param userId   操作人 ID（null 则不过滤）
     * @param module   功能模块（null 则不过滤）
     * @param action   操作类型（null 则不过滤）
     * @param offset   分页偏移量
     * @param limit    每页条数
     * @return 日志列表
     */
    List<YxAuditLog> selectPage(
            @Param("userId") Long userId,
            @Param("module") String module,
            @Param("action") String action,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计审计日志总数
     *
     * @param userId 操作人 ID（null 则不过滤）
     * @param module 功能模块（null 则不过滤）
     * @param action 操作类型（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("userId") Long userId,
            @Param("module") String module,
            @Param("action") String action
    );

    /**
     * 通过主键查询审计日志详情
     *
     * @param id 日志 ID
     * @return 日志详情
     */
    YxAuditLog selectById(@Param("id") Long id);

    /**
     * 新增审计日志
     *
     * @param auditLog 日志对象
     * @return 影响行数
     */
    int insert(YxAuditLog auditLog);

    /**
     * 批量新增审计日志
     *
     * @param list 日志列表
     * @return 影响行数
     */
    int batchInsert(@Param("list") List<YxAuditLog> list);
}
