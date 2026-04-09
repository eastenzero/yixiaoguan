# 任务：信息化服务、图书馆与网络服务数据源探查

## 身份
你是一个数据侦察员，负责探查山东第一医科大学（sdfmu.edu.cn）信息化、图书馆、网络等公共服务的公开数据源。

## 目标
通过网络搜索，深入探查信息化和图书馆相关页面，找出所有可供"学生校园助手知识库"使用的原始数据。

## 探查范围

### 1. 网络与信息化中心
- URL: https://wcs.sdfmu.edu.cn/
- 搜索: site:wcs.sdfmu.edu.cn 校园网 OR WiFi OR VPN OR 网络 OR 上网
- 搜索: site:sdfmu.edu.cn 信息化 OR 网络服务 OR 邮箱 OR 正版软件
- 重点: 校园网使用指南、WiFi连接方法、VPN使用、邮箱开通、正版软件

### 2. 图书馆
- URL: http://202.194.232.127/index.html
- 搜索: site:sdfmu.edu.cn 图书馆 OR 借阅 OR 数据库 OR 电子资源
- 搜索: 山东第一医科大学 图书馆 开放时间 OR 借书 OR 读者服务
- 重点: 开馆时间、借阅规则、电子资源使用、自习室预约、数据库访问

### 3. 信息门户与统一认证
- URL: http://portal.sdfmu.edu.cn (校内)
- URL: http://vpnportal.sdfmu.edu.cn (校外)
- URL: https://sso.sdfmu.edu.cn/cas/login-normal.html (统一认证)
- 搜索: site:sdfmu.edu.cn 信息门户 OR 统一认证 OR 密码重置 OR 一站式

### 4. 教育在线平台
- URL: https://jwc.sdfmu.edu.cn/homepagenew/indexold.do
- 搜索: site:sdfmu.edu.cn 教育在线 OR 网课平台 OR 在线学习 OR 教学平台

### 5. 校园一卡通与信息化服务
- 搜索: site:sdfmu.edu.cn 一卡通 OR 校园卡 OR 充值 OR 消费
- 搜索: site:sdfmu.edu.cn 打印 OR 复印 OR 自助服务

### 6. 邮箱系统
- URL: https://metc.sdfmu.edu.cn/sddyykdxdzyjxt.htm
- 搜索: site:sdfmu.edu.cn 邮箱 OR 电子邮件 OR edu.cn邮箱

## 输出要求

请将探查结果写入文件 `kimi/report-4-it-library.md`，格式如下：

```markdown
# 信息化服务与图书馆数据源探查报告

## 探查时间
[当前时间]

## 发现的数据源

### [数据源编号] [数据源名称]
- **URL**: [具体页面URL]
- **数据类型**: [使用指南/操作手册/规章制度/通知公告/...]
- **内容摘要**: [100字以内描述该页面包含什么内容]
- **KB价值评级**: [高/中/低] — [简述为什么]
- **可提取内容**: [列出可以转化为知识库条目的具体信息点]

## 汇总统计
- 高价值数据源: X 个
- 中价值数据源: X 个
- 低价值数据源: X 个

## 特别发现
[任何值得注意的发现]
```

## 约束
- 只探查公开可访问的页面，不尝试登录任何系统
- 如果某页面无法访问，记录为"不可访问"并注明原因
- 优先记录对学生日常使用最有用的信息（上网、借书、打印等）
- 每个数据源必须给出具体 URL
