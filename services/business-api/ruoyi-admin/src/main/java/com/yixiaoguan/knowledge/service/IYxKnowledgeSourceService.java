package com.yixiaoguan.knowledge.service;

import com.yixiaoguan.knowledge.domain.YxKnowledgeSource;

import java.util.Map;

/**
 * 知识来源记录 Service 接口
 */
public interface IYxKnowledgeSourceService {

    /**
     * 分页查询来源记录
     *
     * @param fileName 文件名模糊查询（null 则不过滤）
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(String fileName, int pageNum, int pageSize);

    /**
     * 通过 ID 查询来源记录
     *
     * @param id 来源记录 ID
     * @return 来源记录详情
     */
    YxKnowledgeSource selectById(Long id);

    /**
     * 新增来源记录
     *
     * @param source 来源记录对象
     */
    void insert(YxKnowledgeSource source);

    /**
     * 更新来源记录
     *
     * @param source 来源记录对象
     */
    void update(YxKnowledgeSource source);

    /**
     * 软删除来源记录
     *
     * @param id 来源记录 ID
     */
    void deleteById(Long id);
}
