"""
Core AptaAgent class wrapping Google Gemini API, universal tool execution, conversation memory, and Udvegadarshini integration.
"""

import sys
from typing import List, Dict, Any, Optional

from config import (
    GEMINI_API_KEY, 
    DEFAULT_MODEL, 
    UNIVERSAL_AGENT_PROMPT,
    CODING_AGENT_PROMPT, 
    UDVEGADARSHINI_PROMPT
)
from tools import UNIVERSAL_TOOLS, get_stress_recommendation

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class AptaAgent:
    """
    apta AI Universal Agent Engine.
    Supports 'universal', 'coding', and 'udvegadarshini' operating modes.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        mode: str = "universal"  # 'universal', 'coding', or 'udvegadarshini'
    ):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        self.mode = mode.lower()
        
        if self.mode == "udvegadarshini":
            self.system_instruction = UDVEGADARSHINI_PROMPT
        elif self.mode == "coding":
            self.system_instruction = CODING_AGENT_PROMPT
        else:
            self.mode = "universal"
            self.system_instruction = UNIVERSAL_AGENT_PROMPT
        
        self.client = None
        self.history: List[Dict[str, str]] = []
        
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Google GenAI Client if API key is present."""
        if not GENAI_AVAILABLE:
            return
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Warning] Failed to initialize Gemini Client: {e}", file=sys.stderr)

    def is_configured(self) -> bool:
        """Check if GenAI client is properly configured with an API key."""
        return self.client is not None

    def send_message(
        self,
        message: str,
        stress_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Send a user message to apta AI and return response.
        """
        full_prompt = message
        if stress_context:
            score = stress_context.get("stress_score", 0.0)
            state = stress_context.get("state", "Normal")
            bands = stress_context.get("band_powers", {})
            bio_summary = get_stress_recommendation(score, state)
            
            full_prompt = (
                f"[Udvegadarshini Live Telemetry]\n"
                f"- Stress Score: {score:.1f}%\n"
                f"- State: {state}\n"
                f"- Band Powers: {bands}\n"
                f"- Biofeedback Suggestion: {bio_summary}\n\n"
                f"User Message: {message}"
            )

        self.history.append({"role": "user", "content": full_prompt})

        if self.is_configured():
            try:
                config = types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    tools=UNIVERSAL_TOOLS
                )
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt,
                    config=config
                )
                
                reply = response.text or "Mama, request process chesanu but response text empty ga undhi."
                self.history.append({"role": "assistant", "content": reply})
                return reply
            except Exception as e:
                error_msg = f"Mama, Gemini API call lo issue vachindhi: {str(e)}"
                self.history.append({"role": "assistant", "content": error_msg})
                return error_msg
        else:
            fallback_reply = (
                "Arey mama! `GEMINI_API_KEY` set avvaledu.\n"
                "Please set `GEMINI_API_KEY` in `apta-ai/.env` file or environment variables.\n\n"
                f"Eppatikainaa nee query received: '{message}'.\n"
                "Once API key add chesthe, full Gemini AI capabilities tho work avuthundi!"
            )
            self.history.append({"role": "assistant", "content": fallback_reply})
            return fallback_reply
