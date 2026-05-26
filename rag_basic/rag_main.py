#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RAG 核心编排：检索 → 重排序 → 生成。

提供 retrieve() / answer() / stream_answer() 三个入口，
支持混合检索、HyDE 查询扩展、模糊检测、相关问题生成。
"""
import re
import sys
import threading
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rag_basic.utils.text_vectorizer import TextVectorizer
from rag_basic.utils.text_splitter import extract_paragraphs_and_summaries
from rag_basic.service.milvus_db_manager import MilvusDBManager
from rag_basic.utils.llm_api import get_llm_instance, get_llm_settings
from rag_basic.utils.reranker import Reranker


class RAGBasic:
    def __init__(
        self,
        collection_name="rag_basic",
        embedding_model=None
    ):
        self.collection_name = collection_name
        self.vectorizer = TextVectorizer(embedding_model)

        # 从 TextVectorizer 获取实际维度来初始化 MilvusDBManager
        self.db_manager = MilvusDBManager(
            collection_name=collection_name,
            dim=self.vectorizer.dim
        )

        self.reranker = Reranker()
        self._lock = threading.Lock()

        settings = get_llm_settings()
        has_valid_llm = bool(settings.OPENAI_API_KEY) or bool(settings.ANTHROPIC_API_KEY)
        if has_valid_llm:
            self.llm = get_llm_instance()
        else:
            self.llm = None

    def initialize_db(self):
        self.db_manager.initialize()

    def _expand_query_hyde(self, query):
        """HyDE: 生成假设性文档 embedding 以提升检索质量"""
        if self.llm is None:
            return None
        hyde_prompt = (
            "Write a short academic paragraph (3-5 sentences) that answers the following question. "
            "Use academic language.\n\n"
            f"Question: {query}\n\nAcademic paragraph:"
        )
        try:
            result = self.llm.chat(hyde_prompt)
            hyde_text = result["text"] if isinstance(result, dict) else result
            if hyde_text and len(hyde_text) > 50:
                return self.vectorizer.vectorize_text(hyde_text)
        except Exception:
            pass
        return None

    def _generate_ambiguous_suggestions(self, query):
        """用 LLM 生成基于用户模糊输入的相关建议问题"""
        if self.llm is None:
            return None
        prompt = (
            "The user asked a vague or short question about computer science papers. "
            "Suggest 2-3 more specific research questions that are closely related to their input, "
            "to help them clarify what they want to know.\n\n"
            f"User's question: {query}\n\n"
            "Return ONLY the suggested questions, one per line, without numbers or prefixes. "
            "Questions should be in the same language as the user's question."
        )
        try:
            result = self.llm.chat(prompt)
            text = result["text"] if isinstance(result, dict) else result
            questions = [
                q.strip().lstrip("1234567890.-) ")
                for q in text.strip().split("\n") if q.strip()
            ]
            return questions[:3]
        except Exception:
            return None

    def _detect_ambiguous_query(self, query):
        """检测模糊/泛化问题，返回建议澄清信息"""
        q = query.strip()
        words = [w for w in q.split() if w]
        q_lower = q.lower().strip()

        # 包含具体 CS 术语 → 不判定为模糊
        specific_topics = [
            "transformer", "attention", "bert", "gpt", "resnet", "cnn", "lstm",
            "gan", "graph neural", "rnn", "gnn", "llm", "nlp", "convolution",
            "reinforcement", "policy gradient", "batch norm", "dropout",
            "embedding", "encoder", "decoder", "self-attention", "multi-head",
            "backpropagation", "optimizer", "activation", "loss function",
            "neural network", "loRA", "fine-tun", "pre-train", "transfer learning",
            "variational", "diffusion", "adversarial", "generative", "contrastive",
            "positional encoding", "layer normalization", "residual",
            "attention mechanism", "bert", "gpt-", "llama", "palm", "chatgpt",
            "machine translation", "text classification", "image classification",
            "object detection", "semantic segmentation", "knowledge distillation",
            "model compression", "quantization", "pruning", "sparsity",
            "transformer architecture", "scaling law", "chain-of-thought",
            "prompt engineering", "in-context learning", "few-shot",
        ]
        for topic in specific_topics:
            if topic in q_lower:
                return None

        # 忽略尾随标点后取前几个词
        clean = re.sub(r'[?？。.!！，,]+$', '', q_lower).strip()
        clean_words = [w for w in clean.split() if w]

        # 1) 问候/无意义输入（1个词或极短）
        greetings = {"hi", "hello", "hey", "你好", "您好", "hi!", "hello!", "hey!"}
        if clean in greetings or (len(words) == 1 and len(q) < 6) or (any(w in greetings for w in words) and len(words) <= 3):
            dynamic = self._generate_ambiguous_suggestions(query)
            return {
                "message": "您的问题比较简短，能否提供更多细节？例如：",
                "suggestions": dynamic or [
                    "Transformer 架构的核心思想是什么？",
                    "比较 ResNet 和 VGGNet 的异同",
                    "什么是注意力机制？在 NLP 中如何应用？"
                ]
            }

        # 2) 单个宽泛术语
        broad_terms = {"ai", "人工智能", "machine learning", "机器学习",
                       "deep learning", "深度学习", "nlp", "计算机科学",
                       "computer science", "论文", "paper", "cs"}
        if clean in broad_terms:
            dynamic = self._generate_ambiguous_suggestions(query)
            return {
                "message": "您的问题比较宽泛，能否具体说明想了解的论文或研究方向？例如：",
                "suggestions": dynamic or [
                    "Transformer 中的自注意力机制是如何工作的？",
                    "LoRA 微调方法的原理是什么？",
                    "图神经网络在推荐系统中的应用"
                ]
            }

        # 3) 非常空泛的提问句式
        vague_starters = ["什么是", "what is", "what are", "tell me about",
                          "介绍下", "介绍一下", "解释", "explain"]
        for vs in vague_starters:
            if q_lower.startswith(vs):
                remainder = q_lower[len(vs):].strip().rstrip("?？")
                # "what is AI" → 剩余词是宽泛术语
                # "explain reinforcement learning" → 含术语，跳过
                if remainder in broad_terms or len(clean_words) <= 2:
                    dynamic = self._generate_ambiguous_suggestions(query)
                    return {
                        "message": "您的问题可以更具体一些。请指定您想了解的论文或技术方向：",
                        "suggestions": dynamic or [
                            "什么是 Transformer？它解决了什么问题？",
                            "ResNet 的残差连接是如何设计的？",
                            "BERT 的预训练任务有哪些？"
                        ]
                    }

        return None

    def _generate_related_questions(self, query, answer):
        """根据问答生成 2~3 个相关问题"""
        if self.llm is None:
            return []
        prompt = (
            "Based on the following Q&A, suggest 2-3 concise related questions "
            "that would help the user deepen their understanding. "
            "Return ONLY the questions, one per line, without numbers or prefixes.\n\n"
            f"Original question: {query}\n\n"
            f"Answer summary: {answer[:600]}\n\n"
            "Related questions:"
        )
        try:
            result = self.llm.chat(prompt)
            text = result["text"] if isinstance(result, dict) else result
            questions = [
                q.strip().lstrip("1234567890.-) ")
                for q in text.strip().split("\n") if q.strip()
            ]
            return questions[:3]
        except Exception:
            return []

    def retrieve(self, query, top_k=5, min_similarity=0.5, use_hybrid=True, use_hyde=False):
        with self._lock:
            query_vector = self.vectorizer.vectorize_text(query)

            # HyDE: 用 LLM 生成假设文档的 embedding 与原始 query 融合
            if use_hyde:
                hyde_vector = self._expand_query_hyde(query)
                if hyde_vector is not None:
                    import numpy as np
                    query_vector = (0.7 * np.array(hyde_vector) + 0.3 * np.array(query_vector)).tolist()

            candidate_k = max(top_k * 4, 20)

            if use_hybrid:
                sparse_vector = self.vectorizer.vectorize_sparse(query)
                results = self.db_manager.hybrid_search(
                    query_vector=query_vector,
                    sparse_vector=sparse_vector,
                    limit=candidate_k,
                    min_similarity=min_similarity
                )
            else:
                results = self.db_manager.search(
                    query_vector=query_vector,
                    limit=candidate_k,
                    min_similarity=min_similarity
                )

            # 使用 reranker 重排序
            if results:
                results = self.reranker.rerank(query, results, top_k=top_k)
            return results

    def answer(self, query, top_k=5, system_prompt=None, chat_history=None):
        context_docs = self.retrieve(query, top_k=top_k)

        if context_docs:
            context_text = "\n\n".join([
                f"【文档{i+1}】来源: {doc.get('source', '未知')}\n{doc.get('text', '')}"
                for i, doc in enumerate(context_docs)
            ])
        else:
            context_text = ""

        if self.llm is None:
            answer = self._generate_answer_without_llm(query, context_text, context_docs)
        else:
            answer = self._generate_answer_with_llm(query, context_text, context_docs, system_prompt, chat_history)

        return answer

    @staticmethod
    def _filter_sources(context_docs, min_score=0.20):
        """过滤低相关性的来源，score 低于 min_score 的不返回"""
        return [
            {"source": doc.get('source', ''), "text": doc.get('text', '')[:500], "score": doc.get('rerank_score', doc.get('score', 0))}
            for doc in context_docs
            if doc.get('rerank_score', doc.get('score', 0)) >= min_score
        ]

    def _generate_answer_without_llm(self, query, context_text, context_docs):
        if not context_text:
            return {
                "answer": f"未检索到相关参考文档。关于「{query}」的问题，建议使用大模型直接回答。",
                "sources": []
            }

        answer_parts = []
        for doc in context_docs:
            text = doc.get('text', '')[:200]
            answer_parts.append(text)

        answer = f"根据检索到的文档，回答「{query}」：\n\n" + "\n\n".join(answer_parts)

        return {
            "answer": answer,
            "sources": self._filter_sources(context_docs)
        }

    def _generate_answer_with_llm(self, query, context_text, context_docs, system_prompt=None, chat_history=None):
        if system_prompt is None:
            system_prompt = "You are a computer science research assistant specializing in academic papers. Answer based on retrieved documents when available. Cite your sources. If the question is in Chinese, answer in Chinese. If in English, answer in English.\n\nWhen comparing models, architectures, or performance metrics, you can include charts using a chart code block:\n```chart\n{\"type\": \"bar\", \"data\": {\"labels\": [\"A\",\"B\"], \"datasets\": [{\"label\": \"Score\", \"data\": [1,2]}]}, \"options\": {\"plugins\": {\"legend\": {\"display\": true}}}}\n```\nSupported chart types: bar, line, radar, doughnut, polarArea."

        if context_text:
            prompt = f"""Please answer the following question.

