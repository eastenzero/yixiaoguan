package com.yixiaoguan.user.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.yixiaoguan.user.mapper.YxUserMapper;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.common.core.service.IYxUserService;
import java.util.Date;

@Service
public class YxUserServiceImpl implements IYxUserService {

    @Autowired
    private YxUserMapper yxUserMapper;

    @Override
    public YxUser selectUserByUsername(String username) {
        return yxUserMapper.selectUserByUsername(username);
    }

    @Override
    public YxUser selectUserById(Long id) {
        return yxUserMapper.selectUserById(id);
    }

    @Override
    public void updateLoginInfo(Long id, String lastLoginIp, Date lastLoginAt) {
        yxUserMapper.updateLoginInfo(id, lastLoginIp, lastLoginAt);
    }
}
