#!/usr/bin/env python3
# 检查 165 服务器验证码配置

import psycopg2
import urllib.request
import json

def check_db_config():
    """检查 sys_config 表中验证码配置"""
    print("=== 检查数据库配置 ===")
    try:
        conn = psycopg2.connect(
            host='192.168.100.165',
            port=5432,
            dbname='yixiaoguan',
            user='yx_admin',
            password='Yx@Admin2026!'
        )
        cur = conn.cursor()
        cur.execute("SELECT config_key, config_value FROM sys_config WHERE config_key='sys.account.captchaEnabled'")
        result = cur.fetchall()
        cur.close()
        conn.close()
        
        if result:
            for row in result:
                print(f"config_key: {row[0]}")
                print(f"config_value: {row[1]}")
            return result[0][1]
        else:
            print("未找到 sys.account.captchaEnabled 配置")
            return None
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def check_api_response():
    """检查 captchaImage 接口返回"""
    print("\n=== 检查 API 接口 ===")
    try:
        url = 'http://192.168.100.165:8080/captchaImage'
        print(f"执行: curl {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode()
        print(f"返回: {data}")
        
        json_data = json.loads(data)
        captcha_enabled = json_data.get('captchaEnabled')
        print(f"captchaEnabled: {captcha_enabled}")
        return captcha_enabled
    except Exception as e:
        print(f"API 调用失败: {e}")
        return None

if __name__ == '__main__':
    db_value = check_db_config()
    api_value = check_api_response()
    
    print("\n=== 结果汇总 ===")
    print(f"数据库配置值: {db_value}")
    print(f"API 返回值: {api_value}")
    
    if api_value == False:
        print("\n✅ 验证码已关闭 (captchaEnabled=false)")
    else:
        print("\n❌ 验证码未关闭，需要清理缓存并重启后端")