Prioritize retrieved documents. If information is insufficient, supplement with your own knowledge.

Question: {query}

Retrieved documents:
{context_text}

Answer:"""
        else:
            prompt = f"""Please answer the following question.

No relevant documents found. Answer using your own knowledge.

Question: {query}

Answer:"""

        try:
            result = self.llm.chat(prompt, system_prompt=system_prompt, chat_history=chat_history)
            answer = result["text"] if isinstance(result, dict) else result
            thinking = result.get("thinking", "") if isinstance(result, dict) else ""
        except Exception as e:
            answer = f"调用LLM失败: {str(e)}"
            thinking = ""

        return {
            "answer": answer,
            "thinking": thinking,
            "sources": self._filter_sources(context_docs)
        }

    def stream_answer(self, query, top_k=5, system_prompt=None, chat_history=None):
        context_docs = self.retrieve(query, top_k=top_k)
        input_tokens = max(len(query) // 4, 1)

        yield {
            "stage": "retrieved",
            "docs": context_docs
        }

        # 模糊问题检测 — 如触发则停止，等待用户选择建议
        ambiguous_info = self._detect_ambiguous_query(query)
        if ambiguous_info:
            yield {
                "stage": "ambiguous",
                "message": ambiguous_info["message"],
                "suggestions": ambiguous_info["suggestions"]
            }
            yield {
                "stage": "done",
                "related_questions": [],
                "token_usage": {"input": input_tokens, "output": 0, "total": input_tokens}
            }
            return

        if context_docs:
            context_text = "\n\n".join([
                f"【文档{i+1}】来源: {doc.get('source', '未知')}\n{doc.get('text', '')}"
                for i, doc in enumerate(context_docs)
            ])
        else:
            context_text = ""

        if self.llm is None:
            result = self._generate_answer_without_llm(query, context_text, context_docs)
            output_tokens = len(result["answer"]) // 4
            yield {
                "stage": "answer",
                "content": result["answer"],
                "sources": result["sources"],
                "token_usage": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                }
            }
        else:
            if system_prompt is None:
                system_prompt = "You are a computer science research assistant specializing in academic papers. Answer based on retrieved documents when available. Cite your sources. If the question is in Chinese, answer in Chinese. If in English, answer in English.\n\nWhen comparing models, architectures, or performance metrics, you can include charts using a chart code block:\n```chart\n{\"type\": \"bar\", \"data\": {\"labels\": [\"A\",\"B\"], \"datasets\": [{\"label\": \"Score\", \"data\": [1,2]}]}, \"options\": {\"plugins\": {\"legend\": {\"display\": true}}}}\n```\nSupported chart types: bar, line, radar, doughnut, polarArea."

            if context_text:
                prompt = f"""Please answer the following question.

Prioritize retrieved documents. If information is insufficient, supplement with your own knowledge.

Question: {query}

Retrieved documents:
{context_text}

Answer:"""
            else:
                prompt = f"""Please answer the following question.

No relevant documents found. Answer using your own knowledge.

Question: {query}

Answer:"""

            full_answer = ""
            full_thinking = ""
            for chunk in self.llm.stream_chat(prompt, system_prompt=system_prompt, chat_history=chat_history):
                text = chunk.get("text", "")
                thinking = chunk.get("thinking", "")
                if text:
                    full_answer = text
                if thinking:
                    full_thinking = thinking
                yield {
                    "stage": "generating" if not chunk.get("done") else "finished",
                    "content": full_answer,
                    "thinking": full_thinking,
                    "sources": self._filter_sources(context_docs)
                }

            # 流式完成后：生成相关问题 + token 统计
            related_questions = []
            if full_answer and len(full_answer) > 80:
                try:
                    related_questions = self._generate_related_questions(query, full_answer)
                except Exception:
                    pass

            output_tokens = len(full_answer) // 4
            yield {
                "stage": "done",
                "related_questions": related_questions,
                "token_usage": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                }
            }
