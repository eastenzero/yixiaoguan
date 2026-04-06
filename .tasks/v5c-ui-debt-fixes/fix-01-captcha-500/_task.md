---
id: "fix-01"
parent: "v5c-ui-debt-fixes"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "services/business-api/Dockerfile"
  - "deploy/docker-compose.yml"
out_of_scope:
  - "services/business-api/ruoyi-admin/src/"
  - "apps/**"
  - "services/ai-service/**"

context_files:
  - ".teb/antipatterns.md"
  - "deploy/docker-compose.yml"

done_criteria:
  L0: "services/business-api/Dockerfile 存在"
  L1: "curl -s http://192.168.100.165:8080/captchaImage | python3 -c \"import sys,json; d=json.load(sys.stdin); print('PASS' if 'img' in d else 'FAIL')\""
  L2: "curl -s http://192.168.100.165:8080/captchaImage 返回 200，响应含 img 和 uuid 字段"
  L3: "访问 http://192.168.100.165:5174 登录页可见验证码图片；输入正确验证码可登录"

root_cause: |
  Alpine 镜像缺少字体文件，kaptcha 生成验证码图片时无可用字体，抛出 500。
  修复方向：Dockerfile 中加 RUN apk add --no-cache ttf-dejavu

reproduction_steps:
  - "确认 Redis captchaEnabled=true"
  - "GET http://192.168.100.165:8080/captchaImage → 500"
  - "docker compose logs business-api | grep -i 'captcha\\|font\\|kaptcha' 查看具体错误"

created_at: "2026-04-06"
---

# FIX-01: captchaImage 接口 500 修复

> GET /captchaImage 返回 200 并携带 Base64 图片，登录页验证码正常显示。

## 背景

DEBT-V5A-02：启用验证码后 /captchaImage 返回 500。推测为 Alpine 容器缺少字体文件。

## 执行步骤

1. **查日志确认根因**：
   ```bash
   ssh easten@192.168.100.165 "cd ~/dev/yixiaoguan && docker compose logs business-api 2>&1 | grep -i 'font\|kaptcha\|captcha' | tail -20"
   ```

2. **若是字体问题**，修改 `services/business-api/Dockerfile`，加入：
   ```dockerfile
   RUN apk add --no-cache ttf-dejavu
   ```

3. **重建并重启**：
   ```bash
   ssh easten@192.168.100.165 "cd ~/dev/yixiaoguan/deploy && docker compose build business-api && docker compose up -d business-api"
   ```

4. **启用验证码**：
   ```bash
   ssh easten@192.168.100.165 "docker exec yx_redis redis-cli -a 'Yx@Redis2026!' SET sys_config:sys.account.captchaEnabled true"
   ```

5. **验证**：
   ```bash
   curl -s http://192.168.100.165:8080/captchaImage | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS' if 'img' in d else 'FAIL')"
   ```

## 已知陷阱

- Alpine 镜像常见字体缺失问题，`ttf-dejavu` 是标准修复方案
- 若日志显示其他根因（如 kaptcha Bean 未注入），则检查 `CaptchaConfig.java` 是否存在
- Docker 重建时间约 2-5 分钟，注意等待 healthy 状态
