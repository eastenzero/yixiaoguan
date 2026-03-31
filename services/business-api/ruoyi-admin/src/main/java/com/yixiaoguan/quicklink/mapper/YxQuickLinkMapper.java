package com.yixiaoguan.quicklink.mapper;

import com.yixiaoguan.quicklink.domain.YxQuickLink;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 快捷链接 Mapper 接口 - 对应 yx_quick_link 表
 */
@Mapper
public interface YxQuickLinkMapper {

    /**
     * 分页查询快捷链接列表
     *
     * @param name     链接名称模糊查询（null 则不过滤）
     * @param category 分类（null 则不过滤）
     * @param isActive 是否启用（null 则不过滤）
     * @param offset   分页偏移量
     * @param limit    每页条数
     * @return 链接列表
     */
    List<YxQuickLink> selectPage(
            @Param("name") String name,
            @Param("category") String category,
            @Param("isActive") Boolean isActive,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计链接总数
     *
     * @param name     链接名称模糊查询（null 则不过滤）
     * @param category 分类（null 则不过滤）
     * @param isActive 是否启用（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("name") String name,
            @Param("category") String category,
            @Param("isActive") Boolean isActive
    );

    /**
     * 通过主键查询链接详情
     *
     * @param id 链接 ID
     * @return 链接详情
     */
    YxQuickLink selectById(@Param("id") Long id);

    /**
     * 新增快捷链接
     *
     * @param quickLink 链接对象
     * @return 影响行数
     */
    int insert(YxQuickLink quickLink);

    /**
     * 更新快捷链接
     *
     * @param quickLink 链接对象
     * @return 影响行数
     */
    int update(YxQuickLink quickLink);

    /**
     * 更新点击次数
     *
     * @param id 链接 ID
     * @return 影响行数
     */
    int incrementClickCount(@Param("id") Long id);

    /**
     * 软删除快捷链接
     *
     * @param id 链接 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
