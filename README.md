# CS-Paper RAG — 计算机科学论文知识问答系统

基于 RAG（检索增强生成）技术的计算机科学论文问答系统。从 arXiv 下载经典 CS 论文，构建向量知识库，支持自然语言问答、多轮对话、流式输出。

## 项目结构

```
rag_proj/
├── docker-compose.yml           # Docker 一键部署（推荐）
├── Dockerfile                   # 应用镜像构建
├── docker-entrypoint.sh         # Docker 容器启动入口
├── run.sh                       # 本地直接运行（非 Docker）
├── rag_basic/                   # Python 包
│   ├── .env.example             # 配置模板（复制为 .env 后填入 API Key）
│   ├── requirements.txt         # Python 依赖
│   ├── rag_main.py              # RAG 核心编排（检索 + 生成）
│   ├── ingest.py                # 数据入库（Markdown → Milvus）
│   ├── preprocess_docs.py       # PDF/DOCX 预处理 → Markdown
│   ├── download_arxiv.py        # arXiv 论文下载
│   ├── utils/
│   ├── service/
│   ├── flask/
│   └── static/
│       └── index.html           # 前端 UI（对话界面）
├── 计算机论文集/                # 论文 PDF 原文
└── res/offline/processed_doc/   # 预处理后的 Markdown 文件
```

## 新手快速上手

### 方式一：Docker 一键部署（推荐）

需要安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

#### 1. 配置 LLM API Key

```bash
cp rag_basic/.env.example rag_basic/.env
```

编辑 `rag_basic/.env`，填入你的 API Key（至少填一个）：

- **Anthropic Claude**：填入 `ANTHROPIC_API_KEY`
- **OpenAI 兼容接口**：填入 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`

#### 2. 准备论文数据

将 PDF 或 DOCX 论文放入 `计算机论文集/` 目录，或运行下载脚本：

```bash
pip install -r rag_basic/requirements.txt
python3 -m rag_basic.download_arxiv
```

然后预处理文档：

```bash
python3 -m rag_basic.preprocess_docs
```

> 预处理后的 Markdown 文件会生成在 `res/offline/processed_doc/` 目录。

#### 3. 启动系统

```bash
docker compose up -d
```

首次启动会自动完成以下步骤：
- 启动 Milvus 向量数据库（含 etcd + MinIO）
- 将论文段落向量化并入库（约 30-40 分钟）
- 预热 AI 模型
- 启动 Web 服务

#### 4. 使用系统

打开浏览器访问 **http://localhost:5003**

- 在输入框输入问题，例如"什么是 Transformer 架构？"
- 系统会检索相关论文段落，并用 LLM 生成回答
- 支持流式输出、多轮对话、相关问题推荐

#### 5. 常用命令

```bash
docker compose logs -f          # 查看日志
docker compose restart rag-app  # 重启应用
docker compose down             # 停止所有服务
```

---

### 方式二：本地直接运行

需要 Python 3.9+ 和 PyTorch。

#### 1. 安装依赖

```bash
pip install -r rag_basic/requirements.txt
```

需要 PyTorch（sentence-transformers 依赖），建议预装：

```bash
pip install torch
```

#### 2. 配置 LLM API Key

```bash
cp rag_basic/.env.example rag_basic/.env
# 编辑 .env 填入 API Key
```

不配置 LLM 则仅返回检索结果，不会生成回答。

#### 3. 准备论文数据

下载论文：

```bash
python3 -m rag_basic.download_arxiv
```

预处理：

```bash
python3 -m rag_basic.preprocess_docs
```

#### 4. 初始化知识库并启动

```bash
bash run.sh
```

脚本会自动完成：入库 → 启动服务。

访问 **http://localhost:5003**

---

## 不配 LLM 也能用

如果不配置 API Key，系统仍然可以检索相关论文段落并展示。只是不会用 AI 生成回答。

## 自定义语料

放入自己的 PDF/DOCX 文档到 `计算机论文集/` 目录：

```bash
python3 -m rag_basic.preprocess_docs
python3 -m rag_basic.ingest --mode clear
python3 -m rag_basic.ingest --mode ingest
```

## API 接口

### POST /api/rag/query
常规查询（非流式）：
```bash
curl -X POST http://localhost:5003/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Transformer architecture?", "top_k": 5}'
```

### POST /api/rag/stream
流式查询（SSE，前端使用）：
```bash
curl -N -X POST http://localhost:5003/api/rag/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Transformer architecture?"}'
```

### GET /api/rag/health
健康检查：
```bash
curl http://localhost:5003/api/rag/health
```

## 技术架构

| 组件 | 技术选型 |
|------|---------|
| **Embedding** | BAAI/bge-large-zh-v1.5 (1024 维) |
| **向量数据库** | Milvus (IVF_FLAT + COSINE) |
| **混合检索** | Dense Vector + Sparse BM25 (RRF 融合) |
| **重排序** | BAAI/bge-reranker-base CrossEncoder |
| **LLM** | Anthropic Claude / OpenAI 兼容接口 |
| **文本分块** | 语义分块（句子边界感知，1500字符/块） |
| **查询扩展** | HyDE（假设性文档嵌入） |
| **前端** | 纯 HTML/CSS/JS，SSE 流式渲染 |
| **部署** | Docker Compose（Milvus Standalone） |
