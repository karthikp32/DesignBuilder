"""
Core Orchestrator

Parses design documents, extracts components, and orchestrates
parallel coding agents to build, test, and debug them.
"""
import asyncio
import json
import os
from . import parser
from designbuilder.coding_agents.python_agent import PythonAgent

STATE_DIR = "/home/karthik/repos/DesignBuilder/designbuilder/state"
STATE_FILE_PATH = os.path.join(STATE_DIR, "status.json")

class Orchestrator:
    """
    Manages the end-to-end build process.
    """
    def __init__(self, design_docs: list[str]):
        self.design_docs = design_docs
        self.components = []
        self.agents = []
        self.agent_map = {}
        self._loaded_agent_states = {}
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE_PATH):
            with open(STATE_FILE_PATH, 'r') as f:
                try:
                    self._loaded_agent_states = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode state file {STATE_FILE_PATH}. Starting fresh.")
        os.makedirs(STATE_DIR, exist_ok=True)

    def _save_state(self):
        serializable_state = {}
        for agent_name, agent in self.agent_map.items():
            serializable_state[agent_name] = {
                "name": agent.component['name'],
                "status": agent.status,
                "debug_attempts": agent.debug_attempts
            }
        with open(STATE_FILE_PATH, 'w') as f:
            json.dump(serializable_state, f, indent=4)

    async def run(self):
        """
        Main entrypoint to start the build process.
        """
        print("Orchestrator starting...")
        self.components = await parser.parse_design_docs(self.design_docs)
        print(f"Found {len(self.components)} components.")

        tasks = []
        # Clear previous agents if any, as we are starting a new run
        self.agents = []
        self.agent_map = {}

        for component in self.components:
            agent = PythonAgent(component, orchestrator=self) # Pass orchestrator to agent
            
            # Apply loaded state if available
            if component['name'] in self._loaded_agent_states:
                loaded_state = self._loaded_agent_states[component['name']]
                agent.status = loaded_state.get("status", "initialized")
                agent.debug_attempts = loaded_state.get("debug_attempts", 0)

            self.agents.append(agent)
            self.agent_map[agent.component['name']] = agent
            tasks.append(agent.run())

        self._save_state() # Save initial state after agents are created

        # TODO: Use multiprocessing instead of asyncio.gather for true parallelism.
        # Run all agents in parallel
        await asyncio.gather(*tasks)

        print("All agents have completed their work.")
        self._run_evals()
        self._save_state() # Save final state

    def get_agent_names(self) -> list[str]:
        """
        Returns a list of names of all agents managed by the orchestrator.
        """
        return list(self.agent_map.keys())

    def get_agent_by_name(self, agent_name: str):
        """
        Returns an agent instance by its name.
        """
        return self.agent_map.get(agent_name)

    def _run_evals(self):
        """
        Placeholder for running AI evaluations on the generated code.
        """
        print("Running AI evaluations (functional, style, robustness)...")
        # TODO: Implement AI evaluation logic
        pass
