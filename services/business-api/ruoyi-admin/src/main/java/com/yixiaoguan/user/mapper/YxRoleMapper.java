package com.yixiaoguan.user.mapper;

import java.util.List;
import com.yixiaoguan.common.core.domain.YxRole;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface YxRoleMapper {
    /**
     * 根据用户ID查询角色列表
     */
    List<YxRole> selectRolesByUserId(Long userId);
}
