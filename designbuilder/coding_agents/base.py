"""
Base Coding Agent Interface

Defines the abstract interface for all coding agents, ensuring
they follow the implement -> test -> debug loop.
"""
import os
from abc import ABC, abstractmethod
from datetime import datetime

class CodingAgent(ABC):
    """
    An abstract base class for an agent that can write, test, and debug code.
    """
    def __init__(self, component: dict):
        self.component = component
        
        # Sanitize component name for filename
        sanitized_name = "".join(c for c in self.component['name'] if c.isalnum() or c in (' ', '_')).rstrip()
        sanitized_name = sanitized_name.replace(' ', '_')
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Define log directory and file
        log_dir = "/home/karthik/repos/DesignBuilder/logs"
        self.log_file = f"{log_dir}/{sanitized_name}_{timestamp}.log"

        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

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