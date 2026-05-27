#!/usr/bin/env bash
# ============================================================
# RAG 系统 — 一键启动脚本
#
# 用法:
#   ./run.sh              — Docker 模式（默认）
#   ./run.sh docker       — Docker 模式（构建镜像 + docker-compose up）
#   ./run.sh local        — 本地模式（直接启动 Flask，需要本地安装依赖）
#   ./run.sh rebuild      — 强制重新构建镜像后启动
#   ./run.sh down         — 停止并清理容器
# ============================================================
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

MODE="${1:-docker}"

case "$MODE" in
    docker|up)
        echo "=========================================="
        echo "  RAG 论文知识问答系统 — Docker 模式"
        echo "=========================================="
        echo ""
        echo "⚙️  构建镜像并启动服务..."
        echo ""
        docker compose up --build -d
        echo ""
        echo "✅ 服务已启动"
        echo "   前端 UI:   http://localhost:5003/"
        echo "   Milvus:    localhost:19530"
        echo ""
        echo "查看日志: docker compose logs -f rag-app"
        echo "停止服务: ./run.sh down"
        ;;

    rebuild)
        echo "=========================================="
        echo "  强制重新构建镜像"
        echo "=========================================="
        docker compose build --no-cache rag-app
        docker compose up -d
        echo ""
        echo "✅ 构建完成并已启动"
        ;;

    down)
        echo "⏹  停止并清理容器..."
        docker compose down
        echo "✅ 已停止"
        ;;

    local)
        echo "=========================================="
        echo "  RAG 论文知识问答系统 — 本地模式"
        echo "=========================================="
        echo ""

        # 检测 Python
        PYTHON="python3"
        if ! command -v $PYTHON &>/dev/null; then
            PYTHON="python"
        fi

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

        echo "📦 安装依赖..."
        $PYTHON -m pip install -q -r rag_basic/requirements.txt 2>/dev/null || true

        echo "🚀 启动 Flask 服务 (端口 5003)..."
        echo ""
        exec $PYTHON -m rag_basic.flask.rag_flask_service
        ;;

    *)
        echo "用法: ./run.sh [docker|local|rebuild|down]"
        echo ""
        echo "  docker    — Docker 模式（默认）"
        echo "  local     — 本地直接启动"
        echo "  rebuild   — 强制重建镜像后启动"
        echo "  down      — 停止服务"
        exit 1
        ;;
esac
