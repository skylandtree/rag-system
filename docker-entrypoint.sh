#!/bin/bash
# ============================================================
# Docker 入口脚本
# 等待 Milvus 就绪 → 检查并入库（首次启动） → 启动 Flask
# ============================================================
set -e

echo "=========================================="
echo "  RAG 论文知识问答系统 — Docker"
echo "=========================================="

# 等待 Milvus 就绪（RESTful API 端点）
echo ""
echo "⏳ 等待 Milvus 服务就绪..."
MILVUS_HOST="${MILVUS_HOST:-milvus}"
MILVUS_PORT="${MILVUS_PORT:-19530}"
RETRIES=0
MAX_RETRIES=30
until curl -sf "http://${MILVUS_HOST}:${MILVUS_PORT}/v2/vectordb/collections/list" -X POST -H 'Content-Type: application/json' -d '{}' > /dev/null 2>&1; do
    RETRIES=$((RETRIES + 1))
    if [ $RETRIES -ge $MAX_RETRIES ]; then
        echo "❌ Milvus 连接超时，请检查 Milvus 容器状态"
        exit 1
    fi
    echo "   等待 Milvus... (${RETRIES}/${MAX_RETRIES})"
    sleep 3
done
echo "✅ Milvus 已就绪"

# 检查是否已有数据
DOC_COUNT=$(python3 -c "
import sys
sys.path.insert(0, '/app')
from rag_basic.service.milvus_db_manager import MilvusDBManager
mgr = MilvusDBManager()
if mgr.client.has_collection(mgr.collection_name):
    stats = mgr.get_stats()
    print(stats.get('num_entities', 0))
else:
    print('0')
" 2>/dev/null | tail -1 || echo "0")

if [ "$DOC_COUNT" = "0" ]; then
    echo ""
    echo "📦 首次启动 — 初始化向量数据库..."
    echo ""
    python3 -m rag_basic.ingest --mode ingest
    echo "✅ 数据入库完成"
else
    echo ""
    echo "📦 数据库已就绪 (${DOC_COUNT} 条记录)"
fi

echo ""
echo "🚀 启动 Flask 服务 (端口 5003)..."
echo ""

exec python3 -m rag_basic.flask.rag_flask_service
