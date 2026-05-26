#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reranker 模块：使用 CrossEncoder 对检索结果进行重排序。

经过向量检索（Milvus COSINE 距离）初筛后，通过 query-doc 交叉编码
对候选文档做精细的相关性打分，提升最终返回给 LLM 的文档排序质量。
"""
import os
import logging

logger = logging.getLogger(__name__)

_DEFAULT_RERANKER = "BAAI/bge-reranker-base"


class Reranker:
    def __init__(self, model_name=None):
        if model_name is None:
            model_name = os.getenv("RERANKER_MODEL", _DEFAULT_RERANKER)
        self.model_name = model_name
        self.model = None

    def _load_model(self):
        """延迟加载 CrossEncoder 模型，避免启动时占用过多显存。"""
        if self.model is not None:
            return
        try:
            from sentence_transformers import CrossEncoder
            logger.info("Loading reranker model: %s", self.model_name)
            self.model = CrossEncoder(
                self.model_name,
                device=self._get_device(),
            )
            logger.info("Reranker model loaded successfully")
        except Exception as e:
            logger.warning("Failed to load reranker model '%s': %s", self.model_name, e)
            self.model = None

    @staticmethod
    def _get_device():
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            if torch.backends.mps.is_available():
                return "mps"
        except ImportError:
            pass
        return "cpu"

    def rerank(self, query, documents, top_k=5):
        """
        对候选文档进行重排序，返回排序后的 top_k 条。

        Args:
            query: 用户原始查询字符串
            documents: 候选文档列表，每项为 dict，必须含 "text" 字段
            top_k: 最终返回条数

        Returns:
            按重排分数降序排列的文档列表（最多 top_k 条）
        """
        if not documents:
            return documents
        if len(documents) <= top_k:
            # 候选集不足时无需重排
            return documents

        self._load_model()
        if self.model is None:
            # 模型加载失败，退化：按原始 score（余弦距离）降序返回
            return sorted(documents, key=lambda d: d.get("score", 0), reverse=True)[:top_k]

        pairs = [[query, doc.get("text", "")] for doc in documents]
        try:
            scores = self.model.predict(pairs, show_progress_bar=False)
        except Exception as e:
            logger.error("Reranker predict failed: %s", e)
            return sorted(documents, key=lambda d: d.get("score", 0), reverse=True)[:top_k]

        scored = list(zip(documents, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc, score in scored[:top_k]:
            doc = dict(doc)  # 浅拷贝避免污染原始数据
            doc["rerank_score"] = float(score)
            results.append(doc)
        return results
