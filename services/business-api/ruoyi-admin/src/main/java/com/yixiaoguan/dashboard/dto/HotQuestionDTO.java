package com.yixiaoguan.dashboard.dto;

import java.io.Serializable;

/**
 * 高频问题热度统计 DTO
 */
public class HotQuestionDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 问题名称 */
    private String name;

    /** 出现次数 */
    private int count;

    /** 占比百分比 */
    private int percent;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    public int getPercent() {
        return percent;
    }

    public void setPercent(int percent) {
        this.percent = percent;
    }
}
