
"""
Gemini LLM Backend Implementation

An implementation that uses the 'gemini' command-line tool.
"""
import asyncio
from designbuilder.llm_clis.base import LLMBackend

class GeminiCliBackend(LLMBackend):
    """
    An implementation that calls the 'gemini' CLI tool as a subprocess.
    """
    async def _run_gemini_cli(self, prompt: str) -> str:
        """Helper function to run the gemini CLI tool."""
        process = await asyncio.create_subprocess_exec(
            "gemini",
            "-p",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Gemini CLI failed: {stderr.decode()}")

        return stdout.decode()

    async def generate_code(self, prompt: str) -> str:
        print(f"Generating code with Gemini CLI for prompt: {prompt[:50]}...")
        return await self._run_gemini_cli(prompt)

    async def fix_code(self, code: str, error: str) -> str:
        prompt = f"Fix the following code:\n\n{code}\n\nThe error was:\n{error}"
        print(f"Fixing code with Gemini CLI for error: {error}")
        return await self._run_gemini_cli(prompt)

