"""Package the committed judging repository and smoke-test the extracted source."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist" / "SafePay_MENA_Source.zip"


def build():
    subprocess.run(["git", "diff", "--exit-code", "HEAD", "--"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    OUTPUT.parent.mkdir(exist_ok=True)
    subprocess.run(["git", "archive", "--format=zip", "--prefix=SafePay-MENA/",
                    f"--output={OUTPUT}", "HEAD"], cwd=ROOT, check=True)
    forbidden = {".git", ".env", "references", "context", "scratch", "workflows",
                 "__pycache__", "token.json", "cookie.txt", "NOTES.md", "image.png"}
    secret_pattern = re.compile(rb"AIza[0-9A-Za-z_-]{35}|[0-9a-f]{10,}msh[a-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")
    with zipfile.ZipFile(OUTPUT) as archive:
        for item in archive.infolist():
            path = Path(item.filename)
            if any(part in forbidden or part.upper().startswith("MENTOR_") for part in path.parts):
                raise ValueError(f"Unintended archive member: {path}")
            if secret_pattern.search(archive.read(item)):
                raise ValueError(f"Possible secret in archive member: {path}")
        with tempfile.TemporaryDirectory(prefix="safepay-source-check-") as directory:
            archive.extractall(directory)
            environment = dict(os.environ, SAFEPAY_ENABLE_LIVE="false", SAFEPAY_DATABASE=":memory:",
                               NOKIA_RAPIDAPI_KEY="", GEMINI_API_KEY="", SAFEPAY_JUDGE_ACCESS_CODE="",
                               PYTHONPATH="")
            environment.pop("SAFEPAY_BROWSER_URL", None)
            subprocess.run([sys.executable, "-m", "pytest", "tests", "--ignore=tests/test_browser.py", "-q"],
                           cwd=Path(directory) / "SafePay-MENA", env=environment, check=True)
    size = OUTPUT.stat().st_size
    if size >= 50_000_000:
        raise ValueError("Source archive exceeds submission limit")
    manifest = {"commit": commit, "file": OUTPUT.name, "bytes": size,
                "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                "extracted_backend_tests": "passed", "secrets_scan": "passed"}
    OUTPUT.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    build()
