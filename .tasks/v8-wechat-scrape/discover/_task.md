# DISCOVER — 公众号 fakeid 确认与清单完善

**所属**: v8-wechat-scrape / PHASE 2
**优先级**: P0
**执行者**: Kimi
**预估工时**: 1h
**依赖**: LOGIN (auth-key 已获取)

## 任务目标

1. 对学生提供的 25 个已知公众号，通过 API 搜索确认 fakeid
2. 通过关键词 API 搜索，发现可能遗漏的学校相关公众号
3. 更新 `kimi/wechat-accounts-list.md`，填入所有 fakeid

## 执行步骤

### Step 1: 确认 API 可用
```
curl.exe -s -H "X-Auth-Key: {auth-key}" http://localhost:3000/api/public/v1/authkey
```
期望 `code: 0`。

### Step 2: 搜索确认 25 个已知账号的 fakeid

对每个账号按名称搜索：
```
curl.exe -s -H "X-Auth-Key: {auth-key}" "http://localhost:3000/api/public/v1/account?keyword=教务部"
curl.exe -s -H "X-Auth-Key: {auth-key}" "http://localhost:3000/api/public/v1/account?keyword=研究生处"
# ... 依此类推，覆盖 25 个账号
```

找到匹配项后记录 fakeid（`nickname` 字段匹配时取 `fakeid` 字段值）。

### Step 3: 补充搜索可能遗漏的账号
```
curl.exe -s -H "X-Auth-Key: {auth-key}" "http://localhost:3000/api/public/v1/account?keyword=山东第一医科大学"
curl.exe -s -H "X-Auth-Key: {auth-key}" "http://localhost:3000/api/public/v1/account?keyword=山一大"
curl.exe -s -H "X-Auth-Key: {auth-key}" "http://localhost:3000/api/public/v1/account?keyword=山东省医学科学院"
```

对新发现的账号判断 KB 价值，加入清单。

## 输出

更新 `kimi/wechat-accounts-list.md`：
- A/B 类所有账号填入 fakeid
- C 类账号尽量填入 fakeid
- 新发现的账号追加到对应分类

## 验收标准

- AC-DIS-01: A 类 8 个账号 fakeid 全部确认
- AC-DIS-02: B 类 8 个账号 fakeid 尽量确认（≥5 个）
- AC-DIS-03: 补充搜索完成，新账号已追加分类
