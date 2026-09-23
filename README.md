# apta AI (ఆప్త AI) 🤖🌐

**apta AI** is a standalone, open-source **Universal Autonomous AI Agent & Pair Programming Desktop Application** created by **Rajwanth Balaka**. Powered by the Google Gemini API (`google-genai` SDK), it features a modern Glassmorphism dark theme user interface, live tool execution tracking, pair programming, code search, file editing, terminal execution, and web research.

---

## 🌟 Key Features

1. **Modern Glassmorphism Desktop & Web App UI**:
   - Built-in responsive Glassmorphism dark mode UI.
   - Interactive mode switcher (`Universal Agent` / `Coding Developer`).
   - Live tool activity visualizer.
   - Rich markdown code rendering with dark mode syntax styling.

2. **Universal Autonomous Agent Capabilities**:
   - 💻 **Pair Programming & Code Editing**: Full multi-file awareness, pattern matching (`find_files`, `search_files`), and single-block editing (`replace_in_file`).
   - ⚡ **Terminal Execution**: Runs shell, PowerShell, and CMD commands with automatic output capturing (`execute_command`).
   - 🌐 **Web Content Research**: Fetches public web content and API data (`fetch_web_content`).
   - 📁 **File & Directory Management**: View, list, search, and edit project files (`read_file`, `write_file`, `list_dir`).

3. **Multi-Lingual Natural Conversation Engine**:
   - Primary conversation style: **Teluglish (Tanglish - Telugu written in Roman script)**, alongside English, Telugu, and Hindi support.

---

## 🚀 Quick Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/rajwanthbalakaofficial-rgb/apta-ai.git
cd apta-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
MODEL_NAME=gemini-2.5-flash
```

---

## 🖥️ Launching the apta AI App

### 🎯 Option A: Launch 1-Click Desktop App (Recommended)
```bash
python run_app.py
```
This automatically starts the application server and opens the **apta AI App Window** in your browser (`http://127.0.0.1:8000`)!

### 💻 Option B: Run Interactive Terminal CLI
```bash
python main.py
```

---

## 📂 Project Architecture

```
apta-ai/
├── gui/              # Glassmorphism App UI (index.html, style.css, app.js)
├── run_app.py        # 1-Click App Launcher
├── app_server.py     # FastAPI Desktop App Server
├── config.py         # System prompts and environment loader
├── tools.py          # Universal tool suite (Files, Search, Shell, Web)
├── agent.py          # Core AptaAgent engine & Gemini client wrapper
├── main.py           # Interactive Rich CLI application
├── requirements.txt  # Dependencies (google-genai, rich, fastapi, uvicorn)
├── test_agent.py     # Automated test suite
├── demo_test.py      # Quick demo test script
└── README.md         # Project documentation
```

---
*Created with ❤️ by Rajwanth Balaka.*
