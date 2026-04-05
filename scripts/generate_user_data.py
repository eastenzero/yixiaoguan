#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成学生和教师（辅导员）数据模型及 SQL 插入脚本
用于"医小管"学术智治系统测试数据准备

FIX-1 修复：
- 列名对齐 yx_schema.sql：nickname（非 nick_name）、department（非 dept_name）
- 删除不存在的 user_type 列
- 新增 student_id / employee_id 列
- 密码使用 Python bcrypt 预先哈希（$2a$ 开头）
- status 显式设为 1（激活）
- 生成 yx_role 和 yx_user_role 初始化 SQL
- BCrypt 哈希使用 E'' 转义避免 $ 符号问题
"""

import pandas as pd
import random
import json
import re
import bcrypt
import argparse
import sys
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

# 角色定义（与 yx_role 表对应）
ROLES = [
    {'id': 1, 'role_key': 'admin', 'role_name': '管理员'},
    {'id': 2, 'role_key': 'student', 'role_name': '学生'},
    {'id': 3, 'role_key': 'teacher', 'role_name': '教师'},
]


def hash_password(password: str) -> str:
    """使用 bcrypt 对密码进行哈希，返回 $2a$ 开头的字符串"""
    # 使用 $2a$ 前缀的 salt（与 Spring Security BCryptPasswordEncoder 兼容）
    salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def escape_sql_string(value: str) -> str:
    """转义 SQL 字符串中的特殊字符"""
    if value is None:
        return ''
    return value.replace("'", "''")


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
        
        # 生成用户名（控制在20字符以内）
        username = f"{surname_pinyin}_{first_char_pinyin}_{dept_code}_{grade_suffix}"
        if len(username) > 20:
            username = f"{surname_pinyin}_{first_char_pinyin}_{grade_suffix}"
        if len(username) > 20:
            username = f"{surname_pinyin}_{grade_suffix}"
        
        # 密码为全拼音
        password_plain = full_pinyin
        password_hashed = hash_password(password_plain)
        
        teachers.append({
            'username': username,
            'password_plain': password_plain,
            'password_hashed': password_hashed,
            'real_name': name,
            'department': dept,
            'grade': grade,
        })
    
    return teachers


def generate_role_sql() -> str:
    """生成 yx_role 角色初始化 SQL"""
    lines = [
        "-- yx_role 角色初始化",
        "-- 生成时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "",
        "-- 清空旧角色数据（谨慎使用，生产环境建议注释）",
        "-- TRUNCATE TABLE yx_user_role CASCADE;",
        "-- TRUNCATE TABLE yx_role CASCADE;",
        "",
        "INSERT INTO yx_role (id, role_key, role_name, sort_order, status, remark) VALUES"
    ]
    
    values = []
    for role in ROLES:
        value = f"  ({role['id']}, '{role['role_key']}', '{role['role_name']}', {role['id']}, 1, '系统初始化角色')"
        values.append(value)
    
    lines.append(',\n'.join(values) + ';')
    lines.append("")
    
    return '\n'.join(lines)


def generate_sql_students(students_data, mapping) -> str:
    """生成学生 SQL 插入语句"""
    sql_lines = [
        "-- 学生数据插入脚本",
        "-- 生成时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "-- 学生数量: {}".format(len(students_data)),
        "-- 注意：密码已使用 BCrypt 预哈希（$2a$ 开头）",
        "",
        "-- 插入学生用户",
        "INSERT INTO yx_user (username, password, real_name, nickname, student_id, department, major, grade, class_name, status, is_deleted, created_at, updated_at) VALUES"
    ]
    
    values = []
    for s in students_data:
        original_id = str(s['学号'])
        obfuscated_id = mapping['student_mapping'][original_id]['obfuscated_id']
        obfuscated_name = mapping['student_mapping'][original_id]['obfuscated_name']
        
        # 使用混淆后的学号作为密码，并预先哈希
        password_plain = obfuscated_id
        password_hashed = hash_password(password_plain)
        
        # 使用 E'' 转义避免 $ 符号问题
        escaped_password = escape_sql_string(password_hashed)
        escaped_name = escape_sql_string(obfuscated_name)
        escaped_dept = escape_sql_string(s['学生所在学院'])
        escaped_major = escape_sql_string(s['专业'])
        escaped_class = escape_sql_string(s['班级'])
        escaped_grade = escape_sql_string(s['年级'])
        
        value = (
            f"  ('{obfuscated_id}', E'{escaped_password}', '{escaped_name}', '{escaped_name}', "
            f"'{obfuscated_id}', '{escaped_dept}', '{escaped_major}', '{escaped_grade}', '{escaped_class}', "
            f"1, FALSE, NOW(), NOW())"
        )
        values.append(value)
    
    sql_lines.append(',\n'.join(values) + ';')
    
    # 添加用户角色关联（使用子查询关联学生角色 role_id=2）
    sql_lines.extend([
        "",
        "-- 关联学生角色 (role_id = 2)",
        "-- 注意：关联 student_id 不为空的用户（学生）",
        "INSERT INTO yx_user_role (user_id, role_id, created_at, updated_at)",
        "SELECT id, 2, NOW(), NOW() FROM yx_user WHERE student_id IS NOT NULL AND student_id != ''",
        "ON CONFLICT (user_id, role_id) DO NOTHING;"
    ])
    
    return '\n'.join(sql_lines)


def generate_sql_teachers(teachers_data) -> str:
    """生成教师 SQL 插入语句"""
    sql_lines = [
        "-- 教师（辅导员）数据插入脚本",
        "-- 生成时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "-- 教师数量: {}".format(len(teachers_data)),
        "-- 注意：密码已使用 BCrypt 预哈希（$2a$ 开头）",
        "",
        "-- 插入教师用户",
        "INSERT INTO yx_user (username, password, real_name, nickname, employee_id, department, grade, status, is_deleted, created_at, updated_at) VALUES"
    ]
    
    values = []
    for idx, t in enumerate(teachers_data):
        # 使用索引作为临时 employee_id（因为没有真实工号）
        employee_id = f"T{idx+1:04d}"
        
        # 使用 E'' 转义避免 $ 符号问题
        escaped_password = escape_sql_string(t['password_hashed'])
        escaped_name = escape_sql_string(t['real_name'])
        escaped_dept = escape_sql_string(t['department'])
        escaped_grade = escape_sql_string(t['grade'])
        
        value = (
            f"  ('{t['username']}', E'{escaped_password}', '{escaped_name}', '{escaped_name}', "
            f"'{employee_id}', '{escaped_dept}', '{escaped_grade}', 1, FALSE, NOW(), NOW())"
        )
        values.append(value)
    
    sql_lines.append(',\n'.join(values) + ';')
    
    # 添加用户角色关联（使用子查询关联教师角色 role_id=3）
    sql_lines.extend([
        "",
        "-- 关联教师角色 (role_id = 3)",
        "-- 注意：关联 employee_id 不为空的用户（教师）",
        "INSERT INTO yx_user_role (user_id, role_id, created_at, updated_at)",
        "SELECT id, 3, NOW(), NOW() FROM yx_user WHERE employee_id IS NOT NULL AND employee_id != '' AND student_id IS NULL",
        "ON CONFLICT (user_id, role_id) DO NOTHING;"
    ])
    
    return '\n'.join(sql_lines)


def generate_test_data():
    """生成测试数据（当没有 Excel 文件时使用）"""
    # 生成 5 个测试学生
    test_students = [
        {'学号': 2024010001, '姓名': '张小明', '学生所在学院': '放射学院', '专业': '医学影像学', '年级': '2024级', '班级': '影像1班'},
        {'学号': 2024010002, '姓名': '李小红', '学生所在学院': '放射学院', '专业': '医学影像学', '年级': '2024级', '班级': '影像1班'},
        {'学号': 2024010003, '姓名': '王强', '学生所在学院': '临床与基础医学院（基础医学研究所）', '专业': '临床医学', '年级': '2024级', '班级': '临床1班'},
        {'学号': 2024010004, '姓名': '刘芳', '学生所在学院': '药学院（药物研究所）', '专业': '药学', '年级': '2024级', '班级': '药学1班'},
        {'学号': 2024010005, '姓名': '陈静', '学生所在学院': '护理学院', '专业': '护理学', '年级': '2024级', '班级': '护理1班'},
    ]
    return test_students


def main():
    parser = argparse.ArgumentParser(description='医小管用户数据生成工具')
    parser.add_argument('--dry-run', action='store_true', help='仅生成 SQL 不写入文件')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR, help='输出目录')
    parser.add_argument('--excel-path', type=str, default=EXCEL_PATH, help='Excel 文件路径')
    parser.add_argument('--test', action='store_true', help='使用测试数据（无需 Excel 文件）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("医小管 - 用户数据生成工具 (FIX-1 修复版)")
    print("=" * 60)
    
    try:
        # 1. 读取数据
        if args.test:
            print(f"\n[1/5] 使用测试数据...")
            students_data = generate_test_data()
            print(f"      测试学生数: {len(students_data)}")
        else:
            print(f"\n[1/5] 读取 Excel 文件...")
            df = pd.read_excel(args.excel_path)
            print(f"      总行数: {len(df)}")
        
        # 2. 提取并去重学生数据
        print(f"\n[2/5] 提取并去重学生数据...")
        if args.test:
            # 测试数据已经是列表格式
            pass
        else:
            students_df = df[['学号', '姓名', '学生所在学院', '专业', '年级', '班级']].drop_duplicates()
            students_df = students_df.drop_duplicates(subset=['学号'])  # 按学号去重
            print(f"      去重后学生数: {len(students_df)}")
            students_data = students_df.to_dict('records')
        
        print(f"      学生数: {len(students_data)}")
        
        # 3. 混淆学生数据
        print(f"\n[3/5] 混淆学生数据...")
        student_mapping = {}
        for s in students_data:
            original_id = str(int(s['学号']) if isinstance(s['学号'], (int, float)) else s['学号'])
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
        if args.test:
            # 从测试数据中提取学院+年级组合
            dept_grade_set = set()
            for s in students_data:
                dept_grade_set.add((s['学生所在学院'], s['年级']))
            dept_grade_groups = list(dept_grade_set)
        else:
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
        sql_roles = generate_role_sql()
        sql_students = generate_sql_students(students_data, data_mapping)
        sql_teachers = generate_sql_teachers(teachers_data)
        
        # 合并学生 SQL：角色初始化 + 学生插入
        full_student_sql = sql_roles + '\n' + sql_students
        
        if args.dry_run:
            print("\n[Dry Run] SQL 预览（前 3 行学生数据）：")
            preview_lines = sql_students.split('\n')
            for line in preview_lines[:30]:
                print(line)
            print("...")
            print(f"\n[Dry Run] 文件将写入：")
            print(f"  - {args.output_dir}/insert_students.sql")
            print(f"  - {args.output_dir}/insert_teachers.sql")
            print(f"  - {args.output_dir}/data_mapping.json")
        else:
            # 写入文件
            with open(f"{args.output_dir}/insert_students.sql", 'w', encoding='utf-8') as f:
                f.write(full_student_sql)
            
            with open(f"{args.output_dir}/insert_teachers.sql", 'w', encoding='utf-8') as f:
                f.write(sql_teachers)
            
            with open(f"{args.output_dir}/data_mapping.json", 'w', encoding='utf-8') as f:
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
        
        # 验证密码格式
        print(f"\n密码格式验证:")
        if students_data:
            sample_student_id = list(student_mapping.keys())[0]
            sample_obfuscated_id = student_mapping[sample_student_id]['obfuscated_id']
            sample_hash = hash_password(sample_obfuscated_id)
            print(f"  - 学生密码示例: {sample_obfuscated_id} -> {sample_hash[:20]}...")
            print(f"  - 格式正确: {sample_hash.startswith('$2a$')}")
        if teachers_data:
            sample_teacher_hash = teachers_data[0]['password_hashed']
            print(f"  - 教师密码示例: {teachers_data[0]['password_plain']} -> {sample_teacher_hash[:20]}...")
            print(f"  - 格式正确: {sample_teacher_hash.startswith('$2a$')}")
        
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
            dept = t['department']
            teacher_dept_counts[dept] = teacher_dept_counts.get(dept, 0) + 1
        
        for dept, count in sorted(teacher_dept_counts.items(), key=lambda x: -x[1]):
            print(f"  - {dept}: {count}人")
        
        print("\n" + "=" * 60)
        print("处理完成！")
        print("=" * 60)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[错误] 文件未找到: {e}")
        print(f"请确认 Excel 文件路径正确: {args.excel_path}")
        return 1
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
