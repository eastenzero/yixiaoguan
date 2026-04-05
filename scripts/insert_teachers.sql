-- 教师（辅导员）数据插入脚本
-- 生成时间: 2026-04-05 23:52:09
-- 教师数量: 4
-- 注意：密码已使用 BCrypt 预哈希（$2a$ 开头）

-- 插入教师用户
INSERT INTO yx_user (username, password, real_name, nickname, employee_id, department, grade, status, is_deleted, created_at, updated_at) VALUES
  ('liang_s_huli_24', E'$2a$10$eXoOu3iVhGpZLqpZlPZ/7.ett35nKD2l76/7JcL5.v3we9e4JXYnq', '梁淑芬', '梁淑芬', 'T0001', '护理学院', '2024级', 1, FALSE, NOW(), NOW()),
  ('xie_s_yaoxue_24', E'$2a$10$imvtwg5ce1/opOcTHi144OPG2xAtqPgGpm2FtjNCOeLyoF54PMOz.', '谢淑华', '谢淑华', 'T0002', '药学院（药物研究所）', '2024级', 1, FALSE, NOW(), NOW()),
  ('deng_p_linchuang_24', E'$2a$10$XSJfuQCuUsjcw79v54XS0.9yHoPkrK6qIw1RwJ4bElasjPcX.Iv8G', '邓平', '邓平', 'T0003', '临床与基础医学院（基础医学研究所）', '2024级', 1, FALSE, NOW(), NOW()),
  ('cheng_d_fangshe_24', E'$2a$10$L/B3XTNwd1w.skrnBHS6G.9mnsHWuUU0yjlBv.diA10x9ZvnirC0G', '程丹', '程丹', 'T0004', '放射学院', '2024级', 1, FALSE, NOW(), NOW());

-- 关联教师角色 (role_id = 3)
-- 注意：关联 employee_id 不为空的用户（教师）
INSERT INTO yx_user_role (user_id, role_id, created_at, updated_at)
SELECT id, 3, NOW(), NOW() FROM yx_user WHERE employee_id IS NOT NULL AND employee_id != '' AND student_id IS NULL
ON CONFLICT (user_id, role_id) DO NOTHING;