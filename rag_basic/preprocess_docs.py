#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""预处理脚本：将 PDF/DOCX 文档转为 ingest 所需的 .md 格式"""
import re
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import fitz
except ImportError:
    fitz = None
try:
    import docx
except ImportError:
    docx = None


def extract_text_from_pdf(pdf_path):
    if fitz is None:
        print("警告: PyMuPDF 未安装，跳过PDF文件")
        return ""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text


def extract_text_from_docx(docx_path):
    """提取 DOCX 每一段作为独立段落"""
    if docx is None:
        print("警告: python-docx 未安装，跳过DOCX文件")
        return []
    doc = docx.Document(docx_path)
    paragraphs_text = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    # 将连续的短段落合并（如标题与正文），避免碎片化
    merged = []
    buffer = ""
    for p in paragraphs_text:
        if len(p) < 30 and buffer:
            buffer += p
        else:
            if buffer:
                merged.append(buffer)
            buffer = p
    if buffer:
        merged.append(buffer)
    return merged


def split_into_paragraphs(text):
    """将文本按空行分割成段落，检测小节标题并保留上下文"""
    lines = text.split("\n")
    paragraphs = []
    current = []
    section_heading = ""
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                paragraphs.append("".join(current))
                current = []
            continue
        # 检测小节标题（# Header 或 ALL CAPS 短行）
        is_heading = (
            line.startswith("#")
            or (line.isupper() and len(line.split()) <= 8 and len(line) > 5)
        )
        if is_heading:
            if current:
                paragraphs.append("".join(current))
                current = []
            section_heading = line.lstrip("#").strip()
            current.append(line)
            continue
        # 在段落前追加所属小节标题
        if section_heading and not current:
            current.append(f"[{section_heading}]")
            section_heading = ""
        current.append(line)
    if current:
        paragraphs.append("".join(current))
    # 过滤太短的段落
    return [p for p in paragraphs if len(p) > 20]


def split_long_paragraph(para, max_chars=1500):
    """对过长的段落按句子切分（适配英文论文）"""
    if len(para) <= max_chars:
        return [para]
    # 按句号、问号、感叹号分割（支持英文和中文）
    sentences = re.split(r'(?<=[.?!。！？])\s+', para)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) <= max_chars:
            current += s + " "
        else:
            if current.strip():
                chunks.append(current.strip())
            current = s + " "
    if current.strip():
        chunks.append(current.strip())
    # 如果还是太长，强制按长度切
    final = []
    for c in chunks:
        if len(c) > max_chars * 2:
            for i in range(0, len(c), max_chars):
                final.append(c[i:i + max_chars])
        else:
            final.append(c)
    return final


def process_document(file_path, output_dir):
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        paragraphs = split_into_paragraphs(text)
    elif ext == ".docx":
        paragraphs = extract_text_from_docx(file_path)
    else:
        print(f"跳过不支持的文件: {file_path}")
        return

    if not paragraphs:
        print(f"警告: {file_path} 提取内容为空")
        return

    # 对超长段落做语义分块
    final_paragraphs = []
    for p in paragraphs:
        from rag_basic.utils.text_splitter import semantic_chunk_text
        final_paragraphs.extend(semantic_chunk_text(p))

    md_filename = file_path.stem + ".md"
    md_path = output_dir / md_filename

    with open(md_path, "w", encoding="utf-8") as f:
        for i, para in enumerate(final_paragraphs):
            if i > 0:
                f.write("\n**********段落分割**********\n")
            f.write(para + "\n")
            # 英文论文：取前 100 字符作为摘要
            first_sentence = para.split(".")[0] if "." in para else para[:100]
            first_sentence = first_sentence.strip()[:100]
            if len(first_sentence) < 20:
                first_sentence = para[:100]
            f.write(f"段落总结：{first_sentence}\n")

    print(f"已生成: {md_path} ({len(final_paragraphs)} 段落)")


def main():
    input_dir = Path(project_root / "计算机论文集")
    output_dir = Path(project_root / "res" / "offline" / "processed_doc")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")

    supported_exts = {".pdf", ".docx"}
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in supported_exts]
    print(f"找到 {len(files)} 个文档待处理\n")

    for file_path in sorted(files):
        print(f"处理: {file_path.name}")
        process_document(file_path, output_dir)

    print(f"\n预处理完成! 输出目录: {output_dir}")


if __name__ == "__main__":
    main()
