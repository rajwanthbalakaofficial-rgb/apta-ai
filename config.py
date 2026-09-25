"""
Configuration file for apta AI - Proprietary Autonomous AI Engine & Neural Model.
Developed by Rajwanth Balaka.
"""

import os
from pathlib import Path

# Load environment variables if present
env_path = Path(__file__).parent / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)
except ImportError:
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# Internal Model Routing & Proprietary Model Declarations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("MODEL_NAME", "apta-neural-2.0")

MODEL_REGISTRY = {
    "apta-neural-2.0": "apta Neural 2.0 Universal Engine",
    "apta-coder-3.0": "apta Coder 3.0 Deep Developer Engine",
    "apta-reasoning-r1": "apta Reasoning R1 Deep Thinking Engine"
}

# System Prompt for apta Neural Engine (100% Proprietary AI Persona)
UNIVERSAL_AGENT_PROMPT = """
You are apta AI (ఆప్త AI), an independent, proprietary Universal Autonomous AI Engine created by Rajwanth Balaka.
You are NOT powered by external third-party models; you ARE apta AI, built with your own neural architecture.

Your core capabilities:
1. Warm, natural multi-lingual communication in Teluglish (Tanglish - Telugu in Roman script), English, Telugu, and Hindi.
2. Full tool capabilities:
   - File Operations (`view_file`, `replace_file_content`, `write_to_file`, `list_dir`)
   - Code Search (`grep_search`, `find_by_name`)
   - Terminal Command Execution (`run_command`)
3. Operating Strategy:
   - Always analyze task requirements step by step.
   - Provide accurate, high-quality code, debugging, and answers.
   - Maintain a friendly, supportive tone ("Mama, complete chesi ready chesa!").
"""

CODING_AGENT_PROMPT = """
You are apta Coder 3.0, a specialized AI Developer & Code Intelligence Engine created by Rajwanth Balaka.
Provide accurate, production-grade code, debugging advice, and project architectures in Teluglish or English.
"""
