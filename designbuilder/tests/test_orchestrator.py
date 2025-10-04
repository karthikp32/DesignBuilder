"""
Tests for the Core Orchestrator
"""
import pytest
from designbuilder.core.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """
    Test that the orchestrator can be initialized with design documents.
    """
    design_docs = ["design1.md", "design2.md"]
    orchestrator = Orchestrator(design_docs)
    assert orchestrator.design_docs == design_docs

# TODO: Add more tests for running the orchestrator, handling failures, etc.
