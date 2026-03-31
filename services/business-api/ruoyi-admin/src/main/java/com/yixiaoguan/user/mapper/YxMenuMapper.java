package com.yixiaoguan.user.mapper;

import java.util.List;
import com.yixiaoguan.common.core.domain.YxMenu;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface YxMenuMapper {
    /**
     * 根据用户ID查询权限标识
     */
    List<String> selectMenuPermsByUserId(Long userId);

    /**
     * 获取所有菜单树（管理员可见）
     */
    List<YxMenu> selectMenuTreeAll();

    /**
     * 根据用户ID查询菜单树
     */
    List<YxMenu> selectMenuTreeByUserId(Long userId);
}
