package com.yixiaoguan.common.core.service;

import java.util.Set;
import java.util.List;
import com.yixiaoguan.common.core.domain.YxMenu;

public interface IYxMenuService {
    /**
     * 根据用户ID查询权限
     * 
     * @param userId 用户ID
     * @return 权限列表
     */
    Set<String> selectMenuPermsByUserId(Long userId);

    /**
     * 根据用户ID查菜单树
     */
    List<YxMenu> selectMenuTreeByUserId(Long userId);
}
