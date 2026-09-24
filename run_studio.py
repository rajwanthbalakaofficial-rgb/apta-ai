"""
One-Click Launcher for apta AI Antigravity Twin Studio Engine.
"""

import sys
import time
import webbrowser
import threading

def start_server():
    import uvicorn
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, log_level="info")

def main():
    print("==========================================================")
    print("  ⚡ Launching apta AI Antigravity Twin Studio Engine")
    print("  Created by Rajwanth Balaka | Exact Antigravity Clone")
    print("==========================================================")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    time.sleep(1.5)
    
    studio_url = "http://127.0.0.1:8000"
    print(f"\n[+] Opening Antigravity Twin Studio at: {studio_url}")
    try:
        webbrowser.open(studio_url)
    except Exception as e:
        print(f"[!] Please open {studio_url} manually in your browser.")
        
    print("\n[✓] Antigravity Twin Studio is live! Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down Antigravity Studio. Bye mama! 👋")
        sys.exit(0)

if __name__ == "__main__":
    main()
