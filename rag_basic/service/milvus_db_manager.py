#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Milvus 向量数据库管理（支持 Docker 模式和本地文件模式）。

通过环境变量 MILVUS_HOST 控制连接方式：
  - 设置 MILVUS_HOST → 连接 Docker Milvus (TCP)
  - 未设置 → 使用 Milvus Lite 本地文件 (原始行为)
"""
from pymilvus import MilvusClient, DataType
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MILVUS_HOST = os.getenv("MILVUS_HOST", "")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
MILVUS_DB_PATH = os.getenv("MILVUS_DB_PATH", str(PROJECT_ROOT / "milvus_data" / "rag_basic.db"))


class MilvusDBManager:
    def __init__(self, collection_name="rag_basic", dim=1024):
        self.collection_name = collection_name
        self.dim = dim

        if MILVUS_HOST:
            # Docker Milvus 模式 — TCP 连接
            uri = f"http://{MILVUS_HOST}:{MILVUS_PORT}"
            print(f"连接 Milvus (Docker): {uri}")
            self.client = MilvusClient(uri=uri)
        else:
            # 本地文件模式 — Milvus Lite
            os.makedirs(os.path.dirname(MILVUS_DB_PATH), exist_ok=True)
            print(f"连接 Milvus (本地文件): {MILVUS_DB_PATH}")
            self.client = MilvusClient(uri=MILVUS_DB_PATH)

        self.schema = None
        self.index_params = None

    def initialize(self):
        if self.client.has_collection(self.collection_name):
            print(f"Collection '{self.collection_name}' already exists.")
            return

        self._create_schema()
        self._prepare_index_params()

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=self.schema,
            index_params=self.index_params
        )
        print(f"Collection '{self.collection_name}' created successfully.")

    def _create_schema(self):
        self.schema = self.client.create_schema(enable_dynamic_field=True)
        self.schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
        self.schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
        self.schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=self.dim)
        self.schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)
        self.schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=512)

    def _prepare_index_params(self):
        self.index_params = self.client.prepare_index_params()
        self.index_params.add_index(
            field_name="vector",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"nlist": 128}
        )
        self.index_params.add_index(
            field_name="sparse_vector",
            index_type="SPARSE_INVERTED_INDEX",
            metric_type="IP",
            params={"drop_ratio_build": 0.2}
        )

    def insert_data(self, data):
        if not self.client.has_collection(self.collection_name):
            print(f"Collection '{self.collection_name}' does not exist.")
            return
        self.client.insert(
            collection_name=self.collection_name,
            data=data
        )

    def search(self, query_vector, limit=5, min_similarity=0.5):
        if not self.client.has_collection(self.collection_name):
            return []
        self.client.load_collection(self.collection_name)
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            anns_field="vector",
            limit=limit,
            output_fields=["text", "source"],
            search_params={
                "metric_type": "COSINE",
                "params": {"ef": 512}
            }
        )
        processed_results = []
        for result in results:
            for hit in result:
                if hit["distance"] >= min_similarity:
                    processed_results.append({
                        "text": hit["entity"].get("text", ""),
                        "source": hit["entity"].get("source", ""),
                        "score": hit["distance"]
                    })
        return processed_results

    def hybrid_search(self, query_vector, sparse_vector, limit=5, min_similarity=0.0):
        """混合检索：dense vector + sparse vector 使用 RRF 融合"""
        if not self.client.has_collection(self.collection_name):
            return []
        self.client.load_collection(self.collection_name)
        try:
            results = self.client.hybrid_search(
                collection_name=self.collection_name,
                reqs=[
                    {
                        "data": [query_vector],
                        "anns_field": "vector",
                        "param": {"metric_type": "COSINE"},
                        "limit": limit * 2,
                    },
                    {
                        "data": [sparse_vector],
                        "anns_field": "sparse_vector",
                        "param": {"metric_type": "IP"},
                        "limit": limit * 2,
                    },
                ],
                ranker_type="rrf",
                ranker_params={"k": 60},
                limit=limit,
                output_fields=["text", "source"],
            )
        except Exception as e:
            print(f"Hybrid search failed, falling back to dense search: {e}")
            return self.search(query_vector, limit=limit, min_similarity=0.0)
        processed_results = []
        for hits in results:
            for hit in hits:
                if hit["distance"] >= min_similarity:
                    processed_results.append({
                        "text": hit["entity"].get("text", ""),
                        "source": hit["entity"].get("source", ""),
                        "score": hit["distance"]
                    })
        return processed_results

    def delete_collection(self):
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted.")

    def get_stats(self):
        if not self.client.has_collection(self.collection_name):
            return {"exists": False}
        return {
            "exists": True,
            "name": self.collection_name,
            "num_entities": self.client.get_collection_stats(self.collection_name).get("row_count", 0)
        }
