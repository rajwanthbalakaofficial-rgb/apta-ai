"""
One-Click App Launcher for apta AI Desktop & Web Application.
"""

import sys
import time
import webbrowser
import threading
from pathlib import Path

def start_server():
    import uvicorn
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, log_level="info")

def main():
    print("==========================================================")
    print("  🤖 Launching apta AI App (ఆప్త AI Desktop Application)")
    print("  Created by Rajwanth Balaka | Standalone Universal Agent")
    print("==========================================================")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    time.sleep(1.5)
    
    app_url = "http://127.0.0.1:8000"
    print(f"\n[+] Opening apta AI App UI at: {app_url}")
    try:
        webbrowser.open(app_url)
    except Exception as e:
        print(f"[!] Could not open browser automatically: {e}")
        print(f"[!] Please open {app_url} manually in your browser.")
        
    print("\n[✓] apta AI App is running! Press Ctrl+C in terminal to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down apta AI App. Bye mama! 👋")
        sys.exit(0)

if __name__ == "__main__":
    main()
