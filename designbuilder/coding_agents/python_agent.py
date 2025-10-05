
"""
Python Coding Agent

A concrete implementation of a CodingAgent that specializes in
writing, testing, and debugging Python code.
"""
import asyncio
import os
from .base import CodingAgent
from designbuilder.llm_clis.gemini_cli import GeminiCliBackend

class PythonAgent(CodingAgent):
    """
    A coding agent for generating Python code.
    """
    def __init__(self, component: dict):
        super().__init__(component)
        self.llm_backend = GeminiCliBackend()
        self.output_dir = "/home/karthik/repos/DesignBuilder/designbuilder/output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.implementation = "" # Initialize implementation

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

        # Sanitize component name for filename
        sanitized_name = "".join(c for c in self.component['name'] if c.isalnum() or c in (' ', '_')).rstrip()
        sanitized_name = sanitized_name.replace(' ', '_').lower()
        
        output_file_path = os.path.join(self.output_dir, f"{sanitized_name}.py")
        with open(output_file_path, "w") as f:
            f.write(self.implementation)
        self._log(f"Generated code written to {output_file_path}")

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
        self._log(f"Debug complete. Re-running tests. Fixed implementation:{self.implementation}")
        
        # Overwrite the file with the fixed implementation
        sanitized_name = "".join(c for c in self.component['name'] if c.isalnum() or c in (' ', '_')).rstrip()
        sanitized_name = sanitized_name.replace(' ', '_').lower()
        output_file_path = os.path.join(self.output_dir, f"{sanitized_name}.py")
        with open(output_file_path, "w") as f:
            f.write(self.implementation)
        self._log(f"Fixed code written to {output_file_path}")

        self.debug_run = True # Mark that a debug cycle has occurred.
        await self.test()

    async def guide(self, guidance: str):
        self._log(f"User guidance received: {guidance}")
        prompt = f"The user has provided the following guidance:\n\n{guidance}\n\nThe current code is:\n\n{self.implementation}\n\nThe tests are failing. Please incorporate this guidance to fix the code."
        self.implementation = await self.llm_backend.fix_code(self.implementation, guidance) # Use guidance as error for fix_code
        self._log(f"Code updated based on guidance: {self.implementation}")
        self.debug_attempts = 0 # Reset debug attempts after guidance
        self.status = "testing" # Set status to testing to resume loop

    def get_changes_summary(self) -> str:
        summary = f"Current Implementation (after {self.debug_attempts} debug attempts):\n"\
                  f"```python\n{self.implementation}\n```\n"
        return summary

    def _log(self, message: str):
        """Log a message to the agent's log file."""
        # In a real implementation, this would be a more robust logger.
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")
        print(f"[{self.component['name']}] {message}")
