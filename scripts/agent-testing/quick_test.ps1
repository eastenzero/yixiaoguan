# 医小管系统 - Agent 精简验证脚本
# 使用方式：先人工登录获取 auth_state.json，然后运行此脚本

param(
    [string]$AuthState = "./auth_state.json",
    [string]$BaseUrl = "http://localhost:5173"
)

# 检查认证状态文件
if (-not (Test-Path $AuthState)) {
    Write-Host "❌ 认证状态文件不存在: $AuthState" -ForegroundColor Red
    Write-Host "请先按照 AUTH_GUIDE.md 准备认证状态" -ForegroundColor Yellow
    exit 1
}

Write-Host "=== 医小管系统 Agent 精简验证 ===" -ForegroundColor Cyan
Write-Host "认证状态: $AuthState"
Write-Host "目标地址: $BaseUrl"
Write-Host ""

# 测试 1：基础登录验证
Write-Host "[测试 1/5] 登录状态验证..." -ForegroundColor Green
agent-browser --session test_agent --state $AuthState open "$BaseUrl/dashboard"
$url = agent-browser --session test_agent get url
if ($url -like "*/dashboard*") {
    Write-Host "✅ 登录成功，已跳转至仪表盘" -ForegroundColor Green
} else {
    Write-Host "❌ 登录失败，当前URL: $url" -ForegroundColor Red
}
Write-Host ""

# 测试 2：学生提问页面
Write-Host "[测试 2/5] 学生提问页面加载..." -ForegroundColor Green
agent-browser --session test_agent open "$BaseUrl/questions"
Start-Sleep -Milliseconds 2000
$snapshot = agent-browser --session test_agent snapshot -i
if ($snapshot -like "*待解决*" -or $snapshot -like "*提问*") {
    Write-Host "✅ 提问页面加载成功" -ForegroundColor Green
} else {
    Write-Host "⚠️ 页面内容异常，请检查截图" -ForegroundColor Yellow
}
agent-browser --session test_agent screenshot --full ./test_questions.png
Write-Host "截图保存: test_questions.png"
Write-Host ""

# 测试 3：空教室审批页面
Write-Host "[测试 3/5] 空教室审批页面加载..." -ForegroundColor Green
agent-browser --session test_agent open "$BaseUrl/approval"
Start-Sleep -Milliseconds 2000
$snapshot = agent-browser --session test_agent snapshot -i
if ($snapshot -like "*待审批*" -or $snapshot -like "*审批*") {
    Write-Host "✅ 审批页面加载成功" -ForegroundColor Green
} else {
    Write-Host "⚠️ 页面内容异常，请检查截图" -ForegroundColor Yellow
}
agent-browser --session test_agent screenshot --full ./test_approval.png
Write-Host "截图保存: test_approval.png"
Write-Host ""

# 测试 4：知识库页面
Write-Host "[测试 4/5] 知识库页面加载..." -ForegroundColor Green
agent-browser --session test_agent open "$BaseUrl/knowledge"
Start-Sleep -Milliseconds 2000
$snapshot = agent-browser --session test_agent snapshot -i
if ($snapshot -like "*知识库*" -or $snapshot -like "*知识条目*") {
    Write-Host "✅ 知识库页面加载成功" -ForegroundColor Green
} else {
    Write-Host "⚠️ 页面内容异常，请检查截图" -ForegroundColor Yellow
}
agent-browser --session test_agent screenshot --full ./test_knowledge.png
Write-Host "截图保存: test_knowledge.png"
Write-Host ""

# 测试 5：仪表盘统计
Write-Host "[测试 5/5] 仪表盘统计加载..." -ForegroundColor Green
agent-browser --session test_agent open "$BaseUrl/dashboard"
Start-Sleep -Milliseconds 2000
agent-browser --session test_agent screenshot --full ./test_dashboard.png
Write-Host "截图保存: test_dashboard.png"
Write-Host ""

# 清理
agent-browser --session test_agent close

Write-Host "=== 精简验证完成 ===" -ForegroundColor Cyan
Write-Host "请检查以下截图文件：" -ForegroundColor Yellow
Write-Host "  - test_questions.png"
Write-Host "  - test_approval.png"
Write-Host "  - test_knowledge.png"
Write-Host "  - test_dashboard.png"
