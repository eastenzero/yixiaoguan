package com.yixiaoguan.classroom.service.impl;

import com.ruoyi.common.exception.ServiceException;
import com.yixiaoguan.classroom.domain.YxClassroom;
import com.yixiaoguan.classroom.mapper.YxClassroomMapper;
import com.yixiaoguan.classroom.service.IYxClassroomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 空教室资源 Service 实现类
 */
@Service
public class YxClassroomServiceImpl implements IYxClassroomService {

    @Autowired
    private YxClassroomMapper classroomMapper;

    @Override
    public Map<String, Object> selectPage(String building, Integer status, int pageNum, int pageSize) {
        int offset = (pageNum - 1) * pageSize;
        List<YxClassroom> rows = classroomMapper.selectPage(building, status, offset, pageSize);
        long total = classroomMapper.count(building, status);

        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("rows", rows);
        return result;
    }

    @Override
    public Map<String, Object> selectAvailableList(int pageNum, int pageSize) {
        return selectPage(null, 1, pageNum, pageSize);
    }

    @Override
    public YxClassroom selectById(Long id) {
        YxClassroom classroom = classroomMapper.selectById(id);
        if (classroom == null) {
            throw new ServiceException("教室不存在");
        }
        return classroom;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void insert(YxClassroom classroom) {
        if (classroom.getStatus() == null) {
            classroom.setStatus(1);
        }
        classroomMapper.insert(classroom);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(YxClassroom classroom) {
        YxClassroom exist = classroomMapper.selectById(classroom.getId());
        if (exist == null) {
            throw new ServiceException("教室不存在");
        }
        classroomMapper.update(classroom);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteById(Long id) {
        YxClassroom exist = classroomMapper.selectById(id);
        if (exist == null) {
            throw new ServiceException("教室不存在");
        }
        classroomMapper.deleteById(id);
    }
}
