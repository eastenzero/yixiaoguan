import sys
import re

def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    # 去掉反引号
    sql = sql.replace('`', '')
    
    # 转义单引号 (针对数据插入)
    # 但不要误伤建表时的默认值单引号。这里先暴力替换，然后把建表部分修复，或者使用更智能的方法。
    # 实际上只需要把 \' 替换为 '' 就可以解决转义问题
    sql = sql.replace(r"\'", "''")
    
    # 替换 auto_increment 
    sql = re.sub(r'(?i)(bigint|int)(?:\(\d+\))?.*?AUTO_INCREMENT', 'BIGSERIAL', sql)
    
    # 替换类型
    sql = re.sub(r'(?i)\btinyint(?:\(\d+\))?', 'SMALLINT', sql)
    sql = re.sub(r'(?i)\bint(?:\(\d+\))?', 'INT', sql)
    sql = re.sub(r'(?i)\bbigint(?:\(\d+\))?', 'BIGINT', sql)
    sql = re.sub(r'(?i)\bdatetime\b', 'TIMESTAMP', sql)
    sql = re.sub(r'(?i)\bbit\(1\)', 'BOOLEAN', sql)
    sql = re.sub(r'(?i)\bdouble(?:\(\d+,\d+\))?', 'DECIMAL(10,2)', sql)
    sql = re.sub(r'(?i)\blongblob\b', 'TEXT', sql)
    
    # 替换函数
    sql = re.sub(r'(?i)\bsysdate\(\)', 'CURRENT_TIMESTAMP', sql)
    
    # 清理 ENGINE=InnoDB 结尾
    sql = re.sub(r'(?im)\)\s*engine\s*=\s*innodb.*?;', ');', sql)
    
    # 清理字符集等
    sql = re.sub(r'(?i)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci\s*', '', sql)
    sql = re.sub(r'(?i)CHARACTER SET utf8mb4\s*', '', sql)
    sql = re.sub(r'(?i)COLLATE utf8mb4_unicode_ci\s*', '', sql)
    sql = re.sub(r'(?i)CHARACTER SET utf8\s*', '', sql)
    
    # 删除列级 COMMENT
    sql = re.sub(r"(?i)\s+COMMENT\s+'[^']*'", "", sql)
    
    # 移除 CREATE TABLE 中的 KEY 和 UNIQUE KEY
    lines = sql.split('\n')
    new_lines = []
    in_create = False
    for line in lines:
        if re.search(r'(?i)CREATE TABLE', line):
            in_create = True
            new_lines.append(line)
        elif in_create and re.match(r'^\s*\)\s*;', line):
            in_create = False
            if new_lines and new_lines[-1].strip().endswith(','):
                new_lines[-1] = new_lines[-1].rstrip()[:-1]
            new_lines.append(line)
        elif in_create:
            if re.search(r'(?i)^\s*(UNIQUE\s+)?KEY\s+', line):
                continue
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    sql = '\n'.join(new_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sql)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
