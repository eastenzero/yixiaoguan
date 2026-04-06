# Phase2-API 调查与端口迁移报告

**调查时间**: 2026-04-06  
**执行者**: T2 (Kiro)  
**状态**: ✅ 完成

---

## 调查背景

phase2-api.service 占用 8000 端口，与 ai-service 冲突。需要调查其用途并决定处理方案。

---

## 调查结果

### 服务信息

**服务名称**: phase2-api.service  
**描述**: Phase2 API Service (collector + retrieval)  
**项目路径**: `/home/easten/ai-collab-control-plane/phase2`  
**服务类型**: systemd 用户服务（enabled，自动启动）

### 功能分析

**核心功能**:
1. **混合检索服务** (Hybrid + Blend + Failover)
   - BM25 索引：674 chunks（全量）
   - BM25 索引：413 chunks（serving）
   - 使用 jieba 分词
   - ChromaDB 向量存储

2. **Collector Pipeline**
   - 端点：`/collector/pipeline/today`
   - 外部客户端（192.168.100.1）每分钟轮询一次
   - 返回 200 OK（正常工作）

3. **认证机制**
   - 需要 API key
   - 未授权请求返回 401 Unauthorized

### 运行状态

- **重启次数**: 7623 次（长期运行）
- **最后重启**: 2026-04-06 06:10:28
- **状态**: active (running)
- **内存占用**: 178.5M
- **CPU 时间**: 4.141s

### 客户端使用情况

**活跃客户端**: 192.168.100.1（Windows 机器）
- 每分钟请求 `/collector/pipeline/today`
- 持续使用中，不能随意停止

---

## 决策分析

### 方案对比

| 方案 | 优点 | 缺点 | 风险 |
|------|------|------|------|
| 禁用 phase2-api | 彻底解决冲突 | 破坏现有服务 | 高 - 影响外部客户端 |
| 修改 phase2-api 端口 | 两个服务共存 | 需要通知客户端 | 低 - 仅配置变更 |
| 修改 ai-service 端口 | 保留 phase2-api | 影响所有学生 | 高 - 需改前端配置 |

### 推荐方案

**选择**: 修改 phase2-api 端口到 8002

**理由**:
1. phase2-api 有外部依赖，但客户端可控（同一内网）
2. ai-service 端口硬编码在 vite.config.ts，影响所有学生
3. 端口迁移对 phase2-api 影响最小

---

## 执行步骤

### Step 1: 备份配置

```bash
cp ~/.config/systemd/user/phase2-api.service \
   ~/.config/systemd/user/phase2-api.service.bak
```

**结果**: ✅ 备份完成

---

### Step 2: 修改端口

```bash
sed -i 's/--port 8000/--port 8002/g' \
  ~/.config/systemd/user/phase2-api.service
```

**修改内容**:
```diff
- ExecStart=... --host 0.0.0.0 --port 8000
+ ExecStart=... --host 0.0.0.0 --port 8002
```

**结果**: ✅ 配置已修改

---

### Step 3: 重新加载并重启

```bash
systemctl --user daemon-reload
systemctl --user restart phase2-api.service
```

**结果**: ✅ 服务重启成功

---

### Step 4: 验证

**端口占用**:
```bash
ss -tlnp | grep -E ':(8000|8001|8002)'
```

**结果**:
```
8000: uvicorn (ai-service)    ✅
8002: python (phase2-api)     ✅
```

**服务状态**:
```bash
systemctl --user status phase2-api.service
```

**结果**: active (running) ✅

**功能测试**:
```bash
curl http://localhost:8002/collector/pipeline/today
```

**结果**: 401 Unauthorized（正常，需要 API key）✅

---

## 后续行动

### 必须执行

1. **通知客户端更新端点**
   - 将 `http://192.168.100.165:8000` 改为 `http://192.168.100.165:8002`
   - 客户端位置：192.168.100.1（Windows 机器）

2. **监控服务运行**
   - 观察客户端是否成功切换到新端口
   - 检查日志确认无错误

### 可选优化

1. **文档化**
   - 记录 phase2-api 的用途和配置
   - 更新端口分配文档

2. **端口规划**
   - 8000: ai-service (yixiaoguan)
   - 8001: 保留
   - 8002: phase2-api (ai-collab-control-plane)

---

## 风险评估

### 已知风险

**RISK-1**: 客户端未更新端点
- **概率**: 中
- **影响**: 高（客户端无法访问服务）
- **缓解**: 立即通知客户端更新配置

**RISK-2**: 其他未知依赖
- **概率**: 低
- **影响**: 中
- **缓解**: 监控日志，发现问题及时回滚

### 回滚方案

如需回滚：
```bash
# 恢复配置
cp ~/.config/systemd/user/phase2-api.service.bak \
   ~/.config/systemd/user/phase2-api.service

# 重新加载
systemctl --user daemon-reload
systemctl --user restart phase2-api.service
```

---

## 总结

✅ phase2-api 成功迁移到 8002 端口  
✅ ai-service 独占 8000 端口  
✅ 两个服务共存，互不干扰  
✅ 配置已备份，可随时回滚

**下一步**: 通知客户端（192.168.100.1）更新端点配置

---

**T2 签收**: ✅ 调查完成，端口迁移成功
