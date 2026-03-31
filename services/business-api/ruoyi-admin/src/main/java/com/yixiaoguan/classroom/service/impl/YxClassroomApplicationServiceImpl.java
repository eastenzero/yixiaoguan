package com.yixiaoguan.classroom.service.impl;

import com.alibaba.fastjson2.JSON;
import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.classroom.domain.YxApplicationReview;
import com.yixiaoguan.classroom.domain.YxClassroomApplication;
import com.yixiaoguan.classroom.mapper.YxApplicationReviewMapper;
import com.yixiaoguan.classroom.mapper.YxClassroomApplicationMapper;
import com.yixiaoguan.classroom.service.IYxClassroomApplicationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 空教室申请 Service 实现类
 * 包含完整的申请提交与审批状态流转逻辑
 */
@Service
public class YxClassroomApplicationServiceImpl implements IYxClassroomApplicationService {

    @Autowired
    private YxClassroomApplicationMapper applicationMapper;

    @Autowired
    private YxApplicationReviewMapper reviewMapper;

    @Override
    public Map<String, Object> selectPage(Long applicantId, Long classroomId, Integer status, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxClassroomApplication> rows = applicationMapper.selectPage(applicantId, classroomId, status, offset, pageSize);

        for (YxClassroomApplication row : rows) {
            parseAttachments(row);
        }

        long total = applicationMapper.count(applicantId, classroomId, status);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public YxClassroomApplication selectById(Long id) {
        YxClassroomApplication application = applicationMapper.selectById(id);
        if (application == null) {
            throw new ServiceException("申请记录不存在");
        }
        parseAttachments(application);
        return application;
    }

    /**
     * 解析附件 JSON 字符串为列表
     */
    private void parseAttachments(YxClassroomApplication application) {
        if (StringUtils.hasText(application.getAttachments())) {
            try {
                List<String> attachmentList = JSON.parseArray(application.getAttachments(), String.class);
                application.setAttachmentList(attachmentList);
            } catch (Exception e) {
                application.setAttachmentList(null);
            }
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public YxClassroomApplication submitApplication(YxClassroomApplication application, Long applicantId) {
        application.setApplicantId(applicantId);
        application.setStatus(0);

        if (application.getAttachmentList() != null && !application.getAttachmentList().isEmpty()) {
            application.setAttachments(JSON.toJSONString(application.getAttachmentList()));
        }

        applicationMapper.insert(application);
        return applicationMapper.selectById(application.getId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void approve(Long applicationId, Long reviewerId, String opinion) {
        YxClassroomApplication application = applicationMapper.selectById(applicationId);
        if (application == null) {
            throw new ServiceException("申请记录不存在");
        }

        if (application.getStatus() != 0) {
            throw new ServiceException("仅待审批状态的申请可执行通过操作");
        }

        applicationMapper.updateStatus(applicationId, 1);

        YxApplicationReview review = new YxApplicationReview();
        review.setApplicationId(applicationId);
        review.setReviewerId(reviewerId);
        review.setAction(1);
        review.setOpinion(opinion);
        reviewMapper.insert(review);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void reject(Long applicationId, Long reviewerId, String opinion) {
        YxClassroomApplication application = applicationMapper.selectById(applicationId);
        if (application == null) {
            throw new ServiceException("申请记录不存在");
        }

        if (application.getStatus() != 0) {
            throw new ServiceException("仅待审批状态的申请可执行拒绝操作");
        }

        applicationMapper.updateStatus(applicationId, 2);

        YxApplicationReview review = new YxApplicationReview();
        review.setApplicationId(applicationId);
        review.setReviewerId(reviewerId);
        review.setAction(2);
        review.setOpinion(opinion);
        reviewMapper.insert(review);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void cancel(Long applicationId, Long applicantId) {
        YxClassroomApplication application = applicationMapper.selectById(applicationId);
        if (application == null) {
            throw new ServiceException("申请记录不存在");
        }

        if (!application.getApplicantId().equals(applicantId)) {
            throw new ServiceException("无权取消他人申请");
        }

        if (application.getStatus() != 0) {
            throw new ServiceException("仅待审批状态的申请可取消");
        }

        applicationMapper.updateStatus(applicationId, 3);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxClassroomApplication application = applicationMapper.selectById(id);
        if (application == null) {
            throw new ServiceException("申请记录不存在");
        }
        applicationMapper.deleteById(id);
    }
}
