#!/usr/bin/env bash
# ============================================================
# RAG 系统 — 一键启动脚本
# ============================================================
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 检测 Python
PYTHON="python3"
if ! command -v $PYTHON &>/dev/null; then
    PYTHON="python"
fi

echo "=========================================="
echo "  RAG 论文知识问答系统"
echo "=========================================="

# 检查 .env
if [ ! -f rag_basic/.env ]; then
    echo ""
    echo "⚠  未检测到 rag_basic/.env 配置文件"
    echo "   复制 rag_basic/.env.example 为 .env 并填入 API Key"
    echo "   示例: cp rag_basic/.env.example rag_basic/.env"
    echo ""
    echo "   LLM 未配置时将使用纯检索模式（无 LLM 生成）"
    echo ""
fi

echo ""
echo "📦 安装依赖..."
$PYTHON -m pip install -q -r rag_basic/requirements.txt 2>/dev/null || true

echo "🚀 启动 Flask 服务 (端口 5003)..."
echo ""
exec $PYTHON -m rag_basic.flask.rag_flask_service
