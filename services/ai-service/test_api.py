#!/usr/bin/env python3
"""
测试 AI 服务的 RAG API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("1. 测试健康检查")
    print("=" * 60)
    
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        data = resp.json()
        print(f"状态: {data.get('status')}")
        chroma = data.get('components', {}).get('chromadb', {})
        print(f"ChromaDB 状态: {chroma.get('status')}")
        details = chroma.get('details', {})
        print(f"条目数: {details.get('entry_count', 'N/A')}")
        print(f"集合: {details.get('collection_name', 'N/A')}")
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_kb_search():
    """测试知识库搜索"""
    print("\n" + "=" * 60)
    print("2. 测试知识库搜索 API")
    print("=" * 60)
    
    test_queries = [
        "如何申请国家奖学金",
        "学籍注册流程",
        "助学金申请条件",
    ]
    
    for query in test_queries:
        print(f"\n查询: '{query}'")
        try:
            resp = requests.post(
                f"{BASE_URL}/kb/search",
                json={"query": query, "top_k": 3},
                timeout=10
            )
            data = resp.json()
            if data.get('code') == 200:
                results = data.get('data', [])
                print(f"  命中 {len(results)} 条:")
                for i, item in enumerate(results, 1):
                    print(f"    {i}. [{item.get('score', 0):.4f}] {item.get('title', '未知')[:40]}")
            else:
                print(f"  ❌ API 错误: {data.get('msg')}")
        except Exception as e:
            print(f"  ❌ 错误: {e}")

def test_chat():
    """测试 RAG 对话"""
    print("\n" + "=" * 60)
    print("3. 测试 RAG 对话 API")
    print("=" * 60)
    
    query = "国家奖学金的申请条件是什么？"
    print(f"\n用户问题: '{query}'")
    print("(使用知识库增强)...")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "query": query,
                "history": [],
                "use_kb": True,
                "top_k": 5
            },
            timeout=30
        )
        data = resp.json()
        if data.get('code') == 0:
            answer = data.get('data', {}).get('answer', '')
            sources = data.get('data', {}).get('sources', [])
            
            print(f"\n🤖 AI 回答:\n{'-' * 60}")
            print(answer[:500] + "..." if len(answer) > 500 else answer)
            print('-' * 60)
            
            print(f"\n📚 引用来源 ({len(sources)} 条):")
            for i, src in enumerate(sources[:3], 1):
                print(f"  {i}. [{src.get('score', 0):.4f}] {src.get('title', '未知')}")
        else:
            print(f"❌ API 错误: {data.get('msg')}")
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_chat_stream():
    """测试流式对话"""
    print("\n" + "=" * 60)
    print("4. 测试流式 RAG 对话 API")
    print("=" * 60)
    
    query = "请介绍一下奖学金申请流程"
    print(f"\n用户问题: '{query}'")
    print("(流式响应)...\n")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/chat/stream",
            json={
                "query": query,
                "history": [],
                "use_kb": True
            },
            stream=True,
            timeout=30
        )
        
        full_text = []
        sources_shown = False
        
        for line in resp.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        chunk = data.get('chunk', '')
                        sources = data.get('sources', [])
                        is_end = data.get('is_end', False)
                        error = data.get('error', '')
                        
                        if error:
                            print(f"\n❌ 流式错误: {error}")
                            break
                        
                        if chunk:
                            print(chunk, end='', flush=True)
                            full_text.append(chunk)
                        
                        if sources and not sources_shown:
                            print(f"\n\n[知识来源: {len(sources)} 条]")
                            sources_shown = True
                        
                        if is_end:
                            print("\n")
                            break
                    except json.JSONDecodeError:
                        pass
        
        print(f"\n✅ 流式接收完成，总长度: {len(''.join(full_text))} 字符")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 医小管 AI 服务 - 端到端测试")
    print("=" * 60)
    
    test_health()
    test_kb_search()
    test_chat()
    # test_chat_stream()  # 流式测试可能较长，可选
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
