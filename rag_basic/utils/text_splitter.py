#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文本分块工具：语义分块 + 段落/摘要提取。

提供 semantic_chunk_text() 按句子边界切分，
以及 extract_paragraphs_and_summaries() 解析预处理后的 Markdown。
"""
import os
import re

WINDOW_SIZE = 200
OVERLAP_SIZE = 20


def split_text_with_overlap(text, window_size=WINDOW_SIZE, overlap_size=OVERLAP_SIZE):
    segments = []
    start = 0
    while start < len(text):
        end = min(start + window_size, len(text))
        segment = text[start:end]
        segments.append(segment)
        start += (window_size - overlap_size)
    return segments


def extract_paragraphs_and_summaries(text):
    text = text.lstrip('﻿')
    sections = text.split("**********段落分割**********")

    paragraphs = []
    summaries = []

    for section in sections:
        section = section.strip()
        if section:
            summary_match = re.search(r"段落总结：(.*)", section)

            if summary_match:
                summary = summary_match.group(1).strip()
                paragraph = re.sub(r"段落总结：.*", "", section).strip()
            else:
                summary = ""
                paragraph = section

            if paragraph:
                paragraphs.append(paragraph)
                summaries.append(summary)

    return paragraphs, summaries


def semantic_chunk_text(text, max_chars=1500, min_chars=300):
    """基于句子边界分块，替代简单按长度切分"""
    sentences = re.split(r'(?<=[.?!。！？])\s+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current) + len(sentence) <= max_chars:
            current += sentence + " "
        elif len(current) >= min_chars:
            chunks.append(current.strip())
            current = sentence + " "
        else:
            current += sentence + " "
            if len(current) >= max_chars:
                chunks.append(current.strip())
                current = ""
    if current.strip():
        chunks.append(current.strip())
    return chunks
