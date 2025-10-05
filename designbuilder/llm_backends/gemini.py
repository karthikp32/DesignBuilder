"""
Gemini LLM Backend

An LLM backend that uses the google-generativeai library.
"""
import os
import google.generativeai as genai
from .base import LLMBackend

class GeminiBackend(LLMBackend):
    """
    An LLM backend that uses the google-generativeai library.
    """
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_content(self, prompt: str) -> str:
        """Generates content using the Gemini API."""
        response = await self.model.generate_content_async(prompt)
        return response.text
