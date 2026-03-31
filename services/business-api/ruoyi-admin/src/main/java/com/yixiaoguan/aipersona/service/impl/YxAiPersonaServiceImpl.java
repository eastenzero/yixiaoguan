package com.yixiaoguan.aipersona.service.impl;

import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.utils.PageUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.aipersona.domain.YxAiPersona;
import com.yixiaoguan.aipersona.mapper.YxAiPersonaMapper;
import com.yixiaoguan.aipersona.service.IYxAiPersonaService;
import com.yixiaoguan.common.core.domain.YxUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * AI 人设配置 Service 实现
 */
@Service
public class YxAiPersonaServiceImpl implements IYxAiPersonaService {

    @Autowired
    private YxAiPersonaMapper aiPersonaMapper;

    @Override
    public TableDataInfo selectPage(Long teacherId, Integer status) {
        // 若依分页规范：显式调用 startPage
        PageUtils.startPage();
        int offset = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() <= 0 ? 0 
                : (com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageNum() - 1) * com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();
        int limit = com.ruoyi.common.core.page.TableSupport.buildPageRequest().getPageSize();

        List<YxAiPersona> list = aiPersonaMapper.selectPage(teacherId, status, offset, limit);
        long total = aiPersonaMapper.count(teacherId, status);

        TableDataInfo result = new TableDataInfo();
        result.setCode(200);
        result.setMsg("查询成功");
        result.setRows(list);
        result.setTotal(total);
        return result;
    }

    @Override
    public YxAiPersona selectById(Long id) {
        return aiPersonaMapper.selectById(id);
    }

    @Override
    public YxAiPersona selectByTeacherId(Long teacherId) {
        YxAiPersona persona = aiPersonaMapper.selectByTeacherId(teacherId);
        if (persona == null) {
            // 如果没有教师专属人设，返回系统默认
            persona = aiPersonaMapper.selectDefault();
        }
        return persona;
    }

    @Override
    public YxAiPersona selectDefault() {
        return aiPersonaMapper.selectDefault();
    }

    @Override
    public int insert(YxAiPersona persona) {
        // 如果设置了 isDefault=true，需要先取消其他的默认人设
        if (Boolean.TRUE.equals(persona.getIsDefault())) {
            // 这里可以添加取消其他默认人设的逻辑
        }
        
        // 如果没有指定教师，默认为当前登录教师
        if (persona.getTeacherId() == null) {
            YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
            persona.setTeacherId(currentUser != null ? currentUser.getId() : null);
        }
        
        // 设置默认值
        if (persona.getName() == null || persona.getName().isEmpty()) {
            persona.setName("小管");
        }
        if (persona.getStatus() == null) {
            persona.setStatus(1);
        }
        if (persona.getIsDefault() == null) {
            persona.setIsDefault(false);
        }
        
        return aiPersonaMapper.insert(persona);
    }

    @Override
    public int update(YxAiPersona persona) {
        return aiPersonaMapper.update(persona);
    }

    @Override
    public int updateStatus(Long id, Integer status) {
        return aiPersonaMapper.updateStatus(id, status);
    }

    @Override
    public int deleteById(Long id) {
        return aiPersonaMapper.deleteById(id);
    }
}
