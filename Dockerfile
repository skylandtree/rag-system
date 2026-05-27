# ============================================================
# Dockerfile — RAG 论文知识问答系统
# 包含：文档预处理 → 向量入库 → Flask 服务
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（PyMuPDF 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装 Python 包
COPY rag_basic/requirements.txt /app/rag_basic/requirements.txt
RUN pip install --no-cache-dir -r /app/rag_basic/requirements.txt

# 复制项目代码
COPY . /app/

# 入口脚本
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 5003

ENTRYPOINT ["/app/docker-entrypoint.sh"]
