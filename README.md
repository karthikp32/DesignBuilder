# DesignBuilder
DesignBuilder reads one or more system design documents, extracts their components, and automatically builds, tests, and debugs those components by orchestrating multiple parallel coding agents. Each agent follows an implement → test → debug loop until its tests pass.

DesignBuilder is designed for modularity and future extensibility. It should support:
- Different agent types (PythonAgent, InfraAgent, etc.).
- Multiple LLM backends (Gemini, Codex, Claude, etc.).
- Local or distributed execution (containers, branches, or async processes).

## CLI Commands

The DesignBuilder CLI provides commands to build, monitor, and debug your software components.

### `build`

Parse design documents, spawn coding agents, and build components.

**Usage:**
```bash
designbuilder build [DESIGN_DOCS]...
```

**Example:**
```bash
designbuilder build design/system.md design/database.md
```

### `agents-status`

View the progress and test results of all running agents.

**Usage:**
```bash
designbuilder agents-status
```

**Example:**
```bash
designbuilder agents-status
```

### `agent-logs`

View the logs for a specific agent.

**Usage:**
```bash
designbuilder agent-logs [OPTIONS] AGENT_NAME
```

**Options:**
* `--tail`, `-t`: Show the last N lines of the log.

**Example:**
```bash
designbuilder agent-logs my_agent -t 100
```

### `guide`

Interactively debug and guide a failing agent.

**Usage:**
```bash
designbuilder guide AGENT_NAME
```

**Example:**
```bash
designbuilder guide my_failing_agent
```
