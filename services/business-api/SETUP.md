# business-api 初始化步骤（若依 RuoYi-Vue3 裁剪指南）

> **说明**：若依需要从官方 GitHub 手动下载并裁剪，步骤较复杂，本文件仅记录操作步骤，不自动执行。  
> 开发者按以下步骤手动操作即可。

---

## 一、环境准备

| 依赖 | 版本要求 | 验证命令 |
|---|---|---| 
| JDK | 21+ | `java -version` |
| Maven | 3.9+ | `mvn -version` |
| PostgreSQL | 16+（运行中） | `docker compose up -d postgres` |
| Redis | 7+（运行中） | `docker compose up -d redis` |
| Node.js | 18+（用于生成代码） | `node -v` |

---

## 二、下载若依源码

```bash
# 克隆官方 RuoYi-Vue3 仓库（后端部分）
git clone https://github.com/yangzongzhuan/RuoYi-Vue3.git ruoyi-source

# 本次仅需后端，前端 ruoyi-ui/ 目录可忽略
```

> 若 GitHub 访问慢，可用 Gitee 镜像：
> ```bash
> git clone https://gitee.com/y_project/RuoYi-Vue3.git ruoyi-source
> ```

---

## 三、将源码复制进项目

```bash
# 将若依后端模块复制到 services/business-api/
cp -r ruoyi-source/ruoyi-admin     services/business-api/ruoyi-admin
cp -r ruoyi-source/ruoyi-common    services/business-api/ruoyi-common
cp -r ruoyi-source/ruoyi-framework services/business-api/ruoyi-framework
cp -r ruoyi-source/ruoyi-generator services/business-api/ruoyi-generator
cp -r ruoyi-source/ruoyi-quartz    services/business-api/ruoyi-quartz
cp -r ruoyi-source/ruoyi-system    services/business-api/ruoyi-system
cp    ruoyi-source/pom.xml         services/business-api/pom.xml
```

---

## 四、适配 PostgreSQL（若依默认 MySQL）

### 4.1 修改 pom.xml — 替换数据库驱动

```xml
<!-- 删除 MySQL 依赖 -->
<!-- <dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency> -->

<!-- 添加 PostgreSQL 驱动 -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

### 4.2 修改 application-druid.yml — 数据源配置

```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    druid:
      master:
        url: jdbc:postgresql://localhost:5432/yixiaoguan
        username: yx_admin
        password: ${POSTGRES_PASSWORD}
        driver-class-name: org.postgresql.Driver
```

### 4.3 修改 application.yml — 关闭 schema 自动建表

```yaml
mybatis:
  configuration:
    # PostgreSQL 不需要 MySQL 的 map-underscore-to-camel-case 之外的特殊配置
    map-underscore-to-camel-case: true
```

---

## 五、初始化数据库

### 5.1 创建数据库

```sql
-- 在 PostgreSQL 中执行
CREATE DATABASE yixiaoguan ENCODING 'UTF8';
```

### 5.2 导入若依基础表（MySQL → PostgreSQL 转换）

若依官方 SQL 文件位于 `ruoyi-source/sql/`，默认为 MySQL 语法，需转换：

- 工具推荐：[pgloader](https://pgloader.io/) 或手动改写
- 需要修改的主要差异：
  - `AUTO_INCREMENT` → `BIGSERIAL`
  - `` ` `` 反引号 → `"` 双引号（或直接去掉）
  - `TINYINT` → `SMALLINT`
  - `DATETIME` → `TIMESTAMP WITH TIME ZONE`
  - `BIT(1)` → `BOOLEAN`

> **医小管说明**：一期业务表（22 张 `yx_` 前缀表）的完整 DDL 在 
> `docs/database/schema-phase1.md`，需单独手写 PostgreSQL 语法的建表 SQL。

### 5.3 执行建表脚本

```bash
psql -h localhost -U yx_admin -d yixiaoguan -f sql/ruoyi_pg.sql
psql -h localhost -U yx_admin -d yixiaoguan -f sql/yx_schema.sql
```

---

## 六、一期保留模块清单

若依默认包含较多功能模块，一期只保留以下内容，其余可保留但不启用：

| 模块 | 保留 | 说明 |
|---|---|---|
| ruoyi-common | ✅ | 公共工具类，必须保留 |
| ruoyi-framework | ✅ | Spring Security + JWT，必须保留 |
| ruoyi-system | ✅ | 用户/角色/菜单管理，保留 |
| ruoyi-admin | ✅ | 启动入口，必须保留 |
| ruoyi-generator | ⚠️ 可选 | 代码生成器，开发期间保留，上线前可移除 |
| ruoyi-quartz | ❌ 暂不启用 | 定时任务，一期不需要 |

---

## 七、新增医小管业务模块

在 `ruoyi-admin/src/main/java/com/yixiaoguan/` 下创建以下包（开发阶段逐步添加）：

```
com.yixiaoguan
├── conversation/     # 问答会话模块
├── knowledge/        # 知识库模块
├── application/      # 申请审批模块
├── notification/     # 通知消息模块
├── ai/               # AI 服务代理（HTTP 调用 ai-service）
└── websocket/        # WebSocket 服务（教师实时介入）
```

---

## 八、本地启动

```bash
cd services/business-api

# 编译
mvn clean package -DskipTests

# 启动（开发模式）
java -jar ruoyi-admin/target/ruoyi-admin.jar \
  --spring.profiles.active=dev \
  --POSTGRES_PASSWORD=your_password \
  --REDIS_PASSWORD=your_redis_password
```

服务启动后访问：`http://localhost:8080`

---

## 九、参考文档

- 若依官方文档：https://doc.ruoyi.vip/
- 医小管 API 设计：`docs/api/business-api-spec.md`
- 若依开发约定：`docs/dev-guides/ruoyi-guide.md`
- 本地环境搭建：`docs/dev-guides/local-setup.md`
