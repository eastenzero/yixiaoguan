package com.yixiaoguan.user.service.impl;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.common.utils.StringUtils;
import com.yixiaoguan.common.core.domain.YxMenu;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.user.mapper.YxMenuMapper;
import com.yixiaoguan.common.core.service.IYxMenuService;

@Service
public class YxMenuServiceImpl implements IYxMenuService {

    @Autowired
    private YxMenuMapper menuMapper;

    @Override
    public Set<String> selectMenuPermsByUserId(Long userId) {
        List<String> perms = menuMapper.selectMenuPermsByUserId(userId);
        Set<String> permsSet = new HashSet<>();
        for (String perm : perms) {
            if (StringUtils.isNotEmpty(perm)) {
                permsSet.addAll(Arrays.asList(perm.trim().split(",")));
            }
        }
        return permsSet;
    }

    @Override
    public List<YxMenu> selectMenuTreeByUserId(Long userId) {
        List<YxMenu> menus = null;
        if (YxUser.isAdmin(userId)) {
            menus = menuMapper.selectMenuTreeAll();
        } else {
            menus = menuMapper.selectMenuTreeByUserId(userId);
        }
        return getChildPerms(menus, 0L);
    }

    private List<YxMenu> getChildPerms(List<YxMenu> list, Long parentId) {
        return list.stream()
                .filter(menu -> menu.getParentId().equals(parentId))
                .map(menu -> {
                    menu.setChildren(getChildPerms(list, menu.getId()));
                    return menu;
                })
                .collect(Collectors.toList());
    }
}
