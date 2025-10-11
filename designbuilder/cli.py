
"""
DesignBuilder CLI

This module provides the command-line interface for DesignBuilder,
allowing users to build, monitor, and debug software components
from design documents.
"""
import asyncio
import typer
import os
import glob
from typing import List, Optional
from pathlib import Path
from designbuilder.core.orchestrator import Orchestrator
from designbuilder.core.status_manager import StatusManager
from rich.console import Console
from rich.table import Table

app = typer.Typer()

# Global orchestrator instance (not ideal, but simplifies CLI access for now)
orchestrator_instance: Optional[Orchestrator] = None

async def _run_build(design_docs: List[str]):
    global orchestrator_instance
    print(f"Building from design documents: {design_docs}")
    orchestrator_instance = Orchestrator(design_docs)
    await orchestrator_instance.run()
    print("Build process completed.")

@app.command()
def build(design_docs: List[str]):
    """
    Parse design documents, spawn coding agents, and build components.
    """
    asyncio.run(_run_build(design_docs))

@app.command()
def agents_status():
    """
    View the progress and test results of all running agents.
    """
    console = Console()
    table = Table(title="Agent Status")
    table.add_column("NAME", style="cyan", no_wrap=True)
    table.add_column("STATUS", style="magenta")

    status_manager = StatusManager()
    status_data = status_manager.get_all_status()

    if not status_data:
        typer.echo("No build process has been started or no state is saved yet.", err=True)
        raise typer.Exit(1)

    for agent_name, agent_state in status_data.items():
        table.add_row(agent_name, agent_state.get("status", "unknown"))

    console.print(table)

@app.command()
def agent_logs(agent_name: str, tail: Optional[int] = typer.Option(None, "--tail", "-t", help="Show last N lines")):
    """
    View the logs for a specific agent.

    Args:
        agent_name: Name of the agent to view logs for
        tail: Number of last lines to show (optional)
    """
    # Find log files for the specified agent
    log_files = _find_agent_log_files(agent_name)

    if not log_files:
        typer.echo(f"No logs found for agent: {agent_name}", err=True)
        typer.echo("Available agents:", err=True)
        _list_available_agents()
        raise typer.Exit(1)

    # Display logs for all matching files
    for log_file in sorted(log_files, reverse=True):  # Most recent first
        _display_log_file(log_file, tail)

def _find_agent_log_files(agent_name: str) -> List[str]:
    """
    Find log files for a specific agent.

    Args:
        agent_name: Name of the agent to search for

    Returns:
        List of log file paths matching the agent name
    """
    # Sanitize agent name similar to how it's done in CodingAgent
    sanitized_name = "".join(c for c in agent_name if c.isalnum() or c in (' ', '_')).rstrip()
    sanitized_name = sanitized_name.replace(' ', '_')

    # Define log directory (same as in CodingAgent)
    log_dir = "/home/karthik/repos/DesignBuilder/logs"

    if not os.path.exists(log_dir):
        return []

    # Search for log files matching the agent name pattern
    # Pattern: {sanitized_name}_YYYYMMDD-HHMMSS.log
    pattern = f"{log_dir}/{sanitized_name}_*.log"
    log_files = glob.glob(pattern)

    # Also search for exact matches (in case the agent name is already sanitized)
    exact_pattern = f"{log_dir}/{agent_name}_*.log"
    exact_files = glob.glob(exact_pattern)

    # Combine and deduplicate
    all_files = list(set(log_files + exact_files))

    return all_files

def _display_log_file(log_file: str, tail: Optional[int] = None):
    """
    Display the contents of a log file.

    Args:
        log_file: Path to the log file
        tail: Number of last lines to show (None for all lines)
    """
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()

        # Show file header
        file_name = Path(log_file).name
        typer.echo(f"\n{'='*60}")
        typer.echo(f"Log file: {file_name}")
        typer.echo(f"{'='*60}")

        # Display lines (last N if tail is specified)
        if tail and len(lines) > tail:
            lines = lines[-tail:]
            typer.echo(f"... showing last {tail} lines ...")

        for line in lines:
            typer.echo(line.rstrip())

    except Exception as e:
        typer.echo(f"Error reading log file {log_file}: {e}", err=True)

