"""
Python Coding Agent

A concrete implementation of a CodingAgent that specializes in
writing, testing, and debugging Python code.
"""
import asyncio
from .base import CodingAgent
from designbuilder.llm_clis.gemini_cli import GeminiCliBackend

class PythonAgent(CodingAgent):
    """
    A coding agent for generating Python code.
    """
    def __init__(self, component: dict):
        super().__init__(component)
        self.llm_backend = GeminiCliBackend()

    async def plan(self):
        self._log("Planning Python component...")
        prompt = f"Create a plan to implement the following component: {self.component['description']}"
        plan = await self.llm_backend.generate_code(prompt)
        self._log(f"Plan created: {plan}")

    async def implement(self):
        self._log("Implementing Python component...")
        prompt = f"Implement the following component in Python: {self.component['description']}"
        self.implementation = await self.llm_backend.generate_code(prompt)
        self._log(f"Implementation complete:{self.implementation}")

    async def test(self) -> bool:
        self._log("Testing Python component...")
        await asyncio.sleep(1)
        # Stub: Simulate a test failure on the first try.
        if not hasattr(self, 'debug_run'):
            self._log("Tests failed.")
            return False
        self._log("Tests passed.")
        return True

    async def debug(self):
        self._log("Debugging Python component...")
        prompt = f"The tests failed for the following code:\n\n{self.implementation}\n\nPlease fix it."
        self.implementation = await self.llm_backend.fix_code(self.implementation, "Tests failed")
        self.debug_run = True # Mark that a debug cycle has occurred.
        self._log("Debug complete. Re-running tests.")
        await self.test()

    def _log(self, message: str):
        """Log a message to the agent's log file."""
        # In a real implementation, this would be a more robust logger.
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")
        print(f"[{self.component['name']}] {message}")