#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文本向量化：dense embedding + sparse BM25 向量。

使用 BAAI/bge-large-zh-v1.5 生成稠密向量，
同时基于词频构建稀疏向量用于混合检索。"""
import os
import math
import torch
import numpy as np
from collections import Counter
from sentence_transformers import SentenceTransformer


# BGE 模型要求 encode 时 normalize_embeddings=True，
# 这样后续余弦距离等价于内积，Milvus 的 COSINE 距离计算正确。
# 可通过环境变量覆盖默认模型，例如：
#   EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5  （512维，轻量）
_DEFAULT_MODEL = "BAAI/bge-large-zh-v1.5"
_DEFAULT_DIM = 1024


class TextVectorizer:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.getenv("EMBEDDING_MODEL", _DEFAULT_MODEL)
        device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        self.model = SentenceTransformer(model_path, device=device)

    @property
    def dim(self):
        return self.model.get_sentence_embedding_dimension()

    def vectorize_texts(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True)
        return embeddings.tolist()

    def vectorize_text(self, text):
        return self.vectorize_texts([text])[0]

    def vectorize_sparse(self, text):
        """为混合检索生成 BM25 风格的稀疏向量"""
        import re
        tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        if not tokens:
            return {}
        token_counts = Counter(tokens)
        # 使用 log 频率作为权重
        sparse_dict = {}
        for token, count in token_counts.items():
            token_hash = hash(token) % (2 ** 31 - 1)
            sparse_dict[token_hash] = 1.0 + math.log(count)
        return sparse_dict
