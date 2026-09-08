"""Run the SafePay MENA prototype locally."""

import uvicorn

def main():
    print("=" * 70)
    print("  SafePay MENA - Adaptive Telecom Evidence")
    print("  GSMA MENA Ignite Hackathon - Phase 2 Prototype")
    print("=" * 70)
    print("\n[+] Dashboard URL: http://127.0.0.1:8000")
    print("[+] Interactive API Docs: http://127.0.0.1:8000/docs")
    print("[+] Fixture mode is available without provider credentials")
    print("[+] Nokia sandbox mode requires SAFEPAY_ENABLE_LIVE=true and both API keys")
    print("\nPress Ctrl+C to stop the server.\n")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
