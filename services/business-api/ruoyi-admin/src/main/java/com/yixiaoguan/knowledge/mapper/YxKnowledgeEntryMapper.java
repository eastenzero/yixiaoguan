package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeEntry;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识条目 Mapper 接口 - 对应 yx_knowledge_entry 表
 */
@Mapper
public interface YxKnowledgeEntryMapper {

    /**
     * 分页查询知识条目列表（连表带出分类名、作者名、来源文件名）
     *
     * @param categoryId 分类 ID（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @param title      标题模糊查询（null 则不过滤）
     * @param offset     分页偏移量
     * @param limit      每页条数
     * @return 条目列表
     */
    List<YxKnowledgeEntry> selectPage(
            @Param("categoryId") Long categoryId,
            @Param("status") Integer status,
            @Param("title") String title,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计条目总数（与分页查询配对）
     *
     * @param categoryId 分类 ID（null 则不过滤）
     * @param status     状态（null 则不过滤）
     * @param title      标题模糊查询（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("categoryId") Long categoryId,
            @Param("status") Integer status,
            @Param("title") String title
    );

    /**
     * 通过主键查询条目详情（连表扩展字段）
     *
     * @param id 条目 ID
     * @return 条目详情
     */
    YxKnowledgeEntry selectById(@Param("id") Long id);

    /**
     * 新增知识条目
     *
     * @param entry 条目对象
     * @return 影响行数
     */
    int insert(YxKnowledgeEntry entry);

    /**
     * 更新知识条目（不含状态字段，状态由专用方法控制）
     *
     * @param entry 条目对象
     * @return 影响行数
     */
    int update(YxKnowledgeEntry entry);

    /**
     * 更新条目状态（状态机流转专用）
     *
     * @param id      条目 ID
     * @param status  新状态
     * @param version 新版本号（审核通过或编辑时递增）
     * @return 影响行数
     */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status, @Param("version") Integer version);

    /**
     * 更新发布时间和版本（审核通过时调用）
     *
     * @param id      条目 ID
     * @param status  新状态
     * @param version 新版本号
     * @return 影响行数
     */
    int updatePublishInfo(@Param("id") Long id, @Param("status") Integer status, @Param("version") Integer version);

    /**
     * 软删除条目
     *
     * @param id 条目 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
