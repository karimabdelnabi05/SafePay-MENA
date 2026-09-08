import re
import urllib.parse
import json
import pathlib
import time

def parse_curl_to_auth(curl_text: str):
    # Extract URL
    url_match = re.search(r"curl\s+['\"]([^'\"]+)['\"]", curl_text)
    url = url_match.group(1) if url_match else ""

    # Extract Cookie
    cookie_match = re.search(r"-H\s+['\"][Cc]ookie:\s*([^'\"]+)['\"]", curl_text)
    cookie_str = cookie_match.group(1) if cookie_match else ""

    # If curl_text is already just cookies:
    if not cookie_str and "=" in curl_text and "curl" not in curl_text:
        cookie_str = curl_text.strip()

    # Extract Body (--data-raw or -d or --data)
    body_match = re.search(r"--data(?:-raw)?\s+['\"]([^'\"]+)['\"]", curl_text)
    body = body_match.group(1) if body_match else ""

    csrf_token = ""
    if body and "at=" in body:
        at_part = body.split("at=")[1].split("&")[0]
        csrf_token = urllib.parse.unquote(at_part)

    session_id = ""
    if url and "f.sid=" in url:
        sid_part = url.split("f.sid=")[1].split("&")[0]
        session_id = urllib.parse.unquote(sid_part)

    cookies = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip()

    print(f"Parsed {len(cookies)} cookies.")
    print(f"CSRF Token: {'Found (' + csrf_token[:15] + '...)' if csrf_token else 'Not found'}")
    print(f"Session ID: {session_id if session_id else 'Not found'}")

    if cookies:
        auth_dir = pathlib.Path.home() / ".notebooklm-mcp"
        auth_dir.mkdir(parents=True, exist_ok=True)
        auth_file = auth_dir / "auth.json"
        auth_data = {
            "cookies": cookies,
            "csrf_token": csrf_token,
            "session_id": session_id,
            "extracted_at": time.time()
        }
        with open(auth_file, "w", encoding="utf-8") as f:
            json.dump(auth_data, f, indent=2)
        print(f"Saved to {auth_file}!")
        return True
    return False

if __name__ == '__main__':
    p = pathlib.Path("cookie.txt")
    if p.exists():
        parse_curl_to_auth(p.read_text(encoding="utf-8", errors="ignore"))
