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
    MAX_DEBUG_ATTEMPTS = 10

    def __init__(self, component: dict):
        self.component = component
        self.debug_attempts = 0
        self.status = "initialized" # New: Agent status
        self.changes_summary = [] # New: To store summaries of changes
        
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

    @abstractmethod
    async def guide(self, guidance: str):
        """Guide the agent with user input."""
        pass

    async def run(self):
        """
        Execute the full implement -> test -> debug loop.
        """
        self.status = "planning"
        await self.plan()
        
        self.status = "implementing"
        await self.implement()
        
        self.status = "testing"
        while not await self.test():
            if self.debug_attempts >= self.MAX_DEBUG_ATTEMPTS:
                self._log(f"Max debug attempts ({self.MAX_DEBUG_ATTEMPTS}) reached for {self.component['name']}. Manual intervention required.")
                print(f"[ATTENTION] Max debug attempts reached for {self.component['name']}. Please review logs and code for manual debugging.")
                self.status = "paused_for_guidance" # New: Set status to paused
                break
            
            self.debug_attempts += 1
            self._log(f"Debug attempt {self.debug_attempts}/{self.MAX_DEBUG_ATTEMPTS} for {self.component['name']}.")
            self.status = "debugging"
            await self.debug()
            self.status = "testing" # After debug, re-test
        
        if self.status != "paused_for_guidance":
            self.status = "completed" # New: Set status to completed if not paused

    def _log(self, message: str):
        """Log a message to the agent's log file."""
        # In a real implementation, this would be a more robust logger.
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")
        print(f"[{self.component['name']}] {message}")

    def get_changes_summary(self) -> str:
        """
        Returns a summary of changes made during debugging.
        This should be implemented by concrete agents.
        """
        return "No specific changes summary available from base agent."