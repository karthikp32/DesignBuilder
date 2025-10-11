"""
Status Manager

This module provides a way to manage the status of the DesignBuilder agents.
"""
import json
import os
from filelock import FileLock

STATUS_FILE = "/home/karthik/repos/DesignBuilder/designbuilder/state/status.json"
LOCK_FILE = "/home/karthik/repos/DesignBuilder/designbuilder/state/status.json.lock"

class StatusManager:
    """
    Manages the status of the agents in a thread-safe and process-safe manner.
    """

    def __init__(self):
        os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
        self._lock = FileLock(LOCK_FILE)

    def get_all_status(self) -> dict:
        """
        Reads all agent statuses from the status file.
        """
        with self._lock:
            if not os.path.exists(STATUS_FILE):
                return {}
            with open(STATUS_FILE, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}

    def get_agent_status(self, agent_name: str) -> dict:
        """
        Reads the status of a specific agent from the status file.
        """
        statuses = self.get_all_status()
        return statuses.get(agent_name, {})

    def set_agent_status(self, agent_name: str, new_status: dict):
        """
        Updates the status of a specific agent in the status file.
        """
        with self._lock:
            statuses = self.get_all_status()
            if agent_name not in statuses:
                statuses[agent_name] = {}
            statuses[agent_name].update(new_status)
            with open(STATUS_FILE, 'w') as f:
                json.dump(statuses, f, indent=4)

    def set_all_status(self, all_statuses: dict):
        """
        Overwrites the entire status file with the given dictionary of statuses.
        """
        with self._lock:
            with open(STATUS_FILE, 'w') as f:
                json.dump(all_statuses, f, indent=4)