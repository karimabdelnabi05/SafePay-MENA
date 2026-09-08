import json
import pathlib
import sys
import time
from notebooklm_mcp.api_client import NotebookLMClient

def get_client(auth):
    return NotebookLMClient(
        cookies=auth['cookies'],
        csrf_token=auth.get('csrf_token', ''),
        session_id=auth.get('session_id', '')
    )

def main():
    auth_path = pathlib.Path.home() / '.notebooklm-mcp' / 'auth.json'
    if not auth_path.exists():
        print("Error: auth.json not found")
        sys.exit(1)
        
    auth = json.loads(auth_path.read_text(encoding='utf-8'))
    notebook_id = '9f9ae107-88d6-4156-9f76-fedcc95d4260' # MENA Ignite Hackathon
    
    queries = [
        ("CAMARA APIs & Telco Monetization",
         "What specific details do the sources contain regarding CAMARA Open Gateway APIs (Number Verification, SIM Swap, Device Status, Know Your Customer Match, Scam Signal), Nokia Network as Code, operator commercial models, pricing per API call, latency, and integration with banking rails?"),
         
        ("Regulatory Directives & SAMA/CBUAE/CBE Anti-Fraud Compliance",
         "What are the specific regulatory mandates, SAMA 2026 Counter-Fraud Framework rules, instant transfer limits (such as 2,500 SAR and 20,000 SAR), liability shift between telecom and banks, and compliance audit trail requirements in the sources?")
    ]
    
    output_file = pathlib.Path("NOTEBOOKLM_RESEARCH_SYNTHESIS.md")
    
    for idx, (title, q) in enumerate(queries, 2):
        print(f"[{idx}/3] Executing query: {title}...")
        success = False
        for attempt in range(1, 4):
            try:
                print(f"  Attempt {attempt}/3...")
                client = get_client(auth)
                res = client.query(notebook_id, q, timeout=180.0)
                if client._client:
                    client._client.close()
                    
                if res and "answer" in res:
                    answer = res["answer"]
                    print(f"  -> Success! Received {len(answer)} characters.")
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"\n\n## {idx}. {title}\n\n")
                        f.write(f"**Research Prompt:** *{q}*\n\n")
                        f.write(answer + "\n\n")
                        f.write("---\n\n")
                    success = True
                    break
                else:
                    print(f"  -> Empty response on attempt {attempt}: {res}")
            except Exception as e:
                print(f"  -> Error on attempt {attempt}: {e}")
                time.sleep(5)
                
        if not success:
            print(f"Failed to fetch {title} after 3 attempts.")
            
        time.sleep(3)
        
    print(f"\nProcess finished. Updated {output_file.resolve()}")

if __name__ == "__main__":
    main()
