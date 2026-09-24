"""
Antigravity Subagents Delegation System:
Launches and manages specialized subagents (Planner, Researcher, CodeWriter).
"""

from typing import Dict, Any, List, Optional
import uuid

class Subagent:
    """Represents an active Antigravity Subagent instance."""
    
    def __init__(self, type_name: str, role: str, prompt: str):
        self.conversation_id = str(uuid.uuid4())[:8]
        self.type_name = type_name
        self.role = role
        self.prompt = prompt
        self.state = "idle"
        self.transcript: List[Dict[str, str]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversationId": self.conversation_id,
            "type": self.type_name,
            "role": self.role,
            "prompt": self.prompt,
            "state": self.state
        }

class SubagentManager:
    """Manages active subagents in apta AI."""

    def __init__(self):
        self.subagents: Dict[str, Subagent] = {}

    def invoke_subagent(self, type_name: str, role: str, prompt: str) -> Subagent:
        agent = Subagent(type_name, role, prompt)
        self.subagents[agent.conversation_id] = agent
        return agent

    def list_subagents(self) -> List[Dict[str, Any]]:
        return [ag.to_dict() for ag in self.subagents.values()]
