package com.yixiaoguan.auditlog.service.impl;

import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.utils.PageUtils;
import com.yixiaoguan.auditlog.domain.YxAuditLog;
import com.yixiaoguan.auditlog.mapper.YxAuditLogMapper;
import com.yixiaoguan.auditlog.service.IYxAuditLogService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 审计日志 Service 实现
 */
@Service
public class YxAuditLogServiceImpl implements IYxAuditLogService {

    private static final Logger log = LoggerFactory.getLogger(YxAuditLogServiceImpl.class);

    @Autowired
    private YxAuditLogMapper auditLogMapper;

    @Override
    public TableDataInfo selectPage(Long userId, String module, String action) {
        // 若依分页规范：显式调用 startPage
        PageUtils.startPage();
        int offset = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() <= 0 ? 0 
                : (com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() - 1) * com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();
        int limit = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();
        
        List<YxAuditLog> list = auditLogMapper.selectPage(userId, module, action, offset, limit);
        long total = auditLogMapper.count(userId, module, action);
        
        TableDataInfo result = new TableDataInfo();
        result.setCode(200);
        result.setMsg("查询成功");
        result.setRows(list);
        result.setTotal(total);
        return result;
    }

    @Override
    public YxAuditLog selectById(Long id) {
        return auditLogMapper.selectById(id);
    }

    @Override
    public int insert(YxAuditLog auditLog) {
        return auditLogMapper.insert(auditLog);
    }

    @Override
    @Async("yxAuditExecutor")
    public void saveAsync(YxAuditLog auditLog) {
        try {
            auditLogMapper.insert(auditLog);
        } catch (Exception e) {
            // 异步保存失败只记录日志，不抛出异常
            log.error("[YxAuditLog] 异步保存审计日志失败: {}", e.getMessage());
        }
    }

    @Override
    public int batchInsert(List<YxAuditLog> list) {
        return auditLogMapper.batchInsert(list);
    }
}
