# CS-Paper RAG — 计算机科学论文知识问答系统

基于 RAG（检索增强生成）技术的计算机科学论文问答系统。从 arXiv 下载经典 CS 论文，构建向量知识库，支持自然语言问答、多轮对话、流式输出。

## 项目结构

```
rag_proj/
├── run.sh                      # 一键启动脚本
├── rag_basic/                  # Python 包
│   ├── .env.example            # 配置模板（复制为 .env 后填入 API Key）
│   ├── requirements.txt        # Python 依赖
│   ├── rag_main.py             # RAG 核心编排（检索 + 生成）
│   ├── ingest.py               # 数据入库（Markdown → Milvus）
│   ├── preprocess_docs.py      # PDF/DOCX 预处理 → Markdown
│   ├── download_arxiv.py       # arXiv 论文下载
│   ├── utils/
│   │   ├── text_splitter.py    # 语义分块 + 段落提取
│   │   ├── text_vectorizer.py  # 向量化（dense + sparse BM25）
│   │   ├── reranker.py         # CrossEncoder 重排序
│   │   └── llm_api.py          # LLM 封装（Anthropic / OpenAI）
│   ├── service/
│   │   └── milvus_db_manager.py # Milvus Lite 向量数据库管理
│   ├── flask/
│   │   └── rag_flask_service.py # Flask REST API + SSE 流式接口
│   └── static/
│       └── index.html          # 前端 UI（对话界面）
├── 计算机论文集/               # 论文 PDF 原文
├── res/offline/processed_doc/  # 预处理后的 Markdown 文件
└── milvus_data/                # Milvus Lite 向量数据库文件
```

## 技术架构

| 组件 | 技术选型 |
|------|---------|
| **Embedding** | BAAI/bge-large-zh-v1.5 (1024 维) |
| **向量数据库** | Milvus Lite (IVF_FLAT + COSINE) |
| **混合检索** | Dense Vector + Sparse BM25 (RRF 融合) |
| **重排序** | BAAI/bge-reranker-base CrossEncoder |
| **LLM** | Anthropic Claude / OpenAI 兼容接口 |
| **文本分块** | 语义分块（句子边界感知，1500字符/块） |
| **查询扩展** | HyDE（假设性文档嵌入） |
| **前端** | 纯 HTML/CSS/JS，SSE 流式渲染 |

## 特性

- **混合检索**: 稠密向量 + 稀疏 BM25 向量，RRF 融合排序
- **语义分块**: 按句子边界切分，保留小节标题上下文
- **重排序**: CrossEncoder 二次排序，提升 Top-K 质量
- **HyDE 查询扩展**: LLM 生成假设文档，丰富查询语义
- **多轮对话**: localStorage 持久化，刷新不丢失
- **流式输出**: SSE 实时渲染，支持思考过程展示
- **模糊问题检测**: 自动识别模糊查询并给出澄清建议
- **相关问题推荐**: 回答后自动生成 2~3 个关联问题
- **Token 统计**: 每次问答估算输入/输出 Token 数
- **点赞/点踩**: 对每轮回答提供反馈（存储在本地）

## 快速开始

### 1. 安装依赖

```bash
pip install -r rag_basic/requirements.txt
```

需要 PyTorch（sentence-transformers 依赖），建议预装：

```bash
pip install torch
```

### 2. 配置 LLM (可选)

```bash
cp rag_basic/.env.example rag_basic/.env
# 编辑 .env 填入 API Key
```

不配置 LLM 则仅使用检索结果回答。

### 3. 下载论文

```bash
python3 -m rag_basic.download_arxiv
```

将从 arXiv 下载约 30 篇经典计算机科学论文 PDF。

### 4. 预处理

```bash
python3 -m rag_basic.preprocess_docs
```

将 PDF 转为带语义分块的 Markdown 文件。

### 5. 入库

```bash
python3 -m rag_basic.ingest --mode ingest
```

将段落向量化并存入 Milvus Lite。

其他 ingest 模式：
```bash
python3 -m rag_basic.ingest --mode query --query "你的问题"  # 测试查询
python3 -m rag_basic.ingest --mode clear                    # 清空知识库
```

### 6. 启动服务

```bash
# 方式一：一键脚本
bash run.sh

# 方式二：直接启动
python3 -m rag_basic.flask.rag_flask_service
```

访问 http://localhost:5003

## API 接口

### POST /api/rag/query
常规查询（非流式）：
```bash
curl -X POST http://localhost:5003/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Transformer architecture?", "top_k": 5}'
```

### POST /api/rag/stream
流式查询（SSE，前端推荐）：
```bash
curl -N -X POST http://localhost:5003/api/rag/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Transformer architecture?"}'
```

请求参数：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | 必填 | 用户问题 |
| `top_k` | int | 5 | 检索文档数量 |
| `chat_history` | array | [] | 历史消息（多轮对话） |
| `system_prompt` | string | null | 自定义系统提示词 |

### GET /api/rag/health
健康检查：
```bash
curl http://localhost:5003/api/rag/health
```

## 自定义语料

将 PDF/DOCX 文档放入 `计算机论文集/` 目录，然后依次运行：

```bash
python3 -m rag_basic.preprocess_docs
python3 -m rag_basic.ingest --mode clear
python3 -m rag_basic.ingest --mode ingest
```
