"""
SafePay MENA - Live Nokia Network as Code API Diagnostic Tool
Executes an authentic, real-time HTTP probe to Nokia Network as Code servers and prints raw wire telemetry.
"""

import os
import sys
import time
from pathlib import Path
import httpx

# Load .env file
def load_env():
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                elif ":" in line:
                    k, v = line.split(":", 1)
                else:
                    continue
                k = k.strip()
                v = v.strip().strip("\"'")
                if k and v and k not in os.environ:
                    os.environ[k] = v

load_env()

api_key = os.getenv("NOKIA_RAPIDAPI_KEY") or os.getenv("Netwrok_as_code_api_key") or ""

print("=" * 80)
print(" SAFEPAY MENA: LIVE NOKIA NETWORK AS CODE API PROBE")
print("=" * 80)

if not api_key:
    print("[ERROR] No Nokia API key found in .env file.")
    sys.exit(1)

masked_key = api_key[:8] + "..." + api_key[-4:]
print(f"[*] API Key Detected: {masked_key}")
print(f"[*] Target Host: network-as-code.p.rapidapi.com")
print(f"[*] CAMARA Standard: GSMA Open Gateway v0.3.0")
print("-" * 80)

# Probe 1: Direct Raw HTTP Wire Call via httpx
url = "https://network-as-code.p.rapidapi.com/passthrough/camara/v1/sim-swap/sim-swap/v0/check"
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "network-as-code.p.rapidapi.com",
    "Content-Type": "application/json",
    "User-Agent": "SafePayMENA-LiveWire/1.0"
}
payload = {
    "phoneNumber": "+966501234567",
    "maxAge": 240
}

print(f"\n[STEP 1] Dispatching Live HTTP POST across internet...")
print(f"  URL:     {url}")
print(f"  Headers: x-rapidapi-host={headers['x-rapidapi-host']}, x-rapidapi-key={masked_key}")
print(f"  Payload: {payload}")

start_time = time.perf_counter()
try:
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url, json=payload, headers=headers)
        latency_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        
        print(f"\n[STEP 2] Received Live Response from Nokia Gateway ({latency_ms} ms):")
        print(f"  HTTP Status:      {response.status_code}")
        print(f"  Cloud Region:     {response.headers.get('x-rapidapi-region', 'N/A')}")
        print(f"  Server Engine:    {response.headers.get('server', 'N/A')}")
        print(f"  RapidAPI Req ID:  {response.headers.get('x-rapidapi-request-id', 'N/A')}")
        print(f"  Response Body:    {response.text}")
        
        print("-" * 80)
        print("[DIAGNOSTIC VERDICT]:")
        if response.status_code == 200:
            print("  >>> LIVE CARRIER SANDBOX CONNECTED AND FULLY OPERATIONAL!")
            print(f"  Data: {response.json()}")
        elif response.status_code == 403:
            print("  >>> KEY AUTHENTICATED BY RAPIDAPI, BUT FREE SUBSCRIPTION PENDING.")
            print("  Explanation: RapidAPI requires clicking 'Subscribe to Free Plan' on rapidapi.com")
            print("  for Nokia Network as Code before API calls are authorized.")
            print("  Direct Link: https://rapidapi.com/nokia-network-as-code/api/network-as-code")
        elif response.status_code == 429:
            print("  >>> RATE LIMIT OR PLAN EXCEEDED.")
        else:
            print(f"  >>> Gateway responded with status {response.status_code}.")

except Exception as e:
    print(f"[ERROR] Connection failed: {e}")

# Probe 2: Test via official Nokia Python SDK
print("\n" + "=" * 80)
print(" [STEP 3] Testing via Official Nokia Python SDK (network_as_code)")
print("=" * 80)
try:
    from network_as_code import NetworkAsCodeApi
    print("[*] Official Nokia SDK imported successfully.")
    sdk_client = NetworkAsCodeApi(
        api_key=api_key,
        rapidapi_host="network-as-code.p.rapidapi.com",
        base_url="https://network-as-code.p.rapidapi.com"
    )
    print("[*] Client initialized targeting Nokia Network as Code gateway.")
    try:
        sdk_res = sdk_client.sim_swap.check(phone_number="+966501234567", max_age=240)
        print("[*] SDK Call Result:", sdk_res)
    except Exception as sdk_err:
        print("[*] SDK Call caught carrier response:")
        print(f"    {sdk_err}")
except ImportError:
    print("[!] Nokia SDK not found in environment.")

print("\n" + "=" * 80)
print(" DIAGNOSTIC COMPLETE")
print("=" * 80)
