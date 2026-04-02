# 【提示词 E0】环境配置核查与 GlobalRules 固化

> **状态**：待执行 | **预估工时**：15分钟 | **优先级：最高，先于 D1 执行**

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**系统运维工程师**，本次任务只有一件事：**把真实的服务配置找出来，写进 `.globalrules`**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（了解现有内容，避免重复追加）
2. `services/business-api/ruoyi-admin/src/main/resources/application.yml`
3. `services/business-api/ruoyi-admin/src/main/resources/application-druid.yml`
4. `services/ai-service/.env`（若不存在则读 `.env.example`）
5. `deploy/docker-compose.yml`

**【任务】**

读取上述配置文件，提取以下信息的**真实值**（不是占位符、不是默认值）：

| 服务 | 需要提取的内容 |
|------|--------------|
| PostgreSQL | host、port、database 名、username、password |
| Redis | host、port、password（如无密码请标注"无密码"） |
| AI 服务 | 监听端口、与 business-api 通信的内网地址 |
| business-api | 服务端口（通常 8080）、context-path（如有） |
| 前端代理目标 | 确认后端实际监听地址与端口 |

**【交付物】**

将以下格式的内容**直接追加到 `.globalrules` 文件末尾**（不要修改已有内容）：

```markdown
## ⚙️ 本地服务配置（真实值，禁止擅自修改）

> 此节由配置核查任务自动生成，如需修改配置请同步更新此处。

| 服务 | 配置项 | 值 |
|------|-------|-----|
| PostgreSQL | host | xxx |
| PostgreSQL | port | xxx |
| PostgreSQL | database | xxx |
| PostgreSQL | username | xxx |
| PostgreSQL | password | xxx |
| Redis | host | xxx |
| Redis | port | xxx |
| Redis | password | xxx（或：无密码） |
| business-api | 端口 | xxx |
| business-api | context-path | xxx（或：无） |
| ai-service | 端口 | xxx |
| Vite proxy target | business-api | http://localhost:xxxx |
```

**【禁止清单】**

- ❌ 禁止修改任何 yml / .env / 配置文件的内容
- ❌ 禁止修改 `.globalrules` 中已有的内容，只能追加到末尾
- ❌ 如果某个配置文件读不到（权限或文件不存在），标注"未找到"，不要猜测
- ❌ 不要尝试连接数据库或启动任何服务

**【完成标准】**

✅ `.globalrules` 末尾新增了服务配置表，所有字段均已填写（即使部分值为"未找到"）  
✅ 表格中没有占位符（如 `your_password`、`xxxxx` 等未替换的默认值）

满足以上标准后，请明确回复 **"配置核查完成"**，并在回复中把你写入的配置表内容再贴一遍供确认。