def _list_available_agents():
    """
    List all available agents based on log files in the logs directory.
    """
    log_dir = "/home/karthik/repos/DesignBuilder/logs"

    if not os.path.exists(log_dir):
        typer.echo("No logs directory found.", err=True)
        return

    log_files = glob.glob(f"{log_dir}/*.log")

    if not log_files:
        typer.echo("No log files found.", err=True)
        return

    # Extract agent names from log files
    agents = set()
    for log_file in log_files:
        file_name = Path(log_file).stem  # Remove .log extension
        # Remove timestamp part (everything after the last _)
        parts = file_name.split('_')
        if len(parts) >= 2:
            # Remove the last part (timestamp) and rejoin
            agent_name = '_'.join(parts[:-1])
            agents.add(agent_name)

    if agents:
        for agent in sorted(agents):
            typer.echo(f"  - {agent}", err=True)
    else:
        typer.echo("No agents found.", err=True)

@app.command()
def guide(agent_name: str):
    """
    Interactively debug and guide a failing agent.
    """
    status_manager = StatusManager()
    agent_status = status_manager.get_agent_status(agent_name)

    if not agent_status:
        typer.echo(f"Error: Agent '{agent_name}' not found.", err=True)
        raise typer.Exit(1)

    if agent_status.get("status") != "paused_for_guidance":
        typer.echo(f"Agent '{agent_name}' is not paused for guidance.", err=True)
        raise typer.Exit(1)

    # Main guidance menu loop
    while True:
        _show_guidance_menu(agent_name)
        choice = typer.prompt("Choose an option", type=int, default=1)
        
        if choice == 1:
            # Interactive guidance mode
            _interactive_guidance_mode(agent_name, status_manager)
        elif choice == 2:
            # Guide once and retry test-debug cycle
            _guided_retry_mode(agent_name, status_manager)
        elif choice == 3:
            # Quit
            typer.echo("Exiting guidance session.")
            break
        else:
            typer.echo("Invalid choice. Please select 1, 2, or 3.", err=True)

def _show_guidance_menu(agent_name: str):
    """Display the guidance menu options."""
    typer.echo(f"\n{'='*60}")
    typer.echo(f"Guidance Menu for Agent: {agent_name}")
    typer.echo(f"{'='*60}")
    typer.echo("1) Interactively guide")
    typer.echo("2) Guide once and retry test-debug cycle")
    typer.echo("3) Quit")
    typer.echo(f"{'='*60}")

def _interactive_guidance_mode(agent_name: str, status_manager: StatusManager):
    """Launch interactive gemini CLI mode."""
    typer.echo(f"\nStarting interactive guidance mode for agent '{agent_name}'...")
    typer.echo("Type 'exit' or 'quit' to return to the main menu.")
    
    try:
        # Launch gemini CLI in interactive mode
        import subprocess
        result = subprocess.run(["gemini", "-i"], 
                              input="", 
                              text=True, 
                              capture_output=False)
        
        if result.returncode == 0:
            typer.echo("Interactive session completed.")
        else:
            typer.echo("Interactive session ended with an error.")
            
    except FileNotFoundError:
        typer.echo("Error: 'gemini' command not found. Please ensure gemini CLI is installed.", err=True)
    except Exception as e:
        typer.echo(f"Error launching interactive mode: {e}", err=True)

def _guided_retry_mode(agent_name: str, status_manager: StatusManager):
    """Provide guidance once and restart test-debug cycle."""
    typer.echo(f"\nProvide guidance for agent '{agent_name}':")
    guidance = typer.prompt("Your guidance")
    
    if guidance.lower() in ['exit', 'quit']:
        typer.echo("Cancelling guidance.")
        return
    
    # Update agent status with guidance
    status_manager.set_agent_status(
        agent_name,
        {
            "status": "guided",
            "guidance": guidance
        }
    )
    
    typer.echo(f"Guidance has been saved for agent '{agent_name}'.")
    typer.echo("Starting test-debug cycle with your guidance...")
    
    # Use orchestrator to restart the cycle with guidance
    global orchestrator_instance
    if orchestrator_instance:
        try:
            success = asyncio.run(orchestrator_instance.restart_agent_cycle(agent_name, guidance))
            if success:
                typer.echo(f"Agent '{agent_name}' completed successfully!")
            else:
                typer.echo(f"Agent '{agent_name}' needs more guidance after debug attempts.")
        except ValueError as e:
            typer.echo(f"Error: {e}", err=True)
        except Exception as e:
            typer.echo(f"Error during guidance application: {e}", err=True)
    else:
        typer.echo("No orchestrator instance available. Please run 'build' first.", err=True)

if __name__ == "__main__":
    app()
