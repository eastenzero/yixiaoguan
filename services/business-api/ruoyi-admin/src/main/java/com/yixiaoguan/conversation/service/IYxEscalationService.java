package com.yixiaoguan.conversation.service;

import com.yixiaoguan.conversation.domain.YxEscalation;

import java.util.Map;

/**
 * 问题上报工单 Service 接口
 */
public interface IYxEscalationService {

    /**
     * 通过主键查询工单详情
     *
     * @param id 工单 ID
     * @return 工单详情
     */
    YxEscalation selectById(Long id);

    /**
     * 学生主动上报问题（trigger_type=1）
     *
     * @param conversationId   来源会话 ID
     * @param messageId        触发上报的消息 ID
     * @param studentId        学生 ID
     * @param questionSummary  问题摘要
     * @param priority         优先级（0低 1中 2高）
     * @return 创建好的工单对象
     */
    YxEscalation createEscalation(Long conversationId, Long messageId,
                                   Long studentId, String questionSummary, Integer priority);

    /**
     * AI 判断自动上报（trigger_type=2），由 ai-service 回调
     *
     * @param conversationId  来源会话 ID
     * @param messageId       触发上报的消息 ID
     * @param studentId       学生 ID
     * @param questionSummary 问题摘要
     * @return 创建好的工单对象
     */
    YxEscalation createAutoEscalation(Long conversationId, Long messageId,
                                       Long studentId, String questionSummary);

    /**
     * 教师查看待处理工单列表（分页）
     *
     * @param pageNum  页码
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPendingPage(int pageNum, int pageSize);

    /**
     * 教师查看已分配给自己的工单（分页）
     *
     * @param teacherId 教师 ID
     * @param status    状态过滤（null 则不过滤）
     * @param pageNum   页码
     * @param pageSize  每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPageByTeacher(Long teacherId, Integer status, int pageNum, int pageSize);

    /**
     * 学生查看自己的工单（分页）
     *
     * @param studentId 学生 ID
     * @param status    状态过滤（null 则不过滤）
     * @param pageNum   页码
     * @param pageSize  每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPageByStudent(Long studentId, Integer status, int pageNum, int pageSize);

    /**
     * 教师接单（分配教师，状态 0→1）
     *
     * @param id        工单 ID
     * @param teacherId 教师 ID
     */
    void assignTeacher(Long id, Long teacherId);

    /**
     * 教师回复并解决（状态 1→2）
     *
     * @param id           工单 ID
     * @param teacherId    教师 ID（身份核对）
     * @param teacherReply 回复内容
     */
    void resolve(Long id, Long teacherId, String teacherReply);

    /**
     * 关闭工单（状态 → 3）
     *
     * @param id       工单 ID
     * @param operatorId 操作人 ID
     */
    void close(Long id, Long operatorId);
}
