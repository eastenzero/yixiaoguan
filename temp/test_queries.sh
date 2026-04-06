#!/bin/bash

# Test 1: 电费
echo "=== Test 1: 电费 ==="
curl -s -X POST http://localhost:8001/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "怎么交电费", "top_k": 3}'
echo ""
echo ""

# Test 2: 报修
echo "=== Test 2: 报修 ==="
curl -s -X POST http://localhost:8001/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "东西坏了怎么报修", "top_k": 3}'
echo ""
echo ""

# Test 3: 校园卡
echo "=== Test 3: 校园卡 ==="
curl -s -X POST http://localhost:8001/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "校园卡怎么办理", "top_k": 3}'
echo ""
echo ""

# Test 4: 奖学金
echo "=== Test 4: 奖学金 ==="
curl -s -X POST http://localhost:8001/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "怎么申请奖学金", "top_k": 3}'
echo ""
echo ""

# Test 5: 请假
echo "=== Test 5: 请假 ==="
curl -s -X POST http://localhost:8001/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "请假流程是什么", "top_k": 3}'
echo ""
