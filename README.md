# apta AI (ఆప్త AI) 🤖🌐

**apta AI** is a standalone, open-source **Universal Autonomous AI Agent & Pair Programming Assistant** created by **Rajwanth Balaka**. Powered by the Google Gemini API (`google-genai` SDK), it operates across software development, project management, file editing, code search, terminal command execution, and web research.

---

## 🌟 Key Features

1. **Universal Autonomous Agent Capabilities**:
   - 💻 **Pair Programming & Code Editing**: Full multi-file awareness, pattern matching (`find_files`, `search_files`), and single-block editing (`replace_in_file`).
   - ⚡ **Terminal Execution**: Runs shell, PowerShell, and CMD commands with automatic output capturing.
   - 🌐 **Web Content Research**: Fetches public web content and API data.
   - 📁 **File & Directory Management**: View, list, search, and edit project files.

2. **Multi-Lingual Natural Conversation Engine**:
   - Primary conversation style: **Teluglish (Tanglish - Telugu written in Roman script)**, alongside English, Telugu, and Hindi support.

3. **Interactive Rich CLI Terminal (`main.py`)**:
   - Feature-rich terminal interface with color highlighting, markdown rendering, and interactive mode switching (`/mode universal`, `/mode coding`, `/tools`, `/clear`).

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

## 🖥️ Usage Guide

### A. Run Interactive CLI Agent
```bash
# Launch Universal Agent CLI
python main.py

# Switch to Coding Mode
python main.py --mode coding
```

### B. Interactive CLI Commands
- `/tools` : Display all registered universal tools.
- `/mode universal` : Switch to Universal Autonomous Agent Mode.
- `/mode coding` : Switch to Developer Assistant Mode.
- `/clear` : Clear terminal screen.
- `exit` / `quit` : Exit session.

---

## 📂 Project Architecture

```
apta-ai/
├── config.py         # System prompts and environment loader
├── tools.py          # Universal tool suite (Files, Search, Shell, Web)
├── agent.py          # Core AptaAgent engine & Gemini client wrapper
├── main.py           # Interactive Rich CLI application
├── requirements.txt  # Dependencies (google-genai, rich, python-dotenv)
├── test_agent.py     # Automated test suite
├── demo_test.py      # Quick demo test script
└── README.md         # Project documentation
```

---
*Created with ❤️ by Rajwanth Balaka.*
