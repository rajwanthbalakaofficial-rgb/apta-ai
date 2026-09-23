# apta AI (ఆప్త AI) 🤖🧠

**apta AI** is an autonomous AI Coding Assistant and Multi-Lingual Biofeedback Companion created for **Rajwanth Balaka** and integrated with the **Udvegadarshini** EEG Neural Stress Detection ecosystem.

---

## 🌟 Key Features

1. **Dual Operating Modes**:
   - 💻 **Coding Assistant Mode**: Code creation, debugging, file system operations (`read_file`, `write_file`, `list_dir`), and shell command execution.
   - 🧠 **Udvegadarshini Biofeedback Companion Mode**: Real-time multi-lingual stress-relief companion supporting **Teluglish (Tanglish)**, English, Telugu, and Hindi.

2. **Udvegadarshini Integration Engine (`server.py`)**:
   - Built-in **FastAPI REST & WebSocket Server** with CORS enabled.
   - Allows the driverless **Udvegadarshini Web Application** (Web Serial / Web BLE) to send live EEG stress metrics (`0-100%`) and band powers (`Delta, Theta, Alpha, Beta, Gamma`).
   - Returns real-time biofeedback suggestions, 4-7-8 breathing triggers, and Solfeggio sound frequency recommendations (432Hz, 528Hz, 396Hz, Binaural Beats).

3. **Tool Calling & Automation**:
   - Seamlessly uses Google Gemini API (`google-genai` SDK) function calling.

---

## 🚀 Quick Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key
Create a `.env` file inside the `apta-ai` directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
MODEL_NAME=gemini-2.5-flash
```

---

## 🖥️ Running apta AI

### A. Run in Terminal CLI Mode (Interactive Chat)
```bash
# Coding Assistant Mode
python main.py --mode coding

# Udvegadarshini Companion Mode
python main.py --mode udvegadarshini
```

### B. Run API Server (For Udvegadarshini Web App Integration)
```bash
python server.py
# Or using uvicorn directly:
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
The server will start at `http://localhost:8000` with full CORS support.

---

## 🔗 Connecting to Udvegadarshini Web App

Inside your Udvegadarshini JavaScript codebase (`Udvegadarshini-App`), send live telemetry or chat messages to `apta AI`:

```javascript
// Example: Sending Chat & Live Stress Score to apta AI
async function sendToAptaAI(userMessage, eegStressScore) {
    const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: userMessage,
            stress_score: eegStressScore,
            state: "High Stress",
            language: "teluglish"
        })
    });
    const data = await response.json();
    console.log("apta AI Reply:", data.reply);
    console.log("Recommendation:", data.recommendation);
}
```

---

## 📂 Project Structure

```
apta-ai/
├── config.py         # System prompts and environment loader
├── tools.py          # File system, command execution, and biofeedback tools
├── agent.py          # Core AptaAgent engine & Gemini client wrapper
├── server.py         # FastAPI integration server for Udvegadarshini Web App
├── main.py           # Interactive Rich CLI application
├── requirements.txt  # Python package dependencies
├── test_agent.py     # Verification & automated test suite
└── README.md         # Project documentation
```

---
*Developed with ❤️ for Rajwanth Balaka & Udvegadarshini Neural System.*
