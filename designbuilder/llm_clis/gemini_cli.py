"""
Gemini LLM Backend Implementation

An implementation that uses the 'gemini' command-line tool.
"""
import asyncio
import tempfile
from designbuilder.llm_clis.base import LLMBackend

class GeminiCliBackend(LLMBackend):
    """
    An implementation that calls the 'gemini' CLI tool as a subprocess.
    """
    async def _run_gemini_cli(self, prompt: str) -> str:
        """Helper function to run the gemini CLI tool."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as prompt_file, tempfile.NamedTemporaryFile(mode='r', delete=False, suffix='.txt') as output_file:
            
            prompt_file.write(prompt)
            prompt_file.flush()

            process = await asyncio.create_subprocess_exec(
                "gemini", "generate",
                "--prompt-file", prompt_file.name,
                "--output-file", output_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"Gemini CLI failed: {stderr.decode()}")

            return output_file.read()

    async def generate_code(self, prompt: str) -> str:
        print(f"Generating code with Gemini CLI for prompt: {prompt[:50]}...")
        return await self._run_gemini_cli(prompt)

    async def fix_code(self, code: str, error: str) -> str:
        prompt = f"Fix the following code:\n\n{code}\n\nThe error was:\n{error}"
        print(f"Fixing code with Gemini CLI for error: {error}")
        return await self._run_gemini_cli(prompt)