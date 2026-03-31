package com.yixiaoguan.common.core.service;

import java.util.Set;
import com.yixiaoguan.common.core.domain.YxRole;

public interface IYxRoleService {
    /**
     * 根据用户ID查询角色权限
     * 
     * @param userId 用户ID
     * @return 权限列表
     */
    Set<String> selectRolePermissionByUserId(Long userId);
}
