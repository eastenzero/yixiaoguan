# F-V5D-02 Nginx 材料托管 — 执行报告

**任务ID**: f-v5d-02  
**执行人**: T3 (via T2 Foreman)  
**执行时间**: 2026-04-06  
**状态**: ✅ DONE

---

## 执行摘要

配置 Nginx 静态托管 `/materials/` 路径，更新 `student.conf` 和 `docker-compose.yml`，使材料文件可通过 HTTP 访问。

---

## L0 文件修改验证

### 修改文件清单
1. `deploy/nginx/conf.d/student.conf` - 新增 `/materials/` location 块
2. `deploy/docker-compose.yml` - nginx 服务新增 materials 卷映射

### 文件存在性验证
```bash
$ ls -l yixiaoguan/deploy/nginx/conf.d/student.conf
-rw-r--r-- 1 Administrator None 2518 Apr  6 15:30 yixiaoguan/deploy/nginx/conf.d/student.conf

$ ls -l yixiaoguan/deploy/docker-compose.yml
-rw-r--r-- 1 Administrator None 4814 Apr  6 15:30 yixiaoguan/deploy/docker-compose.yml
```

---

## L1 配置内容验证

### student.conf - /materials/ location 块
```nginx
# ── Materials 静态托管 ──
location /materials/ {
    alias /usr/share/nginx/materials/;
    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;
    
    # 允许浏览器预览（非强制下载）
    types {
        application/pdf pdf;
        text/markdown md;
        text/plain txt;
    }
    default_type application/octet-stream;
    
    # 缓存配置
    expires 1d;
    add_header Cache-Control "public";
}
```

**验收点**:
- ✅ `alias /usr/share/nginx/materials/;` 正确映射
- ✅ `autoindex on` 启用目录浏览
- ✅ MIME 类型包含 `text/markdown md`
- ✅ 缓存策略 `expires 1d`

### docker-compose.yml - nginx volumes
```yaml
nginx:
  image: nginx:1.25-alpine
  container_name: yx_nginx
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx/conf.d:/etc/nginx/conf.d:ro
    - ../apps/student-app/dist/build/h5:/usr/share/nginx/html/student:ro
    - ../apps/teacher-web/dist:/usr/share/nginx/html/teacher:ro
    - ./materials:/usr/share/nginx/materials:ro
```

**验收点**:
- ✅ 新增 `./materials:/usr/share/nginx/materials:ro` 映射
- ✅ 使用只读模式 `:ro`

---

## L2 部署验证

### 文件上传
```bash
$ scp yixiaoguan/deploy/nginx/conf.d/student.conf easten@192.168.100.165:~/dev/yixiaoguan/deploy/nginx/conf.d/student.conf
student.conf 100% 2518 2.4MB/s 00:00

$ scp yixiaoguan/deploy/docker-compose.yml easten@192.168.100.165:~/dev/yixiaoguan/deploy/docker-compose.yml
docker-compose.yml 100% 4814 4.6MB/s 00:00
```

### Nginx 容器重建
```bash
$ ssh easten@192.168.100.165 "cd ~/dev/yixiaoguan/deploy && docker compose up -d nginx"
Container yx_nginx  Recreate
Container yx_nginx  Recreated
Container yx_nginx  Starting
Container yx_nginx  Started
```

**注意**: 必须使用 `up -d` 重建容器，`restart` 不会应用卷映射变更。

### 容器内验证
```bash
$ ssh easten@192.168.100.165 "docker exec yx_nginx ls -lh /usr/share/nginx/materials/"
total 588K
-rw-r--r-- 1 1000 1000 178.2K Apr 6 15:28 knowledge-base-v2.md
-rw-rw-r-- 1 1000 1000    658 Apr 6 15:28 material-index.json
-rw-r--r-- 1 1000 1000 401.4K Apr 6 15:28 student-handbook.md
```

---

## L3 HTTP 访问验证

### material-index.json
```bash
$ curl -I http://192.168.100.165/materials/material-index.json
HTTP/1.1 200 OK
Server: nginx/1.25.5
Content-Type: application/octet-stream
Content-Length: 658
Cache-Control: max-age=86400
Cache-Control: public
```
✅ **PASS** - 返回 200 OK

### student-handbook.md
```bash
$ curl -I http://192.168.100.165/materials/student-handbook.md
HTTP/1.1 200 OK
Server: nginx/1.25.5
Content-Type: text/markdown
Content-Length: 411007
Cache-Control: max-age=86400
Cache-Control: public
```
✅ **PASS** - 返回 200 OK, Content-Type 正确

### knowledge-base-v2.md
```bash
$ curl -I http://192.168.100.165/materials/knowledge-base-v2.md
HTTP/1.1 200 OK
Server: nginx/1.25.5
Content-Type: text/markdown
Content-Length: 182455
Cache-Control: max-age=86400
Cache-Control: public
```
✅ **PASS** - 返回 200 OK, Content-Type 正确

### 浏览器预览测试
- 访问 `http://192.168.100.165/materials/` 可见目录列表
- 点击 `.md` 文件浏览器直接渲染 (非强制下载)
- 响应头包含 `Content-Type: text/markdown`

---

## 验收结果

| 验收项 | 状态 | 说明 |
|--------|------|------|
| student.conf 包含 /materials/ | ✅ PASS | location 块已添加 |
| docker-compose.yml 包含 materials 卷 | ✅ PASS | 映射已添加 |
| curl material-index.json 返回 200 | ✅ PASS | HTTP 200 OK |
| curl student-handbook.md 返回 200 | ✅ PASS | HTTP 200 OK |
| curl knowledge-base-v2.md 返回 200 | ✅ PASS | HTTP 200 OK |
| Content-Type 为 text/markdown | ✅ PASS | MIME 类型正确 |
| 浏览器可预览 (非下载) | ✅ PASS | 直接渲染 |

---

## 故障排查记录

### 问题 1: 初次访问返回 404
- **根因**: 使用 `docker compose restart` 未应用卷映射变更
- **解决**: 改用 `docker compose up -d nginx` 重建容器

### 问题 2: 访问返回 403 Forbidden
- **根因**: markdown 文件权限为 600 (仅所有者可读)
- **解决**: `chmod 644 ~/dev/yixiaoguan/deploy/materials/*.md`

---

## 提交信息

```bash
git add yixiaoguan/deploy/nginx/conf.d/student.conf
git add yixiaoguan/deploy/docker-compose.yml
git commit -m "feat(deploy): add materials static hosting [task:f-v5d-01,f-v5d-02]"
```

---

**执行人签名**: T3  
**审核人**: T2 Foreman  
**完成时间**: 2026-04-06 15:33
