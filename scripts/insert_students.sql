-- yx_role 角色初始化
-- 生成时间: 2026-04-05 23:52:09

-- 清空旧角色数据（谨慎使用，生产环境建议注释）
-- TRUNCATE TABLE yx_user_role CASCADE;
-- TRUNCATE TABLE yx_role CASCADE;

INSERT INTO yx_role (id, role_key, role_name, sort_order, status, remark) VALUES
  (1, 'admin', '管理员', 1, 1, '系统初始化角色'),
  (2, 'student', '学生', 2, 1, '系统初始化角色'),
  (3, 'teacher', '教师', 3, 1, '系统初始化角色');

-- 学生数据插入脚本
-- 生成时间: 2026-04-05 23:52:09
-- 学生数量: 5
-- 注意：密码已使用 BCrypt 预哈希（$2a$ 开头）

-- 插入学生用户
INSERT INTO yx_user (username, password, real_name, nickname, student_id, department, major, grade, class_name, status, is_deleted, created_at, updated_at) VALUES
  ('2524010001', E'$2a$10$bjrasC00CuWuOWqNKS7P7.ra1XxsV6t/Y/MCZBfgOSIicMfEu7YdS', '张小洋', '张小洋', '2524010001', '放射学院', '医学影像学', '2024级', '影像1班', 1, FALSE, NOW(), NOW()),
  ('2021010002', E'$2a$10$OPKfM7XNtjZsp6gZegcSb.jaEPhl9X0bxkuFaJmUstWslYJMfltaS', '李小辉', '李小辉', '2021010002', '放射学院', '医学影像学', '2024级', '影像1班', 1, FALSE, NOW(), NOW()),
  ('2024010103', E'$2a$10$ctffdvpH/IwiD4ctpDm0K.oO3.kZ68Ux9AlTmILWJgk.BtnInT7Om', '王伟', '王伟', '2024010103', '临床与基础医学院（基础医学研究所）', '临床医学', '2024级', '临床1班', 1, FALSE, NOW(), NOW()),
  ('2024410004', E'$2a$10$NqV4vtk1VizZKi6.ebPFce4p.3uBW4Eq6jGjVWXLRINmZnlcxZOKy', '刘芳', '刘芳', '2024410004', '药学院（药物研究所）', '药学', '2024级', '药学1班', 1, FALSE, NOW(), NOW()),
  ('2024010003', E'$2a$10$uTy.mV3gnHPPLxFRDPpMw.57IhMdB5z/f8CvBoGKP0gu69Uuzh1fG', '陈静', '陈静', '2024010003', '护理学院', '护理学', '2024级', '护理1班', 1, FALSE, NOW(), NOW());

-- 关联学生角色 (role_id = 2)
-- 注意：关联 student_id 不为空的用户（学生）
INSERT INTO yx_user_role (user_id, role_id, created_at, updated_at)
SELECT id, 2, NOW(), NOW() FROM yx_user WHERE student_id IS NOT NULL AND student_id != ''
ON CONFLICT (user_id, role_id) DO NOTHING;