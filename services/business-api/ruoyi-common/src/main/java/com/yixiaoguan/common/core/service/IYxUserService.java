package com.yixiaoguan.common.core.service;

import com.yixiaoguan.common.core.domain.YxUser;
import java.util.Date;

public interface IYxUserService {
    /**
     * 通过用户名查询用户
     * 
     * @param username 用户名
     * @return 用户对象信息
     */
    YxUser selectUserByUsername(String username);

    /**
     * 通过用户ID查询用户
     * 
     * @param id 用户ID
     * @return 用户对象信息
     */
    YxUser selectUserById(Long id);

    /**
     * 记录登录信息
     *
     * @param id 用户ID
     * @param lastLoginIp 登录IP
     * @param lastLoginAt 登录时间
     */
    void updateLoginInfo(Long id, String lastLoginIp, Date lastLoginAt);
}
