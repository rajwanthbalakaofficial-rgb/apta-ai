"""
FastAPI Server for apta AI - Providing REST API endpoints for Udvegadarshini Web Application integration.
"""

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import AptaAgent
from tools import get_stress_recommendation

app = FastAPI(
    title="apta AI Server",
    description="API Server for apta AI & Udvegadarshini Multi-Lingual Biofeedback Integration",
    version="1.0.0"
)

# Enable CORS for Web Browsers (Udvegadarshini PWA / Web App)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows GitHub Pages and Localhost web apps
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agent in Udvegadarshini Wellness Companion mode
udvega_agent = AptaAgent(mode="udvegadarshini")


class ChatRequest(BaseModel):
    message: str = Field(..., example="Mama ippudu naaku tension ga undhi")
    stress_score: Optional[float] = Field(default=0.0, example=65.5)
    state: Optional[str] = Field(default="Normal", example="High Stress")
    band_powers: Optional[Dict[str, float]] = Field(default_factory=dict)
    language: Optional[str] = Field(default="teluglish", example="teluglish")


class EEGSyncRequest(BaseModel):
    stress_score: float = Field(..., example=72.0)
    state: Optional[str] = Field(default="Elevated Stress")
    delta: Optional[float] = 0.0
    theta: Optional[float] = 0.0
    alpha: Optional[float] = 0.0
    beta: Optional[float] = 0.0
    gamma: Optional[float] = 0.0


@app.get("/")
def read_root():
    return {
        "status": "online",
        "name": "apta AI Server",
        "description": "Udvegadarshini EEG Neural Biofeedback & AI Companion Engine",
        "mode": "udvegadarshini",
        "gemini_status": "configured" if udvega_agent.is_configured() else "api_key_missing"
    }


@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for Udvegadarshini Web App.
    Accepts user text message along with live EEG stress score and returns empathetic AI response.
    """
    try:
        stress_ctx = {
            "stress_score": request.stress_score,
            "state": request.state,
            "band_powers": request.band_powers
        }
        
        reply = udvega_agent.send_message(request.message, stress_context=stress_ctx)
        recommendation = get_stress_recommendation(request.stress_score, request.state)
        
        return {
            "status": "success",
            "reply": reply,
            "recommendation": recommendation,
            "stress_score": request.stress_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/eeg-sync")
def eeg_sync_endpoint(request: EEGSyncRequest):
    """
    Telemetry sync endpoint called by Udvegadarshini Web Serial/BLE engine.
    Returns real-time biofeedback suggestions based on EEG band powers and stress score.
    """
    recommendation = get_stress_recommendation(request.stress_score, request.state)
    
    suggested_audio = "528Hz Solfeggio Transformation"
    if request.stress_score <= 30.0:
        suggested_audio = "432Hz Deep Relaxation Soundscape"
    elif request.stress_score >= 70.0:
        suggested_audio = "6Hz Theta Binaural Beats + Gentle Rain"
        
    return {
        "status": "success",
        "stress_score": request.stress_score,
        "state": request.state,
        "recommendation": recommendation,
        "suggested_audio": suggested_audio,
        "breathing_cycle": "4-7-8 Biofeedback Breathing" if request.stress_score > 50.0 else "Normal"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
