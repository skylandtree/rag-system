#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LLM 封装层，提供统一接口。

支持 Anthropic Claude 和 OpenAI 兼容接口，
包含 chat() 和 stream_chat() 两种调用方式。
"""
import os
import asyncio
from pathlib import Path
from typing import AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    # 通用配置
    LLM_PROVIDER: str = ""  # "openai" 或 "anthropic"
    TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 4096

    # OpenAI 兼容
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    MODEL_NAME: str = ""

    # Anthropic
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_BASE_URL: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


def load_llm_settings():
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        return LLMSettings(_env_file=str(env_file))
    return LLMSettings()


_llm_settings = None


def get_llm_settings():
    global _llm_settings
    if _llm_settings is None:
        _llm_settings = load_llm_settings()
    return _llm_settings


class OpenAILLM:
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        settings = get_llm_settings()

        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.model = model or settings.MODEL_NAME
        self.temperature = temperature if temperature is not None else settings.TEMPERATURE
        self.max_tokens = max_tokens or settings.MAX_TOKENS

        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            streaming=True,
            timeout=60,
            max_retries=2,
        )

    def chat(self, query: str = "", system_prompt: str = None, chat_history: list = None) -> dict:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=query))

        for attempt in range(3):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            try:
                resp = loop.run_until_complete(self.llm.ainvoke(messages))
                return {
                    "text": resp.content,
                    "thinking": ""
                }
            except Exception as e:
                if attempt < 2:
                    import time
                    time.sleep(2 ** attempt)
                    continue
                raise e

    def stream_chat(self, query: str, system_prompt: str = None, chat_history: list = None):
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=query))

        async def async_stream():
            full_text = ""
            async for chunk in self.llm.astream(messages):
                if chunk.content:
                    full_text += chunk.content
                    yield {"text": full_text, "thinking": "", "done": False}
            yield {"text": full_text, "thinking": "", "done": True}

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            generator = async_stream()
            while True:
                try:
                    chunk = loop.run_until_complete(generator.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        except Exception as e:
            yield f"Error: {str(e)}"


class AnthropicLLM:
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        settings = get_llm_settings()

        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.base_url = base_url or settings.ANTHROPIC_BASE_URL
        self.model = model or settings.ANTHROPIC_MODEL
        self.temperature = temperature if temperature is not None else settings.TEMPERATURE
        self.max_tokens = max_tokens or settings.MAX_TOKENS

        kwargs = dict(
            model=self.model,
            api_key=self.api_key,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            streaming=True,
            timeout=60,
            max_retries=2,
        )
        if self.base_url:
            kwargs["base_url"] = self.base_url

        self.llm = ChatAnthropic(**kwargs)

    @staticmethod
    def _extract_text(content):
        """从可能包含 thinking 块的 Claude 响应中提取纯文本"""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for block in content:
                if isinstance(block, str) and block.strip():
                    texts.append(block)
                elif isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text", ""))
            return "\n".join(texts)
        return str(content)

    @staticmethod
    def _extract_thinking(content):
        """从 Claude 响应中提取 thinking 内容"""
        if not isinstance(content, list):
            return ""
        for block in content:
            if isinstance(block, dict) and block.get("type") == "thinking":
                return block.get("thinking", "")
        return ""

    def chat(self, query: str = "", system_prompt: str = None, chat_history: list = None) -> dict:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=query))

        for attempt in range(3):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            try:
                resp = loop.run_until_complete(self.llm.ainvoke(messages))
                return {
                    "text": self._extract_text(resp.content),
                    "thinking": self._extract_thinking(resp.content)
                }
            except Exception as e:
                if attempt < 2:
                    import time
                    time.sleep(2 ** attempt)
                    continue
                raise e

    def stream_chat(self, query: str, system_prompt: str = None, chat_history: list = None):
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=query))

        async def async_stream():
            full_text = ""
            full_thinking = ""
            async for chunk in self.llm.astream(messages):
                content = chunk.content
                if not content:
                    continue
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, str) and block.strip():
                            full_text += block
                        elif isinstance(block, dict):
                            if block.get("type") == "text":
                                full_text += block.get("text", "")
                            elif block.get("type") == "thinking":
                                full_thinking += block.get("thinking", "")
                elif isinstance(content, str):
                    full_text += content
                yield {"text": full_text, "thinking": full_thinking}
            # 结束信号
            yield {"text": full_text, "thinking": full_thinking, "done": True}

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            generator = async_stream()
            while True:
                try:
                    chunk = loop.run_until_complete(generator.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        except Exception as e:
            yield f"Error: {str(e)}"


_llm_instance = None


def get_llm_instance(
    api_key: str = None,
    base_url: str = None,
    model: str = None,
    temperature: float = None,
    max_tokens: int = None
):
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    settings = get_llm_settings()
    provider = settings.LLM_PROVIDER

    if provider == "anthropic":
        _api_key = api_key or settings.ANTHROPIC_API_KEY
        _base_url = base_url or settings.ANTHROPIC_BASE_URL
        _model = model or settings.ANTHROPIC_MODEL
        _llm_instance = AnthropicLLM(
            api_key=_api_key,
            base_url=_base_url,
            model=_model,
            temperature=temperature or settings.TEMPERATURE,
            max_tokens=max_tokens or settings.MAX_TOKENS,
        )
    else:
        # 默认使用 OpenAI 兼容
        _api_key = api_key or settings.OPENAI_API_KEY
        _base_url = base_url or settings.OPENAI_BASE_URL
        _model = model or settings.MODEL_NAME
        _llm_instance = OpenAILLM(
            api_key=_api_key,
            base_url=_base_url,
            model=_model,
            temperature=temperature or settings.TEMPERATURE,
            max_tokens=max_tokens or settings.MAX_TOKENS,
        )

    return _llm_instance
