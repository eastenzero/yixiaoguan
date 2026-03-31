package com.yixiaoguan.quicklink.service;

import com.yixiaoguan.quicklink.domain.YxQuickLink;

import java.util.List;
import java.util.Map;

/**
 * 快捷链接 Service 接口
 */
public interface IYxQuickLinkService {

    /**
     * 分页查询快捷链接列表
     *
     * @param name     链接名称模糊查询（null 则不过滤）
     * @param category 分类（null 则不过滤）
     * @param isActive 是否启用（null 则不过滤）
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数
     * @return 含 total 和 rows 的分页结果
     */
    Map<String, Object> selectPage(String name, String category, Boolean isActive, int pageNum, int pageSize);

    /**
     * 通过 ID 查询链接详情
     *
     * @param id 链接 ID
     * @return 链接详情
     */
    YxQuickLink selectById(Long id);

    /**
     * 新增快捷链接
     *
     * @param quickLink 链接对象
     */
    void insert(YxQuickLink quickLink);

    /**
     * 更新快捷链接
     *
     * @param quickLink 链接对象
     */
    void update(YxQuickLink quickLink);

    /**
     * 删除快捷链接（软删除）
     *
     * @param id 链接 ID
     */
    void deleteById(Long id);

    /**
     * 增加点击次数
     *
     * @param id 链接 ID
     */
    void incrementClickCount(Long id);
}
