"""
SafePay MENA - One-Command Application Launcher
Runs FastAPI backend, CAMARA mock gateway, and interactive cyber-shield dashboard on port 8000.
"""

import sys
import uvicorn

def main():
    print("=" * 70)
    print("  SafePay MENA - AI Fraud Shield for Instant Payments")
    print("  GSMA MENA Ignite Hackathon (Phase 2 Prototype)")
    print("=" * 70)
    print("\n[+] Dashboard URL: http://127.0.0.1:8000")
    print("[+] Interactive API Docs: http://127.0.0.1:8000/docs")
    print("[+] Real-time WebSocket: ws://127.0.0.1:8000/ws/live-feed")
    print("\nPress Ctrl+C to stop the server.\n")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
