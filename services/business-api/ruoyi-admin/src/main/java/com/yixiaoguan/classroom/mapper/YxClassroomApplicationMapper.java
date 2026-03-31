package com.yixiaoguan.classroom.mapper;

import com.yixiaoguan.classroom.domain.YxClassroomApplication;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 空教室申请 Mapper 接口 - 对应 yx_classroom_application 表
 */
@Mapper
public interface YxClassroomApplicationMapper {

    /**
     * 分页查询申请列表（连表带出申请人、教室信息）
     *
     * @param applicantId 申请人 ID（null 则不过滤）
     * @param classroomId 教室 ID（null 则不过滤）
     * @param status      状态（null 则不过滤）
     * @param offset      分页偏移量
     * @param limit       每页条数
     * @return 申请列表
     */
    List<YxClassroomApplication> selectPage(
            @Param("applicantId") Long applicantId,
            @Param("classroomId") Long classroomId,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计申请总数
     *
     * @param applicantId 申请人 ID（null 则不过滤）
     * @param classroomId 教室 ID（null 则不过滤）
     * @param status      状态（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("applicantId") Long applicantId,
            @Param("classroomId") Long classroomId,
            @Param("status") Integer status
    );

    /**
     * 通过主键查询申请详情（连表扩展字段）
     *
     * @param id 申请 ID
     * @return 申请详情
     */
    YxClassroomApplication selectById(@Param("id") Long id);

    /**
     * 新增申请
     *
     * @param application 申请对象
     * @return 影响行数
     */
    int insert(YxClassroomApplication application);

    /**
     * 更新申请信息（不含状态）
     *
     * @param application 申请对象
     * @return 影响行数
     */
    int update(YxClassroomApplication application);

    /**
     * 更新申请状态
     *
     * @param id     申请 ID
     * @param status 新状态
     * @return 影响行数
     */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    /**
     * 软删除申请
     *
     * @param id 申请 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
