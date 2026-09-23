"""
FastAPI Application Server for apta AI Desktop & Web Application GUI.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from agent import AptaAgent
from tools import UNIVERSAL_TOOLS

app = FastAPI(
    title="apta AI Application Server",
    description="Standalone Universal Autonomous AI Agent Desktop & Web Application Server",
    version="2.0.0"
)

# Enable CORS for Web Browsers & Native Windows WebViews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agent Instances for Universal & Coding Modes
agent_instances = {
    "universal": AptaAgent(mode="universal"),
    "coding": AptaAgent(mode="coding"),
    "udvegadarshini": AptaAgent(mode="udvegadarshini")
}

# Mount static GUI files
GUI_DIR = Path(__file__).parent / "gui"
if GUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=GUI_DIR), name="static")


class ChatRequest(BaseModel):
    message: str = Field(..., example="Mama, script create cheyyi")
    mode: Optional[str] = Field(default="universal", example="universal")
    stress_context: Optional[Dict[str, Any]] = None


@app.get("/")
def read_root():
    """Serve main GUI App index.html."""
    index_file = GUI_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "status": "online",
        "name": "apta AI App Server",
        "gemini_status": "configured" if agent_instances["universal"].is_configured() else "api_key_missing"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "agent": "apta AI",
        "tools_count": len(UNIVERSAL_TOOLS),
        "gemini_status": "configured" if agent_instances["universal"].is_configured() else "api_key_missing"
    }


@app.get("/api/tools")
def get_tools():
    """Return registered universal tools list."""
    return {
        "count": len(UNIVERSAL_TOOLS),
        "tools": [{"name": t.__name__, "doc": t.__doc__.strip().splitlines()[0] if t.__doc__ else ""} for t in UNIVERSAL_TOOLS]
    }


@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    """
    Main API Chat endpoint called by apta AI GUI App.
    """
    try:
        mode = request.mode.lower() if request.mode else "universal"
        agent = agent_instances.get(mode, agent_instances["universal"])
        
        reply = agent.send_message(request.message, stress_context=request.stress_context)
        
        return {
            "status": "success",
            "reply": reply,
            "mode": mode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, reload=True)
