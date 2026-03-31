package com.yixiaoguan.conversation.mapper;

import com.yixiaoguan.conversation.domain.YxEscalation;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 问题上报工单 Mapper 接口 - 对应 yx_escalation 表
 */
@Mapper
public interface YxEscalationMapper {

    /**
     * 通过主键查询工单（连表带出学生、教师姓名）
     *
     * @param id 工单 ID
     * @return 工单详情
     */
    YxEscalation selectById(@Param("id") Long id);

    /**
     * 通过教师 ID 分页查询已分配的工单（连表带出学生姓名、班级）
     *
     * @param teacherId 教师 ID
     * @param status    工单状态（null 则不过滤）
     * @param offset    分页偏移量
     * @param limit     每页条数
     * @return 工单列表
     */
    List<YxEscalation> selectPageByTeacherId(
            @Param("teacherId") Long teacherId,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计教师可见工单总数
     *
     * @param teacherId 教师 ID
     * @param status    工单状态（null 则不过滤）
     * @return 总条数
     */
    long countByTeacherId(@Param("teacherId") Long teacherId, @Param("status") Integer status);

    /**
     * 通过学生 ID 分页查询自己提交的工单
     *
     * @param studentId 学生 ID
     * @param status    工单状态（null 则不过滤）
     * @param offset    分页偏移量
     * @param limit     每页条数
     * @return 工单列表
     */
    List<YxEscalation> selectPageByStudentId(
            @Param("studentId") Long studentId,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计学生工单总数
     *
     * @param studentId 学生 ID
     * @param status    工单状态（null 则不过滤）
     * @return 总条数
     */
    long countByStudentId(@Param("studentId") Long studentId, @Param("status") Integer status);

    /**
     * 查询待处理的工单（未分配教师）
     *
     * @param offset 分页偏移量
     * @param limit  每页条数
     * @return 工单列表
     */
    List<YxEscalation> selectPendingPage(@Param("offset") int offset, @Param("limit") int limit);

    /**
     * 统计待处理工单总数
     *
     * @return 总条数
     */
    long countPending();

    /**
     * 新建工单
     *
     * @param escalation 工单对象
     * @return 影响行数
     */
    int insert(YxEscalation escalation);

    /**
     * 更新工单状态
     *
     * @param id     工单 ID
     * @param status 新状态
     * @return 影响行数
     */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    /**
     * 分配教师（设置 teacher_id，并更新状态为 1-处理中）
     *
     * @param id        工单 ID
     * @param teacherId 教师 ID
     * @return 影响行数
     */
    int assignTeacher(@Param("id") Long id, @Param("teacherId") Long teacherId);

    /**
     * 教师回复并解决工单（写入 teacher_reply，更新状态和 resolved_at）
     *
     * @param id           工单 ID
     * @param teacherReply 回复内容
     * @return 影响行数
     */
    int resolve(@Param("id") Long id, @Param("teacherReply") String teacherReply);
}
