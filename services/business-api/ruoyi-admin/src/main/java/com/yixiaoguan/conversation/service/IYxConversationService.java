package com.yixiaoguan.conversation.service;

import com.yixiaoguan.conversation.domain.YxConversation;

import java.util.List;
import java.util.Map;

/**
 * 会话 Service 接口
 */
public interface IYxConversationService {

    /**
     * 分页查询当前用户的会话列表
     *
     * @param userId   用户 ID
     * @param status   会话状态过滤（null 则不过滤）
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPageByUserId(Long userId, Integer status, int pageNum, int pageSize);

    /**
     * 查询指定会话详情（会校验所有权）
     *
     * @param id     会话 ID
     * @param userId 当前登录用户 ID（用于所有权校验）
     * @return 会话详情
     */
    YxConversation selectById(Long id, Long userId);

    /**
     * 创建新会话
     *
     * @param userId 学生用户 ID
     * @param title  会话标题（可为 null，后续由 AI 填充）
     * @return 新建的会话对象（含自增 ID）
     */
    YxConversation createConversation(Long userId, String title);

    /**
     * 更新会话标题
     *
     * @param id     会话 ID
     * @param userId 当前登录用户 ID（所有权校验）
     * @param title  新标题
     */
    void updateTitle(Long id, Long userId, String title);

    /**
     * 教师加入会话（状态流转：任意 → 2）
     *
     * @param conversationId 会话 ID
     * @param teacherId      教师用户 ID
     */
    void teacherJoin(Long conversationId, Long teacherId);

    /**
     * 教师离开会话（状态流转：2 → 1）
     *
     * @param conversationId 会话 ID
     * @param teacherId      教师用户 ID（用于身份核对）
     */
    void teacherLeave(Long conversationId, Long teacherId);

    /**
     * 关闭会话（软删除 + 状态置 0）
     *
     * @param id     会话 ID
     * @param userId 当前登录用户 ID（所有权校验）
     */
    void closeConversation(Long id, Long userId);
}
