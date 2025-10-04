"""
DesignBuilder CLI

This module provides the command-line interface for DesignBuilder,
allowing users to build, monitor, and debug software components
from design documents.
"""
import asyncio
import typer
from typing import List
from designbuilder.core.orchestrator import Orchestrator

app = typer.Typer()

@app.command()
def build(design_docs: List[str]):
    """
    Parse design documents, spawn coding agents, and build components.
    """
    print(f"Building from design documents: {design_docs}")
    orchestrator = Orchestrator(design_docs)
    asyncio.run(orchestrator.run())
    print("Build process completed.")

@app.command()
def status():
    """
    View the progress and test results of all running agents.
    """
    print("Fetching agent statuses...")
    # Placeholder for status logic
    # In a real implementation, this would read from /state/status.json
    # or an in-memory state managed by the orchestrator.

@app.command()
def logs(agent_name: str):
    """
    View the logs for a specific agent.
    """
    print(f"Fetching logs for agent: {agent_name}")
    # Placeholder for log retrieval logic
    # This would typically read from /logs/{agent_name}.log

@app.command()
def debug(agent_name: str):
    """
    Interactively debug a failing agent.
    """
    print(f"Starting debug session for agent: {agent_name}")
    # Placeholder for interactive debugging logic
    # This could attach to a running agent or provide a REPL.

if __name__ == "__main__":
    app()
