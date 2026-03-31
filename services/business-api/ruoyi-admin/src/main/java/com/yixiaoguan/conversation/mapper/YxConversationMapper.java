package com.yixiaoguan.conversation.mapper;

import com.yixiaoguan.conversation.domain.YxConversation;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 会话 Mapper 接口 - 对应 yx_conversation 表
 */
@Mapper
public interface YxConversationMapper {

    /**
     * 通过 user_id 分页查询会话列表（连表带出学生、教师姓名）
     *
     * @param userId 用户 ID
     * @param status 会话状态（null 则不过滤）
     * @param offset 分页偏移量
     * @param limit  每页条数
     * @return 会话列表
     */
    List<YxConversation> selectPageByUserId(
            @Param("userId") Long userId,
            @Param("status") Integer status,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计 user_id 下的会话总数（与分页查询配对）
     *
     * @param userId 用户 ID
     * @param status 会话状态（null 则不过滤）
     * @return 总条数
     */
    long countByUserId(@Param("userId") Long userId, @Param("status") Integer status);

    /**
     * 通过主键查询会话（连表带出学生、教师姓名）
     *
     * @param id 会话 ID
     * @return 会话详情
     */
    YxConversation selectById(@Param("id") Long id);

    /**
     * 新建会话
     *
     * @param conversation 会话对象
     * @return 影响行数
     */
    int insert(YxConversation conversation);

    /**
     * 更新会话标题
     *
     * @param id    会话 ID
     * @param title 新标题
     * @return 影响行数
     */
    int updateTitle(@Param("id") Long id, @Param("title") String title);

    /**
     * 更新会话状态（软状态机流转使用，不直接暴露给 Controller raw 调用）
     *
     * @param id     会话 ID
     * @param status 新状态
     * @return 影响行数
     */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    /**
     * 教师加入会话：更新状态为 2，记录教师 ID 和加入时间
     *
     * @param id        会话 ID
     * @param teacherId 教师用户 ID
     * @return 影响行数
     */
    int updateTeacherJoin(@Param("id") Long id, @Param("teacherId") Long teacherId);

    /**
     * 教师离开会话：清空教师 ID，状态回到 1-进行中
     *
     * @param id 会话 ID
     * @return 影响行数
     */
    int updateTeacherLeave(@Param("id") Long id);

    /**
     * 更新最后消息时间和消息总数（发送消息后同步调用）
     *
     * @param id           会话 ID
     * @return 影响行数
     */
    int updateLastMessageInfo(@Param("id") Long id);

    /**
     * 软删除（关闭）会话
     *
     * @param id 会话 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
