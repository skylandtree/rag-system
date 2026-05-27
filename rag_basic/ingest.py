#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据入库：读取预处理后的 Markdown 文件，向量化后写入 Milvus。

支持 MD5 去重、批量写入、集合清空。
用法: python -m rag_basic.ingest --mode ingest
"""
import os
import sys
import hashlib
import argparse
from pathlib import Path
from tqdm import tqdm

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag_basic.utils.text_splitter import extract_paragraphs_and_summaries
from rag_basic.utils.text_vectorizer import TextVectorizer
from rag_basic.service.milvus_db_manager import MilvusDBManager


def ingest_documents(
    collection_name="rag_basic",
    input_dir=None,
    batch_size=10,
    chunk_size=500,
    overlap=100,
    dedup=True
):
    if input_dir is None:
        input_dir = project_root / "res" / "offline" / "processed_doc"

    print(f"输入目录: {input_dir}")

    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"错误: 输入目录不存在 - {input_dir}")
        return

    md_files = list(input_path.glob("**/*.md"))
    print(f"找到 {len(md_files)} 个Markdown文件")

    if not md_files:
        print("未找到Markdown文件，请检查输入目录")
        return

    vectorizer = TextVectorizer()
    db_manager = MilvusDBManager(
        collection_name=collection_name,
        dim=vectorizer.dim
    )
    print(f"初始化集合: {collection_name} (dim={vectorizer.dim})")
    db_manager.initialize()

    total_chunks = 0
    batch_data = []
    seen_hashes = set()
    dedup_skipped = 0

    for md_file in tqdm(md_files, desc="处理文件"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            paragraphs, summaries = extract_paragraphs_and_summaries(content)

            for para_idx, paragraph in enumerate(paragraphs):
                if not paragraph or paragraph.isspace():
                    continue

                paragraph = paragraph.strip()

                # MD5 去重
                if dedup:
                    text_hash = hashlib.md5(paragraph.encode('utf-8')).hexdigest()
                    if text_hash in seen_hashes:
                        dedup_skipped += 1
                        continue
                    seen_hashes.add(text_hash)

                vector = vectorizer.vectorize_text(paragraph)
                sparse_vector = vectorizer.vectorize_sparse(paragraph)

                relative_path = str(md_file.relative_to(project_root))

                data_item = {
                    "text": paragraph,
                    "vector": vector,
                    "sparse_vector": sparse_vector,
                    "source": f"{relative_path}#para{para_idx+1}"
                }

                batch_data.append(data_item)

                if len(batch_data) >= batch_size:
                    db_manager.insert_data(batch_data)
                    total_chunks += len(batch_data)
                    batch_data = []

        except Exception as e:
            print(f"处理文件失败 {md_file}: {str(e)}")
            continue

    if batch_data:
        db_manager.insert_data(batch_data)
        total_chunks += len(batch_data)

    stats = db_manager.get_stats()
    print(f"\n=== 入库完成 ===")
    if dedup and dedup_skipped > 0:
        print(f"去重跳过: {dedup_skipped} 段")
    print(f"总写入段落数: {total_chunks}")
    print(f"集合名称: {stats.get('name')}")
    print(f"集合记录数: {stats.get('num_entities')}")


def query_test(collection_name="rag_basic", query="测试查询", top_k=3):
    vectorizer = TextVectorizer()
    db_manager = MilvusDBManager(
        collection_name=collection_name,
        dim=vectorizer.dim
    )

    query_vector = vectorizer.vectorize_text(query)
    results = db_manager.search(query_vector, limit=top_k)

    print(f"\n=== 查询结果: {query} ===")
    for i, result in enumerate(results):
        print(f"\n【结果 {i+1}】相似度: {result['score']:.4f}")
        print(f"来源: {result['source']}")
        print(f"内容: {result['text'][:200]}...")


def clear_collection(collection_name="rag_basic"):
    vectorizer = TextVectorizer()
    db_manager = MilvusDBManager(
        collection_name=collection_name,
        dim=vectorizer.dim
    )
    db_manager.delete_collection()
    # Docker 模式下不删除本地文件
    milvus_host = os.environ.get("MILVUS_HOST", "")
    if not milvus_host:
        db_file = project_root / "milvus_data" / f"{collection_name}.db"
        if db_file.exists():
            db_file.unlink()
            print(f"Milvus DB 文件已删除: {db_file}")
        lock_file = project_root / "milvus_data" / f".{collection_name}.db.lock"
        if lock_file.exists():
            lock_file.unlink()
    print(f"集合 {collection_name} 已清空")


def main():
    parser = argparse.ArgumentParser(description="RAG Basic 数据入库工具")
    parser.add_argument('--mode', choices=['ingest', 'query', 'clear'], default='ingest',
                        help='运行模式: ingest(入库), query(测试查询), clear(清空集合)')
    parser.add_argument('--collection', default='rag_basic', help='集合名称')
    parser.add_argument('--input', default=None, help='输入目录路径')
    parser.add_argument('--batch-size', type=int, default=10, help='批次大小')
    parser.add_argument('--query', default='测试查询', help='测试查询语句')
    parser.add_argument('--top-k', type=int, default=3, help='返回结果数量')

    args = parser.parse_args()

    if args.mode == 'ingest':
        ingest_documents(
            collection_name=args.collection,
            input_dir=args.input,
            batch_size=args.batch_size
        )
    elif args.mode == 'query':
        query_test(
            collection_name=args.collection,
            query=args.query,
            top_k=args.top_k
        )
    elif args.mode == 'clear':
        clear_collection(args.collection)


if __name__ == '__main__':
    main()
