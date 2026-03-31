package com.yixiaoguan.user.mapper;

import com.yixiaoguan.common.core.domain.YxUser;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Mapper;
import java.util.Date;

@Mapper
public interface YxUserMapper {
    /**
     * 通过用户名查询用户
     */
    YxUser selectUserByUsername(String username);

    /**
     * 通过用户ID查询用户
     */
    YxUser selectUserById(Long id);

    /**
     * 更新登录信息
     */
    int updateLoginInfo(@Param("id") Long id, @Param("lastLoginIp") String lastLoginIp, @Param("lastLoginAt") Date lastLoginAt);
}
