#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask REST API 服务，提供对话接口。

端点:
  POST /api/rag/query     — 非流式查询
  POST /api/rag/stream    — SSE 流式查询
  GET  /api/rag/health    — 健康检查
  POST /api/rag/init      — 初始化数据库
"""
import os
import sys
import json
import logging
import threading
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, Response, jsonify, send_from_directory, send_file
from rag_basic.rag_main import RAGBasic

static_dir = Path(__file__).parent.parent / "static"
app = Flask(__name__, static_folder=str(static_dir), static_url_path="")
app.config.update({
    'JSON_AS_ASCII': False
})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_rag_instance = None
_rag_lock = threading.Lock()


def get_rag_instance():
    global _rag_instance
    if _rag_instance is None:
        with _rag_lock:
            if _rag_instance is None:
                _rag_instance = RAGBasic()
    return _rag_instance


@app.route('/api/rag/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "缺少query参数"}), 400

        query = data['query'].strip()
        if not query:
            return jsonify({"error": "query不能为空"}), 400

        top_k = data.get('top_k', 5)
        system_prompt = data.get('system_prompt')
        chat_history = data.get('chat_history')

        rag = get_rag_instance()
        result = rag.answer(query, top_k=top_k, system_prompt=system_prompt, chat_history=chat_history)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/rag/stream', methods=['POST'])
def stream_query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "缺少query参数"}), 400

        query = data['query'].strip()
        if not query:
            return jsonify({"error": "query不能为空"}), 400

        top_k = data.get('top_k', 5)
        system_prompt = data.get('system_prompt')
        chat_history = data.get('chat_history')

        rag = get_rag_instance()

        def generate():
            for result in rag.stream_answer(query, top_k=top_k, system_prompt=system_prompt, chat_history=chat_history):
                yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/')
def index():
    return send_file(str(static_dir / "index.html"))


@app.route('/api/rag/health', methods=['GET'])
def health():
    rag = get_rag_instance()
    stats = rag.db_manager.get_stats()
    return jsonify({
        "status": "ok",
        "collection": stats
    })


@app.route('/api/rag/init', methods=['POST'])
def init_db():
    try:
        rag = get_rag_instance()
        rag.initialize_db()
        return jsonify({"status": "ok", "message": "数据库初始化成功"})
    except Exception as e:
        return jsonify({"error": f"初始化失败: {str(e)}"}), 500


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == '__main__':
    port = 5003

    # 预热：启动时加载模型，避免首次请求慢
    print("预热模型中...")
    rag = get_rag_instance()
    rag.initialize_db()
    print("模型预热完成，服务已就绪")

    print(f"RAG Basic 服务启动于: http://0.0.0.0:{port}")
    print(f"  前端UI: http://localhost:{port}/")
    print("API示例:")
    print(f'  curl -X POST http://localhost:{port}/api/rag/query -H "Content-Type: application/json" -d \'{{"query": "测试"}}\'')
    app.run(host='0.0.0.0', port=port, threaded=True)
