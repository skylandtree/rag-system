#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""下载知名计算机科学论文 PDF（通过已知 arXiv ID 直接下载）"""
import os
import sys
import time
import logging
import urllib.request
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = project_root / "计算机论文集"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 经典计算机科学论文的 arXiv ID
KNOWN_PAPERS = [
    # Transformer / Attention
    ("1706.03762", "Attention Is All You Need (Vaswani et al.)"),
    ("2106.09685", "LoRA: Low-Rank Adaptation of LLMs (Hu et al.)"),
    ("2005.11401", "RAG: Retrieval-Augmented Generation (Lewis et al.)"),
    ("2203.02155", "LLaMA: Open Foundation Models (Touvron et al.)"),
    ("2302.13971", "LLaMA 2 (Touvron et al.)"),

    # LLM / NLP
    ("2001.08361", "Scaling Laws for Neural Language Models (Kaplan et al.)"),
    ("2005.14165", "GPT-3: Language Models are Few-Shot Learners (Brown et al.)"),
    ("2201.11903", "Chain-of-Thought Prompting (Wei et al.)"),
    ("2107.03374", "Longformer: Long-Document Transformer (Beltagy et al.)"),
    ("1909.11942", "VL-BERT: Visual-Linguistic BERT (Su et al.)"),

    # CV / Deep Learning
    ("1512.03385", "ResNet: Deep Residual Learning (He et al.)"),
    ("1409.1556", "VGGNet: Very Deep ConvNets (Simonyan et al.)"),
    ("1704.04861", "MobileNets (Howard et al.)"),
    ("1502.03167", "Batch Normalization (Ioffe et al.)"),
    ("1603.05027", "Identity Mappings in ResNet (He et al.)"),

    # Reinforcement Learning
    ("1312.5602", "Deep Q-Network (Mnih et al.)"),
    ("1509.06461", "Deep Reinforcement Learning - Pong (Mnih et al.)"),
    ("1707.06347", "PPO: Proximal Policy Optimization (Schulman et al.)"),
    ("1602.01783", "A3C: Asynchronous Methods (Mnih et al.)"),
    ("1811.02553", "Dota 2 with OpenAI Five"),

    # GNN / Representation Learning
    ("1609.02907", "GCN: Graph Convolutional Networks (Kipf et al.)"),
    ("1703.06103", "Graph Attention Networks (Velickovic et al.)"),
    ("1606.09375", "Gated Graph Neural Networks (Li et al.)"),
    ("1806.01261", "How Powerful are GNNs? (Xu et al.)"),
    ("1901.07291", "Supervised GNNs for Quantum Chemistry"),

    # Additional classics
    ("1406.2661", "Generative Adversarial Nets (Goodfellow et al.)"),
    ("1710.03740", "ALBERT: Lite BERT (Lan et al.)"),
    ("1810.04805", "BERT: Pre-training Deep Bidirectional Transformers (Devlin et al.)"),
    ("1907.11692", "RoBERTa: Robustly Optimized BERT (Liu et al.)"),
    ("1910.01108", "UniLM: Unified Language Model (Dong et al.)"),
]


def search_arxiv_by_id(arxiv_id):
    """通过 arXiv API 获取论文元信息"""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "RAG-Project/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        logger.warning("API查询失败 %s: %s", arxiv_id, e)
        return None


def download_pdf(arxiv_id, output_path):
    """直接下载 arXiv PDF"""
    if output_path.exists():
        logger.info("  已存在: %s (%d KB)", output_path.name, output_path.stat().st_size / 1024)
        return True
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    try:
        urllib.request.urlretrieve(pdf_url, output_path)
        size_kb = output_path.stat().st_size / 1024
        if size_kb < 10:
            output_path.unlink(missing_ok=True)
            logger.warning("  文件过小(%d KB): %s", size_kb, arxiv_id)
            return False
        logger.info("  已下载: %s (%.0f KB)", output_path.name, size_kb)
        return True
    except Exception as e:
        logger.warning("  下载失败 %s: %s", arxiv_id, e)
        return False


def main():
    logger.info("输出目录: %s", OUTPUT_DIR)
    logger.info("计划下载 %d 篇论文\n", len(KNOWN_PAPERS))

    total_downloaded = 0
    total_exists = 0
    total_failed = 0

    for i, (arxiv_id, title) in enumerate(KNOWN_PAPERS):
        filename = f"arxiv_{arxiv_id}.pdf"
        output_path = OUTPUT_DIR / filename

        logger.info("[%02d/%02d] %s | %s", i + 1, len(KNOWN_PAPERS), arxiv_id, title)

        success = download_pdf(arxiv_id, output_path)
        if success:
            total_downloaded += 1
        elif output_path.exists():
            total_exists += 1
        else:
            total_failed += 1

        # 每 5 篇休息 3 秒，避免限流
        if (i + 1) % 5 == 0:
            time.sleep(3)

    # 汇总
    logger.info("\n=== 下载完成 ===")
    logger.info("成功: %d 篇", total_downloaded)
    logger.info("已存在: %d 篇", total_exists)
    logger.info("失败: %d 篇", total_failed)

    pdf_files = sorted(OUTPUT_DIR.glob("arxiv_*.pdf"))
    logger.info("磁盘文件: %d 个", len(pdf_files))

    total_size_kb = sum(f.stat().st_size / 1024 for f in pdf_files)
    logger.info("总大小: %.0f KB (%.1f MB)", total_size_kb, total_size_kb / 1024)

    # 列出文件
    if pdf_files:
        logger.info("\n文件列表:")
        for f in pdf_files:
            logger.info("  %s  (%.0f KB)", f.name, f.stat().st_size / 1024)


if __name__ == "__main__":
    main()
