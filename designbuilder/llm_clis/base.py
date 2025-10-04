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
    async def generate_code(self, prompt: str) -> str:
        """Generate code from a prompt."""
        pass

    @abstractmethod
    async def fix_code(self, code: str, error: str) -> str:
        """Fix code based on an error message."""
        pass
