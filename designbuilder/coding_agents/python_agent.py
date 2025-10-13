"""
Python Coding Agent

A concrete implementation of a CodingAgent that specializes in
writing, testing, and debugging Python code.
"""
import asyncio
import os
from .base import CodingAgent
from designbuilder.llm_backends.gemini import GeminiBackend
from designbuilder.prompts import prompts

class PythonAgent(CodingAgent):
    """
    A coding agent for generating Python code.
    """
    def __init__(self, component: dict, orchestrator=None):
        super().__init__(component, orchestrator)
        self.llm_backend = GeminiBackend()
        self.output_dir = "/home/karthik/repos/DesignBuilder/designbuilder/output"
        self.tests_dir = os.path.join(self.output_dir, "tests")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.tests_dir, exist_ok=True)
        self._plan = ""  # Store the plan from plan() function
        self._implementation = ""  # Store the latest implementation

        # Sanitize component name for filename
        sanitized_name = "".join(c for c in self.component['name'] if c.isalnum() or c in (' ', '_')).rstrip()
        self.sanitized_name = sanitized_name.replace(' ', '_').lower()
        self.output_file_path = os.path.join(self.output_dir, f"{self.sanitized_name}.py")
        self.test_file_path = os.path.join(self.tests_dir, f"test_{self.sanitized_name}.py")

    def _extract_code(self, markdown_string: str) -> str:
        """Extracts code from a markdown string."""
        if not markdown_string or markdown_string.strip() == "":
            return ""
        
        # Try to extract from python code blocks first
        if "```python" in markdown_string:
            parts = markdown_string.split("```python")
            if len(parts) > 1:
                code_part = parts[1].split("```")[0]
                return code_part.strip()
        
        # Try to extract from generic code blocks
        if "```" in markdown_string:
            parts = markdown_string.split("```")
            if len(parts) > 1:
                code_part = parts[1].split("```")[0]
                return code_part.strip()
        
        # If no code blocks found, return the original string (might be plain code)
        return markdown_string.strip()

    async def plan(self):
        """
        Generate a concise, actionable implementation plan for the component.
        """
        self._log("Planning Python component...")

        prompt = prompts.get_plan_prompt(self.component['description'])

        # Send the structured planning prompt to the LLM backend (Gemini CLI, Codex, etc.)
        self._plan = await self.llm_backend.send_prompt(prompt)

        # Log for visibility
        self._log(f"Plan created:\n{self._plan}")

    async def setup_scripts(self):
        self._log("Setting up script files...")
        with open(self.test_file_path, "w") as f:
            pass
        self._log(f"Created empty test file: {self.test_file_path}")
        with open(self.output_file_path, "w") as f:
            pass
        self._log(f"Created empty implementation file: {self.output_file_path}")

    async def write_tests(self):
        """
        Generate pytest-style unit tests for the current component.
        """
        self._log("Writing unit tests...")

        prompt = prompts.get_write_tests_prompt(self.component['description'])

        # Send prompt to the LLM backend (Gemini CLI, Codex, etc.)
        test_code = await self.llm_backend.send_prompt(prompt)
        
        # Extract code from response and write to file
        code = self._extract_code(test_code)
        with open(self.test_file_path, "w") as f:
            f.write(code)
        self._log(f"Unit tests written to {self.test_file_path}")

    async def implement(self):
        self._log("Implementing Python component...")
        prompt = prompts.get_implement_prompt(self._plan)
        implementation_code = await self.llm_backend.send_prompt(prompt)
        
        # Extract code from response and write to file
        code = self._extract_code(implementation_code)
        self._implementation = code  # Store the implementation
        with open(self.output_file_path, "w") as f:
            f.write(code)
        self._log(f"Generated code written to {self.output_file_path}")

    async def test(self) -> str:
        self._log("Testing Python component...")
        
        # Run pytest on the test file
        result = await asyncio.create_subprocess_exec(
            "pytest", self.test_file_path, "-v",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()

        test_output = stdout.decode() + stderr.decode()
        
        if result.returncode == 0:
            self._log("Tests passed.")
            return "PASSED"
        else:
            self._log(f"Tests failed:\n{test_output}")
            return "FAILED"

    async def debug(self, test_summary: str):
        self._log("Debugging Python component...")
        prompt = prompts.get_debug_prompt(self._implementation, test_summary)
        
        fixed_code = await self.llm_backend.send_prompt(prompt)
        
        # Extract code from response and write to file
        code = self._extract_code(fixed_code)
        self._implementation = code  # Update stored implementation
        with open(self.output_file_path, "w") as f:
            f.write(code)
        self._log(f"Fixed code written to {self.output_file_path}")

    async def guide(self, guidance: str):
        self._log(f"User guidance received: {guidance}")
        prompt = prompts.get_guide_prompt(guidance, self._implementation)
        
        guided_code = await self.llm_backend.send_prompt(prompt)
        
        # Extract code from response and write to file
        code = self._extract_code(guided_code)
        self._implementation = code  # Update stored implementation
        with open(self.output_file_path, "w") as f:
            f.write(code)
        self._log(f"Code updated based on guidance and written to {self.output_file_path}")
        self.debug_attempts = 0 # Reset debug attempts after guidance
        self.status = "testing" # Set status to testing to resume loop

    async def run_test_debug_cycle(self):
        """
        Run the complete test-debug cycle until completion or max attempts reached.
        """
        self._log("Starting test-debug cycle...")
        
        while self.status in ["testing", "debugging"] and self.debug_attempts < 3:
            if self.status == "testing":
                test_result = await self.test()
                if test_result == "PASSED":
                    self.status = "completed"
                    self._log("Agent completed successfully!")
                    return True
                else:
                    self.status = "debugging"
            
            if self.status == "debugging":
                await self.debug(test_result)
                self.debug_attempts += 1
                
                if self.debug_attempts >= 3:
                    self.status = "paused_for_guidance"
                    self._log(f"Agent needs more guidance after {self.debug_attempts} debug attempts.")
                    return False
                else:
                    self.status = "testing"
        
        return self.status == "completed"

    async def interactive_prompt(self, prompt: str) -> str:
        self._log(f"Interactive prompt received: {prompt}")
        response = await self.llm_backend.send_prompt(prompt) # Only send the user's prompt
        self._log(f"Interactive prompt response: {response}")
        return response

    def get_changes_summary(self) -> str:
        summary = f"Agent Status (after {self.debug_attempts} debug attempts):\n" \
                  f"- Output file: {self.output_file_path}\n" \
                  f"- Test file: {self.test_file_path}\n" \
                  f"- Plan: {self._plan[:200]}...\n" \
                  f"- Current Implementation:\n```python\n{self._implementation}\n```\n"
        return summary

    def get_llm_backend_name(self) -> str:
        """Returns a user-friendly name for the LLM backend."""
        return "Gemini"

    def _log(self, message: str):
        """Log a message to the agent's log file."""
        # In a real implementation, this would be a more robust logger.
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")
        print(f"[{self.component['name']}] {message}")