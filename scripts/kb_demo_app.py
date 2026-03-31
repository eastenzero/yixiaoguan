"""
医小管知识库 RAG 效果展示 Demo (Streamlit)
"""

import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import dashscope
from dashscope import TextEmbedding, Generation
import chromadb
import re

# ── 路径与配置 ────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SECRETS_ENV = ROOT / ".secrets" / ".env"
CHROMA_DIR = ROOT / "knowledge-base" / "raw" / "first-batch-processing" / "converted" / "chroma_db"
DRAFTS_DIR = ROOT / "knowledge-base" / "entries" / "first-batch-drafts"

load_dotenv(SECRETS_ENV)
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

if not dashscope.api_key:
    st.error("未找到 DASHSCOPE_API_KEY，请检查 .secrets/.env")
    st.stop()

EMBED_MODEL = "text-embedding-v3"
LLM_MODEL = "qwen-plus"
COLLECTION_NAME = "kb_first_batch"

# ── 页面设置 & 主题 ────────────────────────────────────────
st.set_page_config(
    page_title="医小管 Default UI",
    page_icon="👨‍⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 仅保留极简的样式清理（消除顶部空白，其余靠 config.toml 的暗黑模式）
st.markdown("""
<style>
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)


# ── 工具函数 初始化 ─────────────────────────────────────
@st.cache_resource
def get_chroma_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(COLLECTION_NAME)

try:
    collection = get_chroma_collection()
except Exception as e:
    st.error(f"无法连接到知识库，请确保已运行向量化脚本。错误：{e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "view_source" not in st.session_state:
    st.session_state.view_source = None

# ── 知识库检索与生成逻辑 ───────────────────────────────────
def build_prompt(query, docs, metas, ids):
    context_str = "\n\n---\n\n".join(
        [f"【参考资料 {i+1}】（来源条目ID：`{id_val}`，标题：《{meta['title']}》，分类：{meta['category']}，受众：{meta['audience']}）\n{doc}" 
         for i, (doc, meta, id_val) in enumerate(zip(docs, metas, ids))]
    )
    
    prompt = f"""你是一个名为“医小管”的校园事务智能助手。请基于以下提供的参考资料回答学生的问题。
要求：
1. 态度要温和、专业，符合高校辅导员或客服人员的身份。
2. 必须且只能依据提供的【参考资料】内容进行回答，不得凭空捏造。
3. 如果参考资料中没有相关信息，请直接回答“知识库中暂未收录相关信息，请咨询辅导员”，不可自行发挥。
4. 回答完毕后，请在回复末尾简洁、详细地附上信息来源（格式如：**信息来源**：《XXX通知》，具体来源条目ID：KB-XXXXXXX）。务必引出条目ID（如 `KB-20260324-0023`），以便用户在右侧比对源文本。
5. 回答格式清晰易读，使用 markdown 语法，对于流程项可以使用分点说明。

【参考资料】
{context_str}

【用户提问】
{query}
"""
    return prompt

def parse_markdown_entry(content):
    """稳健地剥离 YAML 并提取原文件与正文"""
    source_files = []
    m = re.search(r'^\s*---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if m:
        yaml_block = m.group(1)
        body_content = content[m.end():].strip()
        sf_matches = re.findall(r'-\s+"([^"]+)"', yaml_block)
        for sf in sf_matches:
            source_files.append(sf.strip())
        return source_files, body_content
    else:
        return [], content


# ── 主界面布局 ───────────────────────────────────────────
col_chat, col_empty, col_source = st.columns([6, 0.5, 4])

# ====== 右侧内容面板优先渲染以建立状态 ======
with col_source:
    st.markdown('<h3 style="margin-top:0;">📑 知识查阅面板</h3>', unsafe_allow_html=True)
    
    # 使用限制高度的固定窗口使其自带内部滚动，不把整个页面撑高
    with st.container(height=800, border=True):
        if not st.session_state.view_source:
            st.info("💡 提示：在左侧聊天问答后，点击回答下方的 **【📄 阅读原文】** 按钮，此处将展示业务条文的详细内容与真实抽取出处。")
            
        else:
            entry_id = st.session_state.view_source
            filepath = DRAFTS_DIR / f"{entry_id}.md"
            
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8-sig") as f:
                    content = f.read()
                
                source_files, body_content = parse_markdown_entry(content)

                st.markdown(f"**📖 当前查阅草稿**：`{entry_id}`")
                st.divider()
                
                raw_to_view = st.session_state.get("view_raw_file")
                if raw_to_view:
                    # ---- 阅读原文件(DOCX)模式 ----
                    raw_path = ROOT / raw_to_view
                    st.markdown(f"##### 👁️ DOCX/原生文档提取预览")
                    st.caption(f"路径：`{raw_path.name}`")
                    
                    if st.button("🔙 返回业务规范(Markdown)"):
                        st.session_state.pop("view_raw_file", None)
                        st.rerun()
                    
                    if raw_path.exists():
                        st.info("以下文本由系统从对应的原始业务 Word / PDF 中解包提取：")
                        if raw_path.suffix.lower() == ".docx":
                            try:
                                import docx
                                doc = docx.Document(raw_path)
                                full_text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                                st.text_area("📄 原文文本：", full_text, height=450)
                            except Exception as e:
                                st.error(f"提取 DOCX 失败：{e}")
                        elif raw_path.suffix.lower() in [".md", ".txt"]:
                            with open(raw_path, "r", encoding="utf-8-sig") as rf:
                                st.text_area("📄 原文内容：", rf.read(), height=450)
                        else:
                            st.warning(f"暂不支持在 WEB 预览此格式文件 ({raw_path.suffix})。")
                    else:
                        st.error(f"找不到原始文件：\n`{raw_path}`")
                
                else:
                    # ---- 阅读已清洗知识(Markdown)模式 ----
                    if source_files:
                        cols = st.columns(len(source_files))
                        for idx, sf in enumerate(source_files):
                            if cols[idx].button(f"📥 查阅真实源文件 {idx+1}"):
                                st.session_state.view_raw_file = sf
                                st.rerun()
                    else:
                        st.caption("⚠️ 本条目无来源文件信息。")

                    st.markdown("---")
                    st.markdown(body_content)
                    
            else:
                st.error(f"由于文件丢失，未找到归档文件：{filepath}")


# ====== 左侧对话面板 ======
with col_chat:
    st.markdown('<h2 style="margin-top:0;">👨‍⚕️ 医小管 Demo</h2>', unsafe_allow_html=True)
    st.caption("基于 Qwen-Plus + ChromaDB · 本地 60 条最新规则")
    
    # 对话列表使用独立带滚动的容器
    chat_container = st.container(height=650, border=False)
    
    with chat_container:
        # 初始推荐问题
        if len(st.session_state.messages) == 0:
            st.info("💡 **推荐测试的问题（输入框点击发送）：**")
            st.code("新生入学资格审查和录取复查登记表去哪交？\n我大一，请问体质健康测试如果是骨折了可以免测吗，怎么申请？\n本专科的，国奖和省政府奖学金能一起申请吗？\n大学生医保我想停保，能办理吗？\nHRU大赛期间有外媒想采访问我，我可以直接去吗？\n我是毕业生，档案转递接收地址写错了咋办？", language="text")

        # 呈现历史对话
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "sources" in msg:
                    # 简化版的紧凑型来源展示（折叠）
                    with st.expander("📚 查看本次检索文献详情"):
                        for i, (id_val, meta) in enumerate(msg["sources"]):
                            c1, c2 = st.columns([4, 1])
                            with c1:
                                st.markdown(f"**[{id_val}]** {meta['title']}")
                            with c2:
                                if st.button("📄 阅读原文", key=f"btn_{msg['id']}_{i}", use_container_width=True):
                                    st.session_state.view_source = id_val
                                    st.rerun()

    # 输入框（永远锚定在左下方）
    current_query = st.chat_input("您可以向我提问...", key="main_chat_input")
    
    if current_query:
        st.session_state.messages.append({"role": "user", "content": current_query, "id": str(len(st.session_state.messages))})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(current_query)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("🔍 检索知识库并思考..."):
                    try:
                        emb_resp = TextEmbedding.call(model=EMBED_MODEL, input=current_query, dimension=1024)
                        query_embed = emb_resp.output["embeddings"][0]["embedding"]
                        
                        results = collection.query(
                            query_embeddings=[query_embed],
                            n_results=3,
                            include=["documents", "metadatas", "distances"]
                        )
                        
                        contexts_docs = results["documents"][0]
                        contexts_metas = results["metadatas"][0]
                        contexts_ids = results["ids"][0]
                    except Exception as e:
                        message_placeholder.error(f"检索失败：{e}")
                        st.stop()

                    system_prompt = build_prompt(current_query, contexts_docs, contexts_metas, contexts_ids)
                    
                    try:
                        responses = Generation.call(
                            model=LLM_MODEL,
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": system_prompt}
                            ],
                            result_format="message",
                            stream=True,
                            incremental_output=True
                        )
                        
                        full_response = ""
                        for resp in responses:
                            if resp.status_code == 200:
                                chunk = resp.output.choices[0].message.content
                                full_response += chunk
                                message_placeholder.markdown(full_response + "▌")
                            else:
                                st.error(f"生成错误：{resp.code} {resp.message}")
                                st.stop()
                        
                        message_placeholder.markdown(full_response)
                        
                        sources_info = list(zip(contexts_ids, contexts_metas))
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": full_response, 
                            "sources": sources_info,
                            "id": str(len(st.session_state.messages))
                        })
                        st.rerun()
                        
                    except Exception as e:
                        message_placeholder.error(f"大模型调用失败：{e}")
