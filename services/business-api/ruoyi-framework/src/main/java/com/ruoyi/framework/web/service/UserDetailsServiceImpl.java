package com.ruoyi.framework.web.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import com.yixiaoguan.common.core.domain.YxRole;
import com.yixiaoguan.common.core.domain.YxUser;
import com.ruoyi.common.core.domain.entity.SysRole;
import com.ruoyi.common.core.domain.entity.SysUser;
import java.util.stream.Collectors;
import java.util.List;
import com.ruoyi.common.core.domain.model.LoginUser;
import com.ruoyi.common.enums.UserStatus;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.common.utils.MessageUtils;
import com.ruoyi.common.utils.StringUtils;
import com.yixiaoguan.common.core.service.IYxUserService;

/**
 * 用户验证处理
 *
 * @author ruoyi
 */
@Service
public class UserDetailsServiceImpl implements UserDetailsService
{
    private static final Logger log = LoggerFactory.getLogger(UserDetailsServiceImpl.class);

    @Autowired
    private IYxUserService userService;
    
    @Autowired
    private SysPasswordService passwordService;

    @Autowired
    private SysPermissionService permissionService;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException
    {
        YxUser user = userService.selectUserByUsername(username);
        if (StringUtils.isNull(user))
        {
            log.info("登录用户：{} 不存在.", username);
            throw new ServiceException(MessageUtils.message("user.not.exists"));
        }
        else if (user.getIsDeleted() != null && user.getIsDeleted())
        {
            log.info("登录用户：{} 已被删除.", username);
            throw new ServiceException(MessageUtils.message("user.password.delete"));
        }
        else if (user.getStatus() == 0 || user.getStatus() == 2)
        {
            log.info("登录用户：{} 已被停用或未激活.", username);
            throw new ServiceException("对不起，您的账号：" + username + " 已停用或未激活");
        }

        SysUser sysUser = new SysUser();
        sysUser.setUserId(user.getId());
        sysUser.setUserName(user.getUsername());
        sysUser.setPassword(user.getPassword());
        sysUser.setDeptId(100L); // 假数据防止原生组件空指针

        if (user.getRoles() != null) {
            List<SysRole> sysRoles = user.getRoles().stream().map(r -> {
                SysRole sr = new SysRole();
                sr.setRoleId(r.getId());
                sr.setRoleKey(r.getRoleKey());
                sr.setRoleName(r.getRoleName());
                return sr;
            }).collect(Collectors.toList());
            sysUser.setRoles(sysRoles);
        }

        passwordService.validate(sysUser);

        return createLoginUser(user, sysUser);
    }

    public UserDetails createLoginUser(YxUser yxUser, SysUser sysUser)
    {
        LoginUser loginUser = new LoginUser(sysUser.getUserId(), sysUser.getDeptId(), sysUser, permissionService.getMenuPermission(sysUser));
        loginUser.setYxUser(yxUser);
        return loginUser;
    }
}
