
import pytest
import os
from unittest.mock import AsyncMock
from designbuilder.coding_agents.python_agent import PythonAgent

@pytest.fixture
def python_agent():
    component = {
        "name": "Test Component",
        "description": "A test component."
    }
    agent = PythonAgent(component)
    agent.llm_backend = AsyncMock()
    return agent

@pytest.mark.asyncio
async def test_plan(python_agent):
    python_agent.llm_backend.send_prompt.return_value = "This is a plan."
    await python_agent.plan()
    python_agent.llm_backend.send_prompt.assert_called_once()
    assert python_agent._plan == "This is a plan."

@pytest.mark.asyncio
async def test_setup_scripts(python_agent):
    await python_agent.setup_scripts()
    assert os.path.exists(python_agent.test_file_path)
    assert os.path.exists(python_agent.output_file_path)

@pytest.mark.asyncio
async def test_write_tests(python_agent):
    python_agent.llm_backend.send_prompt.return_value = ""
    await python_agent.write_tests()
    python_agent.llm_backend.send_prompt.assert_called_once()

@pytest.mark.asyncio
async def test_implement(python_agent):
    python_agent.llm_backend.send_prompt.return_value = ""
    await python_agent.implement()
    python_agent.llm_backend.send_prompt.assert_called()

@pytest.mark.asyncio
async def test_test_passing(python_agent, tmp_path):
    # Create a dummy test file that passes
    test_file = tmp_path / "test_passing.py"
    test_file.write_text("def test_success():\n    assert True")
    python_agent.test_file_path = test_file

    result = await python_agent.test()
    assert result == "PASSED"

@pytest.mark.asyncio
async def test_test_failing(python_agent, tmp_path):
    # Create a dummy test file that fails
    test_file = tmp_path / "test_failing.py"
    test_file.write_text("def test_failure():\n    assert False")
    python_agent.test_file_path = test_file

    result = await python_agent.test()
    assert "FAILED" in result

@pytest.mark.asyncio
async def test_debug(python_agent):
    test_summary = "This is a test summary."
    python_agent.llm_backend.send_prompt.return_value = ""
    await python_agent.debug(test_summary)
    python_agent.llm_backend.send_prompt.assert_called_once()

