package com.yixiaoguan.auth.controller;

import java.util.Set;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.constant.Constants;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.domain.model.LoginBody;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.framework.web.service.SysPermissionService;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.framework.web.service.SysLoginService;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.common.core.domain.YxMenu;
import com.yixiaoguan.common.core.service.IYxMenuService;

@RestController
public class AuthController
{
    @Autowired
    private SysLoginService loginService;

    @Autowired
    private SysPermissionService permissionService;

    @Autowired
    private IYxMenuService menuService;

    /**
     * 登录方法
     * 
     * @param loginBody 登录信息
     * @return 结果
     */
    @PostMapping("/login")
    public AjaxResult login(@RequestBody LoginBody loginBody)
    {
        AjaxResult ajax = AjaxResult.success();
        // 生成令牌
        String token = loginService.login(loginBody.getUsername(), loginBody.getPassword(), loginBody.getCode(),
                loginBody.getUuid());
        ajax.put(Constants.TOKEN, token);
        return ajax;
    }

    /**
     * 获取用户信息
     * 
     * @return 用户信息
     */
    @GetMapping("/getInfo")
    public AjaxResult getInfo()
    {
        SysUser sysUser = SecurityUtils.getLoginUser().getUser();
        YxUser user = SecurityUtils.getLoginUser().getYxUser();
        // 角色集合
        Set<String> roles = permissionService.getRolePermission(sysUser);
        // 权限集合
        Set<String> permissions = permissionService.getMenuPermission(sysUser);
        AjaxResult ajax = AjaxResult.success();
        // 为了方便前端拿到 isAdmin 标志，这里手动设置一下
        user.setAdmin(YxUser.isAdmin(user.getId()));
        ajax.put("user", user);
        ajax.put("roles", roles);
        ajax.put("permissions", permissions);
        return ajax;
    }

    /**
     * 获取路由信息
     * 
     * @return 路由信息
     */
    @GetMapping("/getRouters")
    public AjaxResult getRouters()
    {
        Long userId = SecurityUtils.getUserId();
        List<YxMenu> menus = menuService.selectMenuTreeByUserId(userId);
        
        // 由于前端依赖特定的 RouterVo 格式，如果前端没有高度自定义，原本应调用若依的 buildMenus。
        // 为了简单适配，阶段 1 往往只要把带 children 属性的 tree 丢给前端或让前端简单调整。
        // 这里直接返回树形结构。
        return AjaxResult.success(menus);
    }
}
