"""
Core Orchestrator

Parses design documents, extracts components, and orchestrates
parallel coding agents to build, test, and debug them.
"""
import asyncio
import os
from . import parser
from designbuilder.coding_agents.python_agent import PythonAgent
from designbuilder.core.status_manager import StatusManager # Import StatusManager
from designbuilder.core.cache_manager import CacheManager
from designbuilder.core.planner import Planner

class Orchestrator:
    """
    Manages the end-to-end build process.
    """
    def __init__(self, design_docs: list[str]):
        self.design_docs = design_docs
        self.components = []
        self.agents = []
        self.agent_map = {}
        self.status_manager = StatusManager() # Instantiate StatusManager
        self._loaded_agent_states = self.status_manager.get_all_status() # Use StatusManager to load state
        self._agent_counter = 0  # Counter for generating agent names

    def _save_state(self):
        serializable_state = {} # This will hold the state of all agents
        for agent_name, agent in self.agent_map.items():
            serializable_state[agent_name] = {
                "name": agent.component['name'],
                "status": agent.status,
                "debug_attempts": agent.debug_attempts,
                "llm_backend": agent.get_llm_backend_name()
            }
        self.status_manager.set_all_status(serializable_state) # Use set_all_status

    def _generate_agent_name(self) -> str:
        """Generate a unique agent name like agent-1, agent-2, etc."""
        self._agent_counter += 1
        return f"agent-{self._agent_counter}"

    async def run(self):
        """
        Main entrypoint to start the build process.
        """
        print("Orchestrator starting...")

        planner = Planner(design_docs=self.design_docs)
        self.components = await planner.plan_all()
        
        if not self.components:
            print("No components found or generated.")
            self.components = []
            return

        print(f"Found {len(self.components)} components.")

        tasks = []
        self.agents = []
        self.agent_map = {}

        for component in self.components:
            agent_name = self._generate_agent_name()
            agent = PythonAgent(
                component,
                status_manager=self.status_manager,
                agent_name=agent_name
            )
            if 'plan' in component:
                agent._plan = component['plan']

            loaded_state = None
            if component['name'] in self._loaded_agent_states:
                loaded_state = self._loaded_agent_states[component['name']]
            elif agent_name in self._loaded_agent_states:
                loaded_state = self._loaded_agent_states[agent_name]
            
            if loaded_state:
                agent.status = loaded_state.get("status", "initialized")
                agent.debug_attempts = loaded_state.get("debug_attempts", 0)

            self.agents.append(agent)
            self.agent_map[agent_name] = agent
            tasks.append(agent.run())

        self._save_state()

        await asyncio.gather(*tasks)

        print("All agents have completed their work.")
        self._run_evals()
        self._save_state()

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

    async def restart_agent_cycle(self, agent_name: str, guidance: str = None):
        """
        Restart the test-debug cycle for a specific agent with optional guidance.
        
        Args:
            agent_name: Name of the agent to restart
            guidance: Optional guidance to apply before restarting the cycle
            
        Returns:
            bool: True if agent completed successfully, False if paused for guidance
        """
        agent = self.get_agent_by_name(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")
        
        if guidance:
            await agent.guide(guidance)
        
        # Run the test-debug cycle
        success = await agent.run_test_debug_cycle()
        
        # Save state after the cycle
        self._save_state()
        
        return success

    def _run_evals(self):
        """
        Placeholder for running AI evaluations on the generated code.
        """
        print("Running AI evaluations (functional, style, robustness)...")
        # TODO: Implement AI evaluation logic
        pass