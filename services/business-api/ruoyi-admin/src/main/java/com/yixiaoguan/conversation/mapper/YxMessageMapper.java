package com.yixiaoguan.conversation.mapper;

import com.yixiaoguan.conversation.domain.YxMessage;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 消息 Mapper 接口 - 对应 yx_message 表
 */
@Mapper
public interface YxMessageMapper {

    /**
     * 通过会话 ID 检索所有历史消息（按创建时间正序）
     * 连表带出发送者真实姓名
     *
     * @param conversationId 会话 ID
     * @return 消息列表
     */
    List<YxMessage> selectByConversationId(@Param("conversationId") Long conversationId);

    /**
     * 通过会话 ID 分页查询消息（适用于消息很多时的翻页场景）
     *
     * @param conversationId 会话 ID
     * @param offset         分页偏移量
     * @param limit          每页条数
     * @return 消息列表
     */
    List<YxMessage> selectPageByConversationId(
            @Param("conversationId") Long conversationId,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计会话消息总数
     *
     * @param conversationId 会话 ID
     * @return 总条数
     */
    long countByConversationId(@Param("conversationId") Long conversationId);

    /**
     * 通过主键查询单条消息
     *
     * @param id 消息 ID
     * @return 消息
     */
    YxMessage selectById(@Param("id") Long id);

    /**
     * 新增消息
     *
     * @param message 消息对象
     * @return 影响行数（同时通过 useGeneratedKeys 回填 id）
     */
    int insert(YxMessage message);
}
