#!/usr/bin/env python3
"""
修复并执行SQL插入脚本
"""
import bcrypt
import json
import psycopg2
import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'yixiaoguan',
    'user': 'yx_admin',
    'password': 'Yx@Admin2026!'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def parse_sql_values(sql_content: str) -> List[Tuple]:
    """解析SQL文件中的VALUES部分"""
    # 标准化行尾符
    sql_content = sql_content.replace('\r\n', '\n')
    # 提取所有值行
    pattern = r"\(([^)]+)\)"
    matches = re.findall(pattern, sql_content)
    
    records = []
    for match in matches:
        # 分割字段
        fields = []
        current = ""
        in_quote = False
        for char in match:
            if char == "'" and (not current or current[-1] != "\\"):
                in_quote = not in_quote
                current += char
            elif char == "," and not in_quote:
                fields.append(current.strip())
                current = ""
            else:
                current += char
        if current.strip():
            fields.append(current.strip())
        
        # 跳过列名行（字段名不以单引号开头，数据值以单引号开头）
        if len(fields) >= 9 and fields[0].startswith("'"):
            records.append(tuple(fields))
    
    return records

def fix_and_insert_students():
    """读取学生SQL并修复列名后插入"""
    with open('scripts/insert_students.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有值
    records = parse_sql_values(content)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted_students = []
    
    print(f"  解析到 {len(records)} 条学生记录")
    
    try:
        # 确保角色存在
        cursor.execute("""
            INSERT INTO yx_role (id, role_key, role_name, sort_order, status) VALUES
            (2, 'student', '学生', 2, 1),
            (3, 'teacher', '教师', 3, 1)
            ON CONFLICT (id) DO UPDATE SET role_key = EXCLUDED.role_key, role_name = EXCLUDED.role_name
        """)
        
        # 重置序列
        cursor.execute("SELECT setval('yx_user_id_seq', COALESCE((SELECT MAX(id) FROM yx_user), 0) + 1, false)")
        
        # 新的列: username, password, real_name, nickname, department, major, grade, class_name, status, is_deleted, student_id
        for fields in records:
            if len(fields) < 11:
                continue
            username = fields[0].strip("'")
            password_plain = fields[1].strip("'")
            password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
            real_name = fields[2].strip("'")
            nickname = fields[3].strip("'")
            department = fields[5].strip("'")
            major = fields[6].strip("'")
            grade = fields[7].strip("'")
            class_name = fields[8].strip("'")
            status = fields[9]
            is_deleted = fields[10]
            
            cursor.execute("""
                INSERT INTO yx_user (username, password, real_name, nickname, department, major, grade, class_name, status, is_deleted, student_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET 
                    real_name = EXCLUDED.real_name,
                    nickname = EXCLUDED.nickname,
                    department = EXCLUDED.department,
                    major = EXCLUDED.major,
                    grade = EXCLUDED.grade,
                    class_name = EXCLUDED.class_name,
                    student_id = EXCLUDED.student_id
                RETURNING id
            """, (username, password, real_name, nickname, department, major, grade, class_name, int(status), is_deleted == 'TRUE' or is_deleted == 'true', username))
            
            result = cursor.fetchone()
            if result:
                inserted_students.append({
                    'id': result[0],
                    'username': username,
                    'real_name': real_name,
                    'dept': department,
                    'grade': grade,
                    'class_name': class_name
                })
        
        conn.commit()
        print(f"✓ 学生数据插入成功，共 {len(inserted_students)} 条")
        
        # 获取角色ID=2
        for student in inserted_students:
            cursor.execute("""
                INSERT INTO yx_user_role (user_id, role_id) 
                VALUES (%s, 2)
                ON CONFLICT (user_id, role_id) DO NOTHING
            """, (student['id'],))
        
        conn.commit()
        print(f"  角色关联完成")
        
        return inserted_students
    except Exception as e:
        conn.rollback()
        print(f"✗ 学生数据插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def fix_and_insert_teachers():
    """读取教师SQL并修复列名后插入"""
    with open('scripts/insert_teachers.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有值
    records = parse_sql_values(content)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted_teachers = []
    
    print(f"  解析到 {len(records)} 条教师记录")
    
    try:
        # 确保角色存在
        cursor.execute("""
            INSERT INTO yx_role (id, role_key, role_name, sort_order, status) VALUES
            (2, 'student', '学生', 2, 1),
            (3, 'teacher', '教师', 3, 1)
            ON CONFLICT (id) DO UPDATE SET role_key = EXCLUDED.role_key, role_name = EXCLUDED.role_name
        """)
        
        # 重置序列
        cursor.execute("SELECT setval('yx_user_id_seq', COALESCE((SELECT MAX(id) FROM yx_user), 0) + 1, false)")
        
        # 教师SQL: username, password, real_name, nick_name, user_type, dept_name, grade, status, is_deleted
        # 新列: username, password, real_name, nickname, department, grade, status, is_deleted, employee_id
        for fields in records:
            if len(fields) < 9:
                print(f"    跳过字段不足的记录: {len(fields)} fields")
                continue
            if len(fields) < 9:
                continue
            username = fields[0].strip("'")
            password_plain = fields[1].strip("'")
            password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
            real_name = fields[2].strip("'")
            nickname = fields[3].strip("'")
            department = fields[5].strip("'")
            grade = fields[6].strip("'")
            status = fields[7]
            is_deleted = fields[8]
            
            cursor.execute("""
                INSERT INTO yx_user (username, password, real_name, nickname, department, grade, status, is_deleted, employee_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET 
                    real_name = EXCLUDED.real_name,
                    nickname = EXCLUDED.nickname,
                    department = EXCLUDED.department,
                    grade = EXCLUDED.grade,
                    employee_id = EXCLUDED.employee_id
                RETURNING id
            """, (username, password, real_name, nickname, department, grade, int(status), is_deleted == 'TRUE' or is_deleted == 'true', username))
            
            result = cursor.fetchone()
            if result:
                inserted_teachers.append({
                    'id': result[0],
                    'username': username,
                    'real_name': real_name,
                    'dept': department,
                    'grade': grade
                })
        
        conn.commit()
        print(f"✓ 教师数据插入成功，共 {len(inserted_teachers)} 条")
        
        # 获取角色ID=3
        for teacher in inserted_teachers:
            cursor.execute("""
                INSERT INTO yx_user_role (user_id, role_id) 
                VALUES (%s, 3)
                ON CONFLICT (user_id, role_id) DO NOTHING
            """, (teacher['id'],))
        
        conn.commit()
        print(f"  角色关联完成")
        
        return inserted_teachers
    except Exception as e:
        conn.rollback()
        print(f"✗ 教师数据插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def generate_user_id_mapping(students, teachers):
    """生成用户ID映射文件"""
    mapping = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "students": students,
        "teachers": teachers
    }
    
    with open('scripts/user_id_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 用户ID映射文件已生成: scripts/user_id_mapping.json")
    return mapping

def generate_conversations(user_mapping, count=300):
    """生成会话数据"""
    students = user_mapping["students"]
    teachers = user_mapping["teachers"]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    conversation_ids = []
    try:
        for i in range(count):
            student = random.choice(students)
            teacher = random.choice([t for t in teachers if t.get("grade") == student.get("grade")] or teachers)
            
            cursor.execute("""
                INSERT INTO yx_conversation (user_id, title, status, teacher_id, last_message_at, message_count)
                VALUES (%s, %s, %s, %s, NOW(), %s)
                RETURNING id
            """, (
                student["id"],
                f"咨询会话 {i+1}",
                random.choice([0, 1]),
                teacher["id"],
                random.randint(1, 20)
            ))
            conversation_ids.append(cursor.fetchone()[0])
        
        conn.commit()
        print(f"✓ 会话数据插入成功，共 {len(conversation_ids)} 条")
        return conversation_ids
    except Exception as e:
        conn.rollback()
        print(f"✗ 会话数据插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def generate_escalations(user_mapping, conversation_ids, count=250):
    """生成提问工单数据"""
    students = user_mapping["students"]
    teachers = user_mapping["teachers"]
    
    # 问题摘要模板
    question_templates = [
        "关于{课程}补考的咨询",
        "奖学金评定政策疑问",
        "宿舍调换申请流程",
        "校园网账号密码重置",
        "选课系统操作问题",
        "学籍异动办理流程",
        "医保报销相关问题",
        "图书馆借阅规则咨询",
        "学生证补办流程",
        "成绩单盖章办理",
        "休学申请流程咨询",
        "转专业政策咨询",
        "助学金申请条件",
        "勤工助学岗位申请",
        "毕业生档案转递问题"
    ]
    
    courses = ["高等数学", "大学英语", "医学概论", "计算机基础", "生理学", "解剖学", "病理学"]
    question_templates = [t.replace("{课程}", "{course}") for t in question_templates]
    
    records = []
    for i in range(count):
        student = random.choice(students)
        teacher = random.choice([t for t in teachers if t.get("grade") == student.get("grade")] or teachers)
        
        # 触发类型: 70%学生主动, 30%AI自动
        trigger_type = 1 if random.random() < 0.7 else 2
        
        # 状态分布: 40%待处理, 30%处理中, 20%已解决, 10%已关闭
        r = random.random()
        if r < 0.4:
            status = 0
        elif r < 0.7:
            status = 1
        elif r < 0.9:
            status = 2
        else:
            status = 3
        
        # 优先级: 10%紧急, 20%高, 50%普通, 20%低
        r = random.random()
        if r < 0.1:
            priority = 3
        elif r < 0.3:
            priority = 2
        elif r < 0.8:
            priority = 1
        else:
            priority = 0
        
        # 生成问题摘要
        template = random.choice(question_templates)
        if "{课程}" in template:
            question_summary = template.format(course=random.choice(courses))
        else:
            question_summary = template
        
        # 创建时间 (最近30天内)
        created_at = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        conversation_id = random.choice(conversation_ids)
        
        # 创建对应的消息
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO yx_message (conversation_id, sender_type, sender_id, content, message_type)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (conversation_id, 1, student["id"], question_summary, 1))
        message_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        records.append({
            "conversation_id": conversation_id,
            "message_id": message_id,
            "student_id": student["id"],
            "teacher_id": teacher["id"],
            "question_summary": question_summary,
            "status": status,
            "priority": priority,
            "trigger_type": trigger_type,
            "created_at": created_at,
            "updated_at": created_at
        })
    
    return records

def generate_classroom_applications(user_mapping, count=125):
    """生成教室申请数据"""
    students = user_mapping["students"]
    
    # 用途模板
    purpose_templates = [
        "班级团建活动",
        "社团例会",
        "学习小组讨论",
        "班会",
        "辩论队训练",
        "创新创业项目讨论",
        "志愿服务培训",
        "学生组织换届选举"
    ]
    
    # 教学楼和教室
    buildings = ["教学楼A", "教学楼B", "实验楼", "图书馆"]
    classrooms = [
        ("教学楼A", "101"), ("教学楼A", "102"), ("教学楼A", "201"), ("教学楼A", "202"),
        ("教学楼B", "101"), ("教学楼B", "102"), ("教学楼B", "201"), ("教学楼B", "202"),
        ("实验楼", "301"), ("实验楼", "302"), ("图书馆", "报告厅"), ("图书馆", "会议室")
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取或创建教室
    classroom_map = {}
    for building, room in classrooms:
        cursor.execute("""
            INSERT INTO yx_classroom (building, room_number, capacity, status)
            VALUES (%s, %s, %s, 1)
            ON CONFLICT (building, room_number) DO UPDATE SET building = %s
            RETURNING id
        """, (building, room, random.randint(30, 100), building))
        result = cursor.fetchone()
        if result:
            classroom_map[(building, room)] = result[0]
    
    conn.commit()
    cursor.close()
    conn.close()
    
    records = []
    for i in range(count):
        student = random.choice(students)
        building, room = random.choice(classrooms)
        classroom_id = classroom_map.get((building, room), 1)
        
        # 状态分布: 30%待审批, 40%已通过, 20%已拒绝, 10%已取消
        r = random.random()
        if r < 0.3:
            status = 0
        elif r < 0.7:
            status = 1
        elif r < 0.9:
            status = 2
        else:
            status = 3
        
        # 申请日期 (未来30天内)
        apply_date = datetime.now() + timedelta(days=random.randint(1, 30))
        start_time = f"{random.randint(8, 18):02d}:00:00"
        end_time = f"{random.randint(int(start_time[:2])+1, 21):02d}:00:00"
        
        created_at = datetime.now() - timedelta(days=random.randint(0, 15))
        
        records.append({
            "applicant_id": student["id"],
            "classroom_id": classroom_id,
            "apply_date": apply_date.strftime("%Y-%m-%d"),
            "start_time": start_time,
            "end_time": end_time,
            "purpose": random.choice(purpose_templates),
            "attendee_count": random.randint(10, 50),
            "contact_phone": f"138{random.randint(10000000, 99999999)}",
            "status": status,
            "created_at": created_at,
            "updated_at": created_at
        })
    
    return records

def generate_knowledge_entries(user_mapping, count=50):
    """生成知识库条目"""
    teachers = user_mapping["teachers"]
    
    # 分类
    categories = [
        {"name": "学工政策", "code": "STUDENT_AFFAIRS"},
        {"name": "教务咨询", "code": "ACADEMIC"},
        {"name": "后勤服务", "code": "LOGISTICS"},
        {"name": "技术故障", "code": "TECH_SUPPORT"},
        {"name": "其他", "code": "OTHER"}
    ]
    
    # 标题模板
    title_templates = {
        "学工政策": [
            "奖学金评定政策详解与申请流程指南",
            "助学金申请条件及发放标准说明",
            "学生违纪处分条例解读",
            "优秀学生评选办法",
            "学生请假制度管理规定"
        ],
        "教务咨询": [
            "选课系统操作手册及常见问题解答",
            "学籍异动办理流程及注意事项",
            "学生成绩单打印及认证流程",
            "补考重修申请流程说明",
            "毕业论文提交规范与时间安排"
        ],
        "后勤服务": [
            "宿舍调换申请流程与注意事项",
            "校园卡挂失与补办流程",
            "食堂投诉建议渠道说明",
            "宿舍水电费缴纳指南",
            "校园快递收取点分布"
        ],
        "技术故障": [
            "校园网账号密码重置操作指南",
            "教务系统登录问题解决方案",
            "VPN使用教程及常见问题",
            "电子邮箱配置指南",
            "打印系统使用说明"
        ],
        "其他": [
            "图书馆电子资源使用指南",
            "学生证的补办流程说明",
            "学生医保报销流程及所需材料",
            "毕业生就业推荐表办理流程",
            "校友联络方式汇总"
        ]
    }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 插入分类
    category_ids = {}
    for cat in categories:
        cursor.execute("""
            INSERT INTO yx_knowledge_category (name, code, description, status)
            VALUES (%s, %s, %s, 1)
            ON CONFLICT (code) DO UPDATE SET name = %s
            RETURNING id
        """, (cat["name"], cat["code"], f"{cat['name']}相关知识点", cat["name"]))
        result = cursor.fetchone()
        if result:
            category_ids[cat["name"]] = result[0]
    
    conn.commit()
    cursor.close()
    conn.close()
    
    records = []
    entries_per_category = count // len(categories)
    
    for cat_name, titles in title_templates.items():
        category_id = category_ids.get(cat_name, 1)
        for title in titles[:entries_per_category]:
            author = random.choice(teachers)
            
            # 状态分布: 20%草稿, 20%待审核, 50%已发布, 10%已下线
            r = random.random()
            if r < 0.2:
                status = 0
            elif r < 0.4:
                status = 1
            elif r < 0.9:
                status = 2
            else:
                status = 3
            
            created_at = datetime.now() - timedelta(days=random.randint(1, 60))
            published_at = None
            if status >= 2:
                published_at = created_at + timedelta(days=random.randint(1, 5))
            
            records.append({
                "category_id": category_id,
                "title": title,
                "content": f"这是关于{title}的详细内容...",
                "summary": f"{title}的简要说明",
                "status": status,
                "author_id": author["id"],
                "published_at": published_at.strftime("%Y-%m-%d %H:%M:%S") if published_at else None,
                "view_count": random.randint(0, 500),
                "hit_count": random.randint(0, 100),
                "created_at": created_at,
                "updated_at": created_at
            })
    
    return records

def generate_sql_file(filename, tablename, records, columns):
    """生成SQL插入文件"""
    lines = [
        f"-- {tablename} 数据插入脚本",
        f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"-- 记录数量: {len(records)}",
        ""
    ]
    
    col_names = ', '.join(columns)
    lines.append(f"INSERT INTO {tablename} ({col_names}) VALUES")
    
    values_list = []
    for record in records:
        values = []
        for col in columns:
            val = record.get(col)
            if val is None:
                values.append("NULL")
            elif isinstance(val, str):
                escaped = val.replace("'", "''")
                values.append(f"'{escaped}'")
            elif isinstance(val, bool):
                values.append("TRUE" if val else "FALSE")
            elif isinstance(val, datetime):
                values.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
            else:
                values.append(str(val))
        values_list.append(f"  ({', '.join(values)})")
    
    lines.append(",\n".join(values_list) + ";")
    
    with open(f'scripts/{filename}', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ 生成SQL文件: scripts/{filename}")

def execute_escalations(records):
    """执行提问工单插入"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for record in records:
            cursor.execute("""
                INSERT INTO yx_escalation (conversation_id, message_id, student_id, teacher_id, 
                    question_summary, status, priority, trigger_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record['conversation_id'], record['message_id'], 
                record['student_id'], record['teacher_id'],
                record['question_summary'], record['status'], 
                record['priority'], record['trigger_type'],
                record['created_at'], record['updated_at']
            ))
        conn.commit()
        print(f"✓ 提问工单插入成功，共 {len(records)} 条")
    except Exception as e:
        conn.rollback()
        print(f"✗ 提问工单插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def execute_classroom_applications(records):
    """执行教室申请插入"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for record in records:
            cursor.execute("""
                INSERT INTO yx_classroom_application (applicant_id, classroom_id, apply_date, 
                    start_time, end_time, purpose, attendee_count, contact_phone, status, 
                    created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record['applicant_id'], record['classroom_id'], 
                record['apply_date'], record['start_time'], record['end_time'],
                record['purpose'], record['attendee_count'], 
                record['contact_phone'], record['status'],
                record['created_at'], record['updated_at']
            ))
        conn.commit()
        print(f"✓ 教室申请插入成功，共 {len(records)} 条")
    except Exception as e:
        conn.rollback()
        print(f"✗ 教室申请插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def execute_knowledge_entries(records):
    """执行知识条目插入"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for record in records:
            cursor.execute("""
                INSERT INTO yx_knowledge_entry (category_id, title, content, summary, status,
                    author_id, published_at, view_count, hit_count, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record['category_id'], record['title'], record['content'], 
                record['summary'], record['status'], record['author_id'],
                record['published_at'], record['view_count'], 
                record['hit_count'], record['created_at'], record['updated_at']
            ))
        conn.commit()
        print(f"✓ 知识条目插入成功，共 {len(records)} 条")
    except Exception as e:
        conn.rollback()
        print(f"✗ 知识条目插入失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def generate_report():
    """生成数据统计报告"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 学生总数
    cursor.execute("SELECT COUNT(*) FROM yx_user WHERE student_id IS NOT NULL AND is_deleted = FALSE")
    student_count = cursor.fetchone()[0]
    print(f"学生总数: {student_count}")
    
    # 教师总数
    cursor.execute("SELECT COUNT(*) FROM yx_user WHERE employee_id IS NOT NULL AND is_deleted = FALSE")
    teacher_count = cursor.fetchone()[0]
    print(f"教师总数: {teacher_count}")
    
    # 提问工单按状态分布
    cursor.execute("""
        SELECT status, COUNT(*) FROM yx_escalation 
        WHERE is_deleted = FALSE GROUP BY status ORDER BY status
    """)
    escalation_stats = cursor.fetchall()
    print(f"\n提问工单统计:")
    status_names = {0: "待处理", 1: "处理中", 2: "已解决", 3: "已关闭"}
    for status, count in escalation_stats:
        print(f"  - {status_names.get(status, status)}: {count}")
    cursor.execute("SELECT COUNT(*) FROM yx_escalation WHERE is_deleted = FALSE")
    total = cursor.fetchone()[0]
    print(f"  总计: {total}")
    
    # 教室申请按状态分布
    cursor.execute("""
        SELECT status, COUNT(*) FROM yx_classroom_application 
        WHERE is_deleted = FALSE GROUP BY status ORDER BY status
    """)
    application_stats = cursor.fetchall()
    print(f"\n教室申请统计:")
    status_names = {0: "待审批", 1: "已通过", 2: "已拒绝", 3: "已取消"}
    for status, count in application_stats:
        print(f"  - {status_names.get(status, status)}: {count}")
    cursor.execute("SELECT COUNT(*) FROM yx_classroom_application WHERE is_deleted = FALSE")
    total = cursor.fetchone()[0]
    print(f"  总计: {total}")
    
    # 知识条目按分类分布
    cursor.execute("""
        SELECT kc.name, COUNT(*) FROM yx_knowledge_entry ke
        JOIN yx_knowledge_category kc ON ke.category_id = kc.id
        WHERE ke.is_deleted = FALSE GROUP BY kc.name
    """)
    entry_stats = cursor.fetchall()
    print(f"\n知识条目统计:")
    for name, count in entry_stats:
        print(f"  - {name}: {count}")
    cursor.execute("SELECT COUNT(*) FROM yx_knowledge_entry WHERE is_deleted = FALSE")
    total = cursor.fetchone()[0]
    print(f"  总计: {total}")
    
    cursor.close()
    conn.close()

def main():
    print("=" * 60)
    print("医小管测试数据生成工具")
    print("=" * 60)
    
    # 阶段1: 插入基础数据
    print("\n【阶段1】插入学生和教师数据")
    print("-" * 40)
    
    students = fix_and_insert_students()
    teachers = fix_and_insert_teachers()
    
    # 生成用户ID映射
    print("\n【阶段2】生成用户ID映射")
    print("-" * 40)
    user_mapping = generate_user_id_mapping(students, teachers)
    
    # 阶段2: 生成业务数据SQL
    print("\n【阶段3】生成业务测试数据")
    print("-" * 40)
    
    # 首先生成会话数据
    conversation_ids = generate_conversations(user_mapping, count=300)
    
    # 生成提问工单
    escalations = generate_escalations(user_mapping, conversation_ids, count=250)
    generate_sql_file('insert_escalations.sql', 'yx_escalation', escalations, [
        'conversation_id', 'message_id', 'student_id', 'teacher_id', 
        'question_summary', 'status', 'priority', 'trigger_type',
        'created_at', 'updated_at'
    ])
    execute_escalations(escalations)
    
    # 生成教室申请
    applications = generate_classroom_applications(user_mapping, count=125)
    generate_sql_file('insert_classroom_applications.sql', 'yx_classroom_application', applications, [
        'applicant_id', 'classroom_id', 'apply_date', 'start_time', 'end_time',
        'purpose', 'attendee_count', 'contact_phone', 'status',
        'created_at', 'updated_at'
    ])
    execute_classroom_applications(applications)
    
    # 生成知识条目
    entries = generate_knowledge_entries(user_mapping, count=50)
    generate_sql_file('insert_knowledge_entries.sql', 'yx_knowledge_entry', entries, [
        'category_id', 'title', 'content', 'summary', 'status',
        'author_id', 'published_at', 'view_count', 'hit_count',
        'created_at', 'updated_at'
    ])
    execute_knowledge_entries(entries)
    
    # 生成统计报告
    print("\n【阶段4】数据统计报告")
    print("-" * 40)
    generate_report()
    
    print("\n" + "=" * 60)
    print("数据生成完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
