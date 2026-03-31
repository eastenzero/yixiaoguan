package com.yixiaoguan.user.service.impl;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.common.utils.StringUtils;
import com.yixiaoguan.common.core.domain.YxRole;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.user.mapper.YxRoleMapper;
import com.yixiaoguan.common.core.service.IYxRoleService;

@Service
public class YxRoleServiceImpl implements IYxRoleService {

    @Autowired
    private YxRoleMapper roleMapper;

    @Override
    public Set<String> selectRolePermissionByUserId(Long userId) {
        List<YxRole> perms = roleMapper.selectRolesByUserId(userId);
        Set<String> permsSet = new HashSet<>();
        for (YxRole perm : perms) {
            if (StringUtils.isNotNull(perm)) {
                permsSet.addAll(Arrays.asList(perm.getRoleKey().trim().split(",")));
            }
        }
        return permsSet;
    }
}
