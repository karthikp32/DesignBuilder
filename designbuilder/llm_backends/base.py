"""
LLM Backend Interface

Provides an abstract interface for different LLM backends that use APIs.
"""
from abc import ABC, abstractmethod

class LLMBackend(ABC):
    """
    Abstract interface for a large language model backend.
    """
    @abstractmethod
    async def generate_content(self, prompt: str) -> str:
        """Generate content from a prompt."""
        pass
