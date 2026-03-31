package com.yixiaoguan.classroom.mapper;

import com.yixiaoguan.classroom.domain.YxApplicationReview;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 申请审批记录 Mapper 接口 - 对应 yx_application_review 表
 */
@Mapper
public interface YxApplicationReviewMapper {

    /**
     * 分页查询审批记录列表（连表带出审批人、申请信息）
     *
     * @param applicationId 申请单 ID（null 则不过滤）
     * @param reviewerId    审批人 ID（null 则不过滤）
     * @param offset        分页偏移量
     * @param limit         每页条数
     * @return 审批记录列表
     */
    List<YxApplicationReview> selectPage(
            @Param("applicationId") Long applicationId,
            @Param("reviewerId") Long reviewerId,
            @Param("offset") int offset,
            @Param("limit") int limit
    );

    /**
     * 统计审批记录总数
     *
     * @param applicationId 申请单 ID（null 则不过滤）
     * @param reviewerId    审批人 ID（null 则不过滤）
     * @return 总条数
     */
    long count(
            @Param("applicationId") Long applicationId,
            @Param("reviewerId") Long reviewerId
    );

    /**
     * 通过申请单 ID 查询审批记录
     *
     * @param applicationId 申请单 ID
     * @return 审批记录
     */
    YxApplicationReview selectByApplicationId(@Param("applicationId") Long applicationId);

    /**
     * 通过主键查询审批记录详情
     *
     * @param id 记录 ID
     * @return 审批记录详情
     */
    YxApplicationReview selectById(@Param("id") Long id);

    /**
     * 新增审批记录
     *
     * @param review 审批记录对象
     * @return 影响行数
     */
    int insert(YxApplicationReview review);

    /**
     * 软删除审批记录
     *
     * @param id 记录 ID
     * @return 影响行数
     */
    int deleteById(@Param("id") Long id);
}
