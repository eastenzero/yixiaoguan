package com.yixiaoguan.aipersona.service;

import com.yixiaoguan.aipersona.domain.YxAiPersona;
import com.ruoyi.common.core.page.TableDataInfo;

import java.util.List;

/**
 * AI 人设配置 Service 接口
 */
public interface IYxAiPersonaService {

    /**
     * 分页查询 AI 人设列表
     *
     * @param teacherId 所属教师 ID（null 则不过滤）
     * @param status    状态（null 则不过滤）
     * @return 分页数据
     */
    TableDataInfo selectPage(Long teacherId, Integer status);

    /**
     * 通过 ID 查询人设详情
     *
     * @param id 人设 ID
     * @return 人设详情
     */
    YxAiPersona selectById(Long id);

    /**
     * 查询教师的 AI 人设
     *
     * @param teacherId 教师 ID（null 查询系统默认）
     * @return 人设详情
     */
    YxAiPersona selectByTeacherId(Long teacherId);

    /**
     * 查询系统默认人设
     *
     * @return 系统默认人设
     */
    YxAiPersona selectDefault();

    /**
     * 新增 AI 人设
     *
     * @param persona 人设对象
     * @return 影响行数
     */
    int insert(YxAiPersona persona);

    /**
     * 更新 AI 人设
     *
     * @param persona 人设对象
     * @return 影响行数
     */
    int update(YxAiPersona persona);

    /**
     * 更新人设状态
     *
     * @param id     人设 ID
     * @param status 新状态
     * @return 影响行数
     */
    int updateStatus(Long id, Integer status);

    /**
     * 删除 AI 人设（软删除）
     *
     * @param id 人设 ID
     * @return 影响行数
     */
    int deleteById(Long id);
}
