#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成学生和教师（辅导员）数据模型及 SQL 插入脚本
用于"医小管"学术智治系统测试数据准备
"""

import pandas as pd
import random
import json
import re
from datetime import datetime
from pypinyin import lazy_pinyin

# 设置随机种子以确保可重复性
random.seed(42)

# ========== 配置 ==========
EXCEL_PATH = r'C:\Users\Administrator\Documents\code\yixiaoguan\_references\2025-2026学年第一学期补、缓考考试安排(1).xlsx'
OUTPUT_DIR = r'C:\Users\Administrator\Documents\code\yixiaoguan\scripts'

# 常见名字用字（用于姓名混淆）
COMMON_NAMES = [
    '伟', '磊', '娜', '敏', '强', '丽', '军', '洋', '勇', '艳', 
    '杰', '娟', '涛', '斌', '燕', '刚', '芳', '秀', '霞', '明',
    '平', '辉', '静', '超', '健', '玲', '龙', '丹', '鹏', '洁'
]

# 真实辅导员风格姓名池
REAL_TEACHER_NAMES = [
    # 两字姓名
    '张伟', '李芳', '王建国', '刘晓明', '陈静', '杨波', '赵敏', '黄磊',
    '周强', '吴丽', '徐军', '孙洋', '马勇', '朱艳', '胡杰', '郭娟',
    '林涛', '何斌', '高燕', '梁刚', '郑芳', '罗霞', '宋明', '谢平',
    '韩辉', '唐静', '冯超', '于健', '董玲', '萧龙', '程丹', '曹鹏',
    '袁洁', '邓平', '许辉', '傅静', '沈超', '曾健', '彭玲', '吕龙',
    # 三字姓名
    '李建国', '王秀兰', '张建军', '刘淑芬', '陈秀英', '杨桂英', '赵淑华',
    '黄玉梅', '周建华', '吴淑珍', '徐志强', '孙桂芝', '马淑兰', '朱玉华',
    '胡志强', '郭淑珍', '林建华', '何玉梅', '高志华', '梁淑芬', '郑建华',
    '罗玉珍', '宋志强', '谢淑华', '韩玉芬', '唐志华', '冯淑珍', '于建华',
]

# 学院代码映射
DEPT_CODES = {
    '放射学院': 'fangshe',
    '临床与基础医学院（基础医学研究所）': 'linchuang',
    '药学院（药物研究所）': 'yaoxue',
    '医学信息与人工智能学院': 'yixuexx',
    '护理学院': 'huli',
    '化学与制药工程学院': 'huaxue',
    '公共卫生与健康管理学院': 'gongwei',
    '生命科学学院': 'shengke',
    '第一附属医院（第一临床学院）': 'fuyi',
    '外国语学院': 'waiyu',
    '附属中心医院（济南中心临床学院）': 'zhongxin',
    '眼科学院': 'yanke',
    '口腔医学院': 'kouqiang',
    '附属省立医院（省立临床学院）': 'shengli',
    '医疗保障学院（山东省医疗保障研究院）': 'yibao',
    '运动医学与康复学院': 'yundong',
    '第二附属医院（第二临床学院）': 'fuer',
    '医药管理学院': 'guanli',
    '生物医学科学学院（省医药生物技术研究中心）': 'shengwu',
    '预防医学科学学院（放射医学研究所）': 'fangsheyx',
    '附属肿瘤医院（肿瘤临床学院）': 'zhongliu',
    '实验动物学院（省实验动物中心）': 'dongwu',
}


def obfuscate_student_id(student_id):
    """混淆学号：随机修改 1-2 位数字"""
    student_id = str(student_id)
    num_changes = random.randint(1, 2)
    id_list = list(student_id)
    
    # 随机选择位置进行修改（除了第一位，避免改变长度）
    positions = random.sample(range(1, len(id_list)), num_changes)
    
    for pos in positions:
        # 替换为一个不同的随机数字
        new_digit = random.choice([d for d in '0123456789' if d != id_list[pos]])
        id_list[pos] = new_digit
    
    return ''.join(id_list)


def obfuscate_name(name):
    """混淆姓名：保持姓氏和第一个字，第二个字随机替换"""
    if len(name) <= 1:
        return name
    
    surname = name[0]  # 姓氏
    first_char = name[1] if len(name) > 1 else ''  # 名字第一个字
    
    if len(name) == 2:
        # 两字姓名：保持姓氏，名字随机替换
        new_name = surname + random.choice(COMMON_NAMES)
    else:
        # 三字及以上姓名：保持姓氏和第一个字，其余随机替换
        second_char = random.choice(COMMON_NAMES)
        new_name = surname + first_char + second_char
    
    return new_name


def generate_teachers(dept_grade_groups):
    """生成辅导员数据"""
    teachers = []
    name_pool = REAL_TEACHER_NAMES.copy()
    random.shuffle(name_pool)
    
    for idx, (dept, grade) in enumerate(dept_grade_groups):
        # 获取姓名
        if idx < len(name_pool):
            name = name_pool[idx]
        else:
            # 如果名字池用完，生成新名字
            surname = random.choice(['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴'])
            name = surname + random.choice(COMMON_NAMES)
        
        # 获取拼音
        pinyin_list = lazy_pinyin(name)
        surname_pinyin = pinyin_list[0]
        first_char_pinyin = pinyin_list[1][0] if len(pinyin_list) > 1 else ''
        full_pinyin = ''.join(pinyin_list)
        
        # 获取学院代码
        dept_code = DEPT_CODES.get(dept, 'other')
        
        # 获取年级后两位
        grade_suffix = grade.replace('级', '')[-2:]
        
        # 生成用户名
        username = f"{surname_pinyin}_{first_char_pinyin}_{dept_code}_{grade_suffix}"
        
        # 密码为全拼音
        password = full_pinyin
        
        teachers.append({
            'username': username,
            'password': password,
            'real_name': name,
            'dept_name': dept,
            'grade': grade,
            'user_type': 'teacher'
        })
    
    return teachers


def generate_sql_students(students_data, mapping):
    """生成学生 SQL 插入语句"""
    sql_lines = [
        "-- 学生数据插入脚本",
        "-- 生成时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "-- 学生数量: {}".format(len(students_data)),
        "",
        "INSERT INTO yx_user (username, password, real_name, nick_name, user_type, dept_name, major, grade, class_name, status, is_deleted) VALUES"
    ]
    
    values = []
    for s in students_data:
        original_id = str(s['学号'])
        obfuscated_id = mapping['student_mapping'][original_id]['obfuscated_id']
        obfuscated_name = mapping['student_mapping'][original_id]['obfuscated_name']
        
        # 使用混淆后的学号作为密码（明文，后端会自动 BCrypt 加密）
        password = obfuscated_id
        
        value = (
            f"  ('{obfuscated_id}', '{password}', '{obfuscated_name}', '{obfuscated_name}', 'student', "
            f"'{s['学生所在学院']}', '{s['专业']}', '{s['年级']}', '{s['班级']}', 1, FALSE)"
        )
        values.append(value)
    
    sql_lines.append(',\n'.join(values) + ';')
    
    # 添加用户角色关联
    sql_lines.extend([
        "",
        "-- 关联学生角色 (假设学生角色ID为 2)",
        "INSERT INTO yx_user_role (user_id, role_id) SELECT id, 2 FROM yx_user WHERE user_type = 'student';"
    ])
    
    return '\n'.join(sql_lines)


def generate_sql_teachers(teachers_data):
    """生成教师 SQL 插入语句"""
    sql_lines = [
        "-- 教师（辅导员）数据插入脚本",
        "-- 生成时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "-- 教师数量: {}".format(len(teachers_data)),
        "",
        "INSERT INTO yx_user (username, password, real_name, nick_name, user_type, dept_name, grade, status, is_deleted) VALUES"
    ]
    
    values = []
    for t in teachers_data:
        value = (
            f"  ('{t['username']}', '{t['password']}', '{t['real_name']}', '{t['real_name']}', 'teacher', "
            f"'{t['dept_name']}', '{t['grade']}', 1, FALSE)"
        )
        values.append(value)
    
    sql_lines.append(',\n'.join(values) + ';')
    
    # 添加用户角色关联
    sql_lines.extend([
        "",
        "-- 关联教师角色 (假设教师角色ID为 3)",
        "INSERT INTO yx_user_role (user_id, role_id) SELECT id, 3 FROM yx_user WHERE user_type = 'teacher';"
    ])
    
    return '\n'.join(sql_lines)


def main():
    print("=" * 60)
    print("医小管 - 用户数据生成工具")
    print("=" * 60)
    
    # 1. 读取 Excel
    print(f"\n[1/5] 读取 Excel 文件...")
    df = pd.read_excel(EXCEL_PATH)
    print(f"      总行数: {len(df)}")
    
    # 2. 提取并去重学生数据
    print(f"\n[2/5] 提取并去重学生数据...")
    students_df = df[['学号', '姓名', '学生所在学院', '专业', '年级', '班级']].drop_duplicates()
    students_df = students_df.drop_duplicates(subset=['学号'])  # 按学号去重
    print(f"      去重后学生数: {len(students_df)}")
    
    # 转换为字典列表
    students_data = students_df.to_dict('records')
    
    # 3. 混淆学生数据
    print(f"\n[3/5] 混淆学生数据...")
    student_mapping = {}
    for s in students_data:
        original_id = str(int(s['学号']))  # 确保纯数字字符串
        original_name = str(s['姓名'])
        
        obfuscated_id = obfuscate_student_id(original_id)
        obfuscated_name = obfuscate_name(original_name)
        
        student_mapping[original_id] = {
            'original_id': original_id,
            'original_name': original_name,
            'obfuscated_id': obfuscated_id,
            'obfuscated_name': obfuscated_name,
            'dept': s['学生所在学院'],
            'major': s['专业'],
            'grade': s['年级'],
            'class': s['班级']
        }
    print(f"      已处理 {len(student_mapping)} 名学生")
    
    # 4. 生成辅导员数据
    print(f"\n[4/5] 生成辅导员数据...")
    dept_grade_groups = students_df.groupby(['学生所在学院', '年级']).size().index.tolist()
    print(f"      学院+年级组合数: {len(dept_grade_groups)}")
    
    teachers_data = generate_teachers(dept_grade_groups)
    print(f"      生成辅导员数: {len(teachers_data)}")
    
    # 5. 生成 SQL 和 JSON 文件
    print(f"\n[5/5] 生成输出文件...")
    
    # 创建完整映射数据
    data_mapping = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'students_count': len(students_data),
        'teachers_count': len(teachers_data),
        'student_mapping': student_mapping,
        'teachers': teachers_data
    }
    
    # 生成 SQL
    sql_students = generate_sql_students(students_data, data_mapping)
    sql_teachers = generate_sql_teachers(teachers_data)
    
    # 写入文件
    with open(f"{OUTPUT_DIR}/insert_students.sql", 'w', encoding='utf-8') as f:
        f.write(sql_students)
    
    with open(f"{OUTPUT_DIR}/insert_teachers.sql", 'w', encoding='utf-8') as f:
        f.write(sql_teachers)
    
    with open(f"{OUTPUT_DIR}/data_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(data_mapping, f, ensure_ascii=False, indent=2)
    
    print(f"      ✓ insert_students.sql")
    print(f"      ✓ insert_teachers.sql")
    print(f"      ✓ data_mapping.json")
    
    # 输出统计信息
    print("\n" + "=" * 60)
    print("数据统计")
    print("=" * 60)
    print(f"\n学生总数: {len(students_data)}")
    print(f"教师总数: {len(teachers_data)}")
    
    print(f"\n各学院学生分布:")
    dept_counts = {}
    for s in students_data:
        dept = s['学生所在学院']
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    for dept, count in sorted(dept_counts.items(), key=lambda x: -x[1]):
        print(f"  - {dept}: {count}人")
    
    print(f"\n各学院辅导员分布:")
    teacher_dept_counts = {}
    for t in teachers_data:
        dept = t['dept_name']
        teacher_dept_counts[dept] = teacher_dept_counts.get(dept, 0) + 1
    
    for dept, count in sorted(teacher_dept_counts.items(), key=lambda x: -x[1]):
        print(f"  - {dept}: {count}人")
    
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
