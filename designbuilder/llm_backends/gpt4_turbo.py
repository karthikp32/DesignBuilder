"""
GPT-4-turbo LLM Backend

An LLM backend that uses OpenAI's GPT-4-turbo API asynchronously.
"""
import os
import openai
from .base import LLMBackend

class GPT4TurboBackend(LLMBackend):
    """
    An LLM backend that uses OpenAI's GPT-4-turbo model.
    """
    def __init__(self, model: str = "gpt-4-turbo"):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key
        self.model = model

    async def send_prompt(self, prompt: str) -> str:
        """Generates content using OpenAI GPT-4-turbo asynchronously."""
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
        )
        return response.choices[0].message.content

