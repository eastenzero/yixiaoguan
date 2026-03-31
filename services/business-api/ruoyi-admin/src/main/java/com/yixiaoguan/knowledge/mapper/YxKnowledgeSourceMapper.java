package com.yixiaoguan.knowledge.mapper;

import com.yixiaoguan.knowledge.domain.YxKnowledgeSource;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识来源记录 Mapper 接口 - 对应 yx_knowledge_source 表
 */
@Mapper
public interface YxKnowledgeSourceMapper {

    /**
     * 分页查询来源记录（连表带出上传人姓名）
     *
     * @param fileName 文件名模糊查询（null 则不过滤）
     * @param offset   分页偏移量
     * @param limit    每页条数
     * @return 来源记录列表
     */
    List<YxKnowledgeSource> selectPage(
            @Param("fileName") String fileName,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计来源记录总数
     *
     * @param fileName 文件名模糊查询（null 则不过滤）
     * @return 总条数
     */
    long count(@Param("fileName") String fileName);

    /**
     * 通过主键查询来源记录
     *
     * @param id 来源记录 ID
     * @return 来源记录详情
     */
    YxKnowledgeSource selectById(@Param("id") Long id);

    /**
     * 新增来源记录
     *
     * @param source 来源记录对象
     * @return 影响行数
     */
    int insert(YxKnowledgeSource source);

    /**
     * 更新来源记录
     *
     * @param source 来源记录对象
     * @return 影响行数
     */
    int update(YxKnowledgeSource source);

    /**
     * 软删除来源记录
     *
     * @param id 来源记录 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
