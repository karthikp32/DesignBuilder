import pytest
import os
from designbuilder.coding_agents.python_agent import PythonAgent
from designbuilder.llm_backends.gemini import GeminiBackend

@pytest.fixture
def python_agent():
    component = {
        "name": "HTTP Server",
        "description": """### 1. HTTP Server
- **Type:** Service
- **Responsibilities:**
  - Accept incoming HTTP requests.
  - Route requests to appropriate handlers.
  - Return HTTP responses.
- **Dependencies:** 
  - Request Handler
  - Router
  - Logger
- **Interfaces:**
  - `start_server(port: int)` → starts listening for HTTP requests.
  - `stop_server()` → gracefully stops the server. Write in Python"""
    }
    agent = PythonAgent(component)
    agent.llm_backend = GeminiBackend()
    agent.plan_ = "A reasonable plan for an HTTP server."
    return agent

@pytest.mark.asyncio
async def test_setup_scripts(python_agent):
    await python_agent.setup_scripts()
    assert os.path.exists(python_agent.test_file_path)
    assert os.path.exists(python_agent.output_file_path)

@pytest.mark.asyncio
async def test_plan(python_agent):
    await python_agent.plan()
    assert isinstance(python_agent._plan, str)
    assert len(python_agent._plan) > 0

@pytest.mark.asyncio
async def test_write_tests(python_agent):
    await python_agent.write_tests()
    assert os.path.exists(python_agent.test_file_path)
    with open(python_agent.test_file_path, "r") as f:
        test_code = f.read()
    assert "def test_" in test_code

@pytest.mark.asyncio
async def test_implement(python_agent):
    await python_agent.implement()
    assert os.path.exists(python_agent.output_file_path)
    with open(python_agent.output_file_path, "r") as f:
        impl_code = f.read()
    assert "class" in impl_code or "def" in impl_code

@pytest.mark.asyncio
async def test_test(python_agent):
    # Create dummy files for testing the test method
    with open(python_agent.output_file_path, "w") as f:
        f.write("def main():\n    pass")
    with open(python_agent.test_file_path, "w") as f:
        f.write("def test_main():\n    assert True")

    test_result = await python_agent.test()
    assert test_result == "PASSED"

    # Test with a failing test
    with open(python_agent.test_file_path, "w") as f:
        f.write("def test_main():\n    assert False")

    test_result = await python_agent.test()
    assert test_result == "FAILED"
