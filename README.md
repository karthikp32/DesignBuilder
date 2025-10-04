# DesignBuilder
DesignBuilder reads one or more system design documents, extracts their components, and automatically builds, tests, and debugs those components by orchestrating multiple parallel coding agents. Each agent follows an implement → test → debug loop until its tests pass.

DesignBuilder is designed for modularity and future extensibility. It should support:
- Different agent types (PythonAgent, InfraAgent, etc.).
- Multiple LLM backends (Gemini, Codex, Claude, etc.).
- Local or distributed execution (containers, branches, or async processes).
