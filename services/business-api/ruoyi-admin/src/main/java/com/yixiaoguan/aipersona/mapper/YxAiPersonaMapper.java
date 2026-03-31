package com.yixiaoguan.aipersona.mapper;

import com.yixiaoguan.aipersona.domain.YxAiPersona;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * AI 人设配置 Mapper 接口 - 对应 yx_ai_persona 表
 */
@Mapper
public interface YxAiPersonaMapper {

    /**
     * 分页查询 AI 人设列表
     *
     * @param teacherId  所属教师 ID（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @param offset     分页偏移量
     * @param limit      每页条数
     * @return 人设列表
     */
    List<YxAiPersona> selectPage(
            @Param("teacherId") Long teacherId,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计人设总数
     *
     * @param teacherId  所属教师 ID（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("teacherId") Long teacherId,
            @Param("status") Integer status
    );

    /**
     * 通过主键查询人设详情
     *
     * @param id 人设 ID
     * @return 人设详情
     */
    YxAiPersona selectById(@Param("id") Long id);

    /**
     * 查询教师的 AI 人设
     *
     * @param teacherId 教师 ID（null 查询系统默认）
     * @return 人设详情
     */
    YxAiPersona selectByTeacherId(@Param("teacherId") Long teacherId);

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
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    /**
     * 软删除 AI 人设
     *
     * @param id 人设 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
