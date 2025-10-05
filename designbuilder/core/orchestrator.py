"""
Core Orchestrator

Parses design documents, extracts components, and orchestrates
parallel coding agents to build, test, and debug them.
"""
import asyncio
from . import parser
from designbuilder.coding_agents.python_agent import PythonAgent

class Orchestrator:
    """
    Manages the end-to-end build process.
    """
    def __init__(self, design_docs: list[str]):
        self.design_docs = design_docs
        self.components = []
        self.agents = []
        self.agent_map = {}

    async def run(self):
        """
        Main entrypoint to start the build process.
        """
        print("Orchestrator starting...")
        self.components = await parser.parse_design_docs(self.design_docs)
        print(f"Found {len(self.components)} components.")

        tasks = []
        for component in self.components:
            # Agent selection logic can be expanded here
            agent = PythonAgent(component)
            self.agents.append(agent)
            self.agent_map[agent.component['name']] = agent
            tasks.append(agent.run())

        # TODO: Use multiprocessing instead of asyncio.gather for true parallelism.
        # Run all agents in parallel
        await asyncio.gather(*tasks)

        print("All agents have completed their work.")
        self._run_evals()

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
