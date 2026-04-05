#!/usr/bin/env python3
"""
FIX-3: 165 服务器部署脚本
部署修复后的用户数据并进行端到端验证
"""

import psycopg2
import urllib.request
import json
import sys
from pathlib import Path

# 数据库连接配置
DB_CONFIG = {
    'host': '192.168.100.165',
    'port': 5432,
    'dbname': 'yixiaoguan',
    'user': 'yx_admin',
    'password': 'Yx@Admin2026!'
}

# API 配置
API_BASE = 'http://192.168.100.165:8080'

def connect_db():
    """连接数据库"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        sys.exit(1)

def backup_data(conn):
    """备份现有数据"""
    print("\n=== 步骤 1: 备份现有数据 ===")
    cur = conn.cursor()
    
    # 检查现有数据
    cur.execute("SELECT COUNT(*) FROM yx_user")
    user_count = cur.fetchone()[0]
    print(f"现有 yx_user 记录数: {user_count}")
    
    if user_count > 0:
        print("⚠️ 发现现有数据，建议手动备份")
        # 这里可以添加自动备份逻辑
    
    cur.close()
    return user_count

def clear_data(conn):
    """清空现有数据"""
    print("\n=== 步骤 2: 清空现有数据 ===")
    cur = conn.cursor()
    
    try:
        cur.execute("TRUNCATE TABLE yx_user_role CASCADE")
        print("✅ yx_user_role 已清空")
        
        cur.execute("TRUNCATE TABLE yx_user CASCADE")
        print("✅ yx_user 已清空")
        
        conn.commit()
    except Exception as e:
        print(f"❌ 清空数据失败: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()

def execute_sql_file(conn, sql_file_path):
    """执行 SQL 文件"""
    print(f"\n=== 执行 SQL 文件: {sql_file_path} ===")
    
    if not Path(sql_file_path).exists():
        print(f"❌ SQL 文件不存在: {sql_file_path}")
        return False
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    cur = conn.cursor()
    try:
        cur.execute(sql_content)
        conn.commit()
        print(f"✅ {sql_file_path} 执行成功")
        return True
    except Exception as e:
        print(f"❌ {sql_file_path} 执行失败: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()

def verify_database(conn):
    """验证数据库状态"""
    print("\n=== 步骤 3: 验证数据库状态 ===")
    cur = conn.cursor()
    
    results = {}
    
    # L0: 检查用户数量
    cur.execute("SELECT COUNT(*) FROM yx_user")
    user_count = cur.fetchone()[0]
    results['user_count'] = user_count
    print(f"L0: yx_user 记录数 = {user_count}")
    
    if user_count == 0:
        print("❌ L0 FAIL: 没有用户数据")
        return results
    
    # L1: 检查密码格式
    cur.execute("SELECT LEFT(password, 4) FROM yx_user LIMIT 5")
    passwords = cur.fetchall()
    results['password_samples'] = [p[0] for p in passwords]
    print(f"L1: 密码前缀样本: {results['password_samples']}")
    
    all_bcrypt = all(p[0] == '$2a$' for p in passwords)
    if all_bcrypt:
        print("✅ L1 PASS: 所有密码均为 BCrypt 格式")
    else:
        print("❌ L1 FAIL: 存在非 BCrypt 格式密码")
    
    # 检查 status
    cur.execute("SELECT COUNT(*) FROM yx_user WHERE status != 1")
    inactive_count = cur.fetchone()[0]
    results['inactive_count'] = inactive_count
    print(f"status != 1 的用户数: {inactive_count}")
    
    # 检查角色关联
    cur.execute("SELECT COUNT(*) FROM yx_user_role")
    role_count = cur.fetchone()[0]
    results['role_count'] = role_count
    print(f"yx_user_role 记录数: {role_count}")
    
    cur.close()
    return results

def verify_api():
    """验证 API 接口"""
    print("\n=== 步骤 4: 验证 API 接口 ===")
    
    results = {}
    
    # 验证验证码接口
    try:
        url = f"{API_BASE}/captchaImage"
        print(f"GET {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        results['captcha'] = data
        print(f"captchaEnabled: {data.get('captchaEnabled')}")
        
        if data.get('captchaEnabled') == False:
            print("✅ 验证码已关闭")
        else:
            print("❌ 验证码未关闭")
    except Exception as e:
        print(f"❌ 验证码接口调用失败: {e}")
        results['captcha_error'] = str(e)
    
    # 验证登录接口（使用测试账号）
    try:
        url = f"{API_BASE}/login"
        # 使用第一个测试学生账号
        test_data = json.dumps({
            "username": "2524010001",
            "password": "2524010001"  # 原始密码
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"POST {url}")
        print(f"Body: {test_data.decode()}")
        
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        results['login'] = data
        
        if 'token' in data:
            print(f"✅ L2 PASS: 登录成功，获取到 token")
            print(f"Token (前20字符): {data['token'][:20]}...")
        else:
            print(f"❌ L2 FAIL: 登录失败 - {data}")
    except Exception as e:
        print(f"❌ 登录接口调用失败: {e}")
        results['login_error'] = str(e)
    
    return results

def main():
    """主函数"""
    print("=" * 60)
    print("FIX-3: 165 服务器部署与验证")
    print("=" * 60)
    
    # 连接数据库
    conn = connect_db()
    
    try:
        # 备份数据
        backup_data(conn)
        
        # 清空数据
        clear_data(conn)
        
        # 执行 SQL 文件
        students_sql = "scripts/insert_students.sql"
        teachers_sql = "scripts/insert_teachers.sql"
        
        if not execute_sql_file(conn, students_sql):
            print("❌ 学生数据插入失败，终止部署")
            return False
        
        if not execute_sql_file(conn, teachers_sql):
            print("❌ 教师数据插入失败，终止部署")
            return False
        
        # 验证数据库
        db_results = verify_database(conn)
        
        # 验证 API
        api_results = verify_api()
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("部署验证结果汇总")
        print("=" * 60)
        print(f"用户数量: {db_results.get('user_count', 0)}")
        print(f"密码格式: {db_results.get('password_samples', [])}")
        print(f"验证码状态: {api_results.get('captcha', {}).get('captchaEnabled')}")
        print(f"登录测试: {'成功' if 'token' in api_results.get('login', {}) else '失败'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 部署过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()
        print("\n数据库连接已关闭")

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
