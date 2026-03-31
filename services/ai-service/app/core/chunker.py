"""
文本切分器 — 针对 Markdown / TXT 的轻量级 Chunking 实现

功能：
- 优先按 Markdown 标题层级（# 至 ######）切分，保留文档结构
- 超长段落按字符数切分，维持指定重叠量
- 纯 Python 标准库实现，零额外依赖
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TextChunk:
    """文本片段数据结构"""
    content: str                    # 切分后的文本内容
    index: int                      # 在原文中的顺序索引
    source_path: str                # 源文件路径
    metadata: Dict[str, Any]        # 附加元数据（标题层级、原始标题等）


class MarkdownTextSplitter:
    """
    Markdown 文本切分器
    
    策略：
    1. 先按 Markdown 标题（# 开头）将文档切分为逻辑块
    2. 每个逻辑块若超过 chunk_size，则按字符数进一步切分
    3. 切分时维持 overlap 大小的上下文重叠
    """
    
    # Markdown 标题正则（匹配行首的 # 至 ######）
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ):
        """
        初始化切分器
        
        Args:
            chunk_size: 每个 chunk 的目标字符数（不含重叠部分）
            chunk_overlap: 相邻 chunk 之间的重叠字符数
        """
        if chunk_overlap >= chunk_size:
            raise ValueError(f"chunk_overlap ({chunk_overlap}) 必须小于 chunk_size ({chunk_size})")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split(
        self,
        text: str,
        source_path: str = "",
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[TextChunk]:
        """
        切分文本为多个 chunk
        
        Args:
            text: 原始文本内容
            source_path: 源文件路径（用于溯源）
            base_metadata: 基础元数据（标题、分类等）
        
        Returns:
            TextChunk 列表
        """
        if not text or not text.strip():
            return []
        
        base_metadata = base_metadata or {}
        chunks: List[TextChunk] = []
        chunk_index = 0
        
        # 步骤1：按 Markdown 标题切分为逻辑块
        sections = self._split_by_headings(text)
        
        for section in sections:
            section_content = section["content"]
            section_metadata = {
                **base_metadata,
                "heading_level": section["level"],
                "heading_title": section["title"],
            }
            
            # 步骤2：如果该部分内容较短，直接作为一个 chunk
            if len(section_content) <= self.chunk_size:
                chunks.append(TextChunk(
                    content=section_content.strip(),
                    index=chunk_index,
                    source_path=source_path,
                    metadata=section_metadata,
                ))
                chunk_index += 1
                continue
            
            # 步骤3：内容过长，按字符数切分（带重叠）
            section_chunks = self._split_by_size(section_content)
            for sc in section_chunks:
                chunks.append(TextChunk(
                    content=sc.strip(),
                    index=chunk_index,
                    source_path=source_path,
                    metadata=section_metadata,
                ))
                chunk_index += 1
        
        return chunks
    
    def _split_by_headings(self, text: str) -> List[Dict[str, Any]]:
        """
        按 Markdown 标题切分文档为逻辑块
        
        Returns:
            每个块包含：level(标题层级), title(标题内容), content(块内容)
        """
        # 在文本开头添加一个虚拟标题，确保整个文档都被处理
        if not text.lstrip().startswith('#'):
            text = "# Document\n" + text
        
        matches = list(self.HEADING_PATTERN.finditer(text))
        
        if not matches:
            # 无标题结构，整体作为一个块返回
            return [{
                "level": 0,
                "title": "",
                "content": text,
            }]
        
        sections = []
        for i, match in enumerate(matches):
            level = len(match.group(1))  # # 的数量
            title = match.group(2).strip()
            start_pos = match.start()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start_pos:end_pos]
            
            sections.append({
                "level": level,
                "title": title,
                "content": content,
            })
        
        return sections
    
    def _split_by_size(self, text: str) -> List[str]:
        """
        按字符数切分长文本，维持指定重叠量
        
        策略：
        - 每个 chunk 约 chunk_size 字符
        - 相邻 chunk 重叠 chunk_overlap 字符
        - 优先在换行符处切分，避免切断句子
        """
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # 计算本次切分的结束位置
            end = min(start + self.chunk_size, text_len)
            
            if end < text_len:
                # 尝试在换行符处切分（回退最多 50 字符）
                search_start = max(end - 50, start)
                newline_pos = text.rfind('\n', search_start, end + 50)
                if newline_pos != -1 and newline_pos > start:
                    end = newline_pos
            
            chunk_content = text[start:end]
            chunks.append(chunk_content)
            
            # 计算下一个起始位置（考虑重叠）
            next_start = end - self.chunk_overlap
            if next_start <= start:
                # 防止死循环
                next_start = end
            start = next_start
        
        return chunks


class SimpleTextSplitter:
    """
    纯文本切分器（用于无 Markdown 结构的 .txt 文件）
    
    仅按字符数 + 重叠量切分，无标题结构感知
    """
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split(
        self,
        text: str,
        source_path: str = "",
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[TextChunk]:
        """切分纯文本"""
        if not text or not text.strip():
            return []
        
        base_metadata = base_metadata or {}
        chunks = []
        start = 0
        text_len = len(text)
        index = 0
        
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            if end < text_len:
                # 尝试在换行符处切分
                search_start = max(end - 50, start)
                newline_pos = text.rfind('\n', search_start, end + 50)
                if newline_pos != -1 and newline_pos > start:
                    end = newline_pos
            
            chunks.append(TextChunk(
                content=text[start:end].strip(),
                index=index,
                source_path=source_path,
                metadata=base_metadata,
            ))
            index += 1
            
            next_start = end - self.chunk_overlap
            if next_start <= start:
                next_start = end
            start = next_start
        
        return chunks


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """
    解析 Markdown frontmatter（YAML 格式）
    
    格式示例：
    ---
    title: 文档标题
    category: 入学与学籍
    tags: [tag1, tag2]
    ---
    
    Returns:
        (metadata_dict, content_without_frontmatter)
    """
    metadata = {}
    
    # 检查是否以 --- 开头
    if not content.lstrip().startswith('---'):
        return metadata, content
    
    # 找到第二个 ---
    lines = content.split('\n')
    if len(lines) < 2:
        return metadata, content
    
    end_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        return metadata, content
    
    # 解析 frontmatter 行（简化版，支持 key: value 格式）
    frontmatter_lines = lines[1:end_idx]
    for line in frontmatter_lines:
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            
            # 简单处理数组格式 [a, b, c]
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
            
            metadata[key] = value
    
    # 剩余内容
    remaining_content = '\n'.join(lines[end_idx + 1:])
    return metadata, remaining_content


# 默认切分器实例（可被外部导入使用）
default_splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
