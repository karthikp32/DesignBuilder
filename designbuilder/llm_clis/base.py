"""
LLM Backend Interface

Provides an abstract interface for different LLM backends.
"""
from abc import ABC, abstractmethod

class LLMBackend(ABC):
    """
    Abstract interface for a large language model backend.
    """
    @abstractmethod
    async def send_prompt(self, prompt: str) -> str:
        """Send a prompt to the LLM."""
        pass
