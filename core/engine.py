"""
Master Antigravity Trajectory Engine for apta AI:
Coordinates trajectory step logging, thinking CoT drawers, tool call dispatching, artifacts, and subagent invocation.
"""

import sys
import json
from typing import List, Dict, Any, Optional

from config import GEMINI_API_KEY, DEFAULT_MODEL, UNIVERSAL_AGENT_PROMPT
from core.tools import ANTIGRAVITY_TOOLS, view_file, replace_file_content, write_to_file, grep_search, find_by_name, list_dir, run_command
from core.artifacts import ArtifactManager
from core.skills import SkillsLoader
from core.subagents import SubagentManager

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class AntigravityEngine:
    """
    Antigravity AI Agent Trajectory Engine.
    Executes thinking steps, dispatches tools, logs step index, and manages artifacts.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        workspace_dir: str = "."
    ):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        self.workspace_dir = workspace_dir
        
        self.artifact_manager = ArtifactManager()
        self.skills_loader = SkillsLoader()
        self.subagent_manager = SubagentManager()
        
        self.step_index = 0
        self.trajectory_log: List[Dict[str, Any]] = []
        
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        if not GENAI_AVAILABLE:
            return
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Warning] Failed to initialize Gemini Client in Engine: {e}", file=sys.stderr)

    def is_configured(self) -> bool:
        return self.client is not None

    def execute_step(
        self,
        user_input: str,
        thinking_cot: str = "Analyzing request, inspecting workspace, and determining optimal action plan..."
    ) -> Dict[str, Any]:
        """
        Execute one step in the Antigravity Trajectory loop.
        """
        self.step_index += 1
        
        step_record = {
            "step_index": self.step_index,
            "type": "PLANNER_RESPONSE",
            "thinking": thinking_cot,
            "user_input": user_input,
            "tool_calls": [],
            "response": ""
        }
        
        if self.is_configured():
            try:
                sys_prompt = UNIVERSAL_AGENT_PROMPT + "\n\n" + self.skills_loader.get_skills_summary()
                config = types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.7,
                    tools=ANTIGRAVITY_TOOLS
                )
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_input,
                    config=config
                )
                
                reply = response.text or "Mama, Antigravity step executed smoothly."
                step_record["response"] = reply
            except Exception as e:
                step_record["response"] = f"Mama, Gemini execution error: {str(e)}"
        else:
            step_record["response"] = (
                "Arey mama! `GEMINI_API_KEY` is not set.\n"
                "Please add `GEMINI_API_KEY` in `.env` to enable full Antigravity Trajectory execution!\n\n"
                f"Antigravity Trajectory Step {self.step_index} logged for: '{user_input}'."
            )

        self.trajectory_log.append(step_record)
        return step_record
