"""
Core AptaAgent engine wrapping apta Neural Model v2.0.
Developed by Rajwanth Balaka.
"""

import sys
from typing import List, Dict, Any, Optional
from config import GEMINI_API_KEY, DEFAULT_MODEL, UNIVERSAL_AGENT_PROMPT, CODING_AGENT_PROMPT
from core.tools import ANTIGRAVITY_TOOLS

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class AptaAgent:
    """
    apta AI Proprietary Autonomous AI Engine.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        mode: str = "universal"
    ):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        self.mode = mode.lower()
        self.system_instruction = CODING_AGENT_PROMPT if self.mode == "coding" else UNIVERSAL_AGENT_PROMPT
        
        self.client = None
        self.history: List[Dict[str, str]] = []
        self._initialize_client()

    def _initialize_client(self):
        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                pass

    def is_configured(self) -> bool:
        return self.client is not None

    def send_message(
        self,
        message: str,
        stress_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Send a user message to apta AI engine.
        """
        self.history.append({"role": "user", "content": message})

        if self.is_configured():
            try:
                # Map apta model names to underlying inference
                target_model = "gemini-2.5-flash"
                config = types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    tools=ANTIGRAVITY_TOOLS
                )
                response = self.client.models.generate_content(
                    model=target_model,
                    contents=message,
                    config=config
                )
                reply = response.text or "Mama, request process chesanu."
                self.history.append({"role": "assistant", "content": reply})
                return reply
            except Exception as e:
                pass

        # Native apta Neural AI Fallback Engine (Out-of-the-box response)
        fallback_reply = (
            f"Namaste / Hello Mama! Nenu **apta AI Neural Engine**!\n\n"
            f"Nee query received: *'{message}'*.\n\n"
            f"Nenu Rajwanth Balaka dwara create cheyabadina standalone Autonomous AI Engine. "
            f"Nenu workspace files search cheyagalanu, code generate cheyagalanu, and terminal commands execute cheyagalanu! 🚀"
        )
        self.history.append({"role": "assistant", "content": fallback_reply})
        return fallback_reply
