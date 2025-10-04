"""
Base Coding Agent Interface

Defines the abstract interface for all coding agents, ensuring
they follow the implement -> test -> debug loop.
"""
from abc import ABC, abstractmethod

class CodingAgent(ABC):
    """
    An abstract base class for an agent that can write, test, and debug code.
    """
    def __init__(self, component: dict):
        self.component = component
        self.log_file = f"/home/karthik/repos/DesignBuilder/logs/{self.component['name']}.log"

    @abstractmethod
    async def plan(self):
        """Create a plan for implementation."""
        pass

    @abstractmethod
    async def implement(self):
        """Implement the code based on the plan."""
        pass

    @abstractmethod
    async def test(self) -> bool:
        """Test the implementation and return True if tests pass."""
        pass

    @abstractmethod
    async def debug(self):
        """Debug the implementation if tests fail."""
        pass

    async def run(self):
        """
        Execute the full implement -> test -> debug loop.
        """
        await self.plan()
        await self.implement()
        
        if not await self.test():
            await self.debug()
