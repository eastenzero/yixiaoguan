package com.yixiaoguan.classroom.mapper;

import com.yixiaoguan.classroom.domain.YxClassroom;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 空教室资源 Mapper 接口 - 对应 yx_classroom 表
 */
@Mapper
public interface YxClassroomMapper {

    /**
     * 分页查询空教室列表
     *
     * @param building   教学楼名称（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @param offset     分页偏移量
     * @param limit      每页条数
     * @return 教室列表
     */
    List<YxClassroom> selectPage(
            @Param("building") String building,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计教室总数
     *
     * @param building 教学楼名称（null 则不过滤）
     * @param status   状态（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("building") String building,
            @Param("status") Integer status
    );

    /**
     * 通过主键查询教室详情
     *
     * @param id 教室 ID
     * @return 教室详情
     */
    YxClassroom selectById(@Param("id") Long id);

    /**
     * 新增教室
     *
     * @param classroom 教室对象
     * @return 影响行数
     */
    int insert(YxClassroom classroom);

    /**
     * 更新教室信息
     *
     * @param classroom 教室对象
     * @return 影响行数
     */
    int update(YxClassroom classroom);

    /**
     * 软删除教室
     *
     * @param id 教室 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
