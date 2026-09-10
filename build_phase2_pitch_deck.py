"""Export the single-source Phase 2 HTML deck and verify its geometry.

Development dependencies: playwright, pypdf, pypdfium2, Pillow.
Run --capture to refresh actual app screenshots using fixture mode only.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from playwright.sync_api import expect, sync_playwright
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "docs_and_presentations/SafePay_MENA_Phase2_Slides.html"
OUTPUT = SOURCE.with_name("SafePay_MENA_Phase2_Pitch_Deck.pdf")
CHECKS = ROOT / "scratch/phase2-deck"


def capture_app(browser):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    env = dict(os.environ, SAFEPAY_ENABLE_LIVE="false", SAFEPAY_DATABASE=":memory:")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        url = f"http://127.0.0.1:{port}"
        for _ in range(60):
            try:
                with urllib.request.urlopen(url + "/api/v1/health", timeout=1) as response:
                    if response.status == 200:
                        break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("Fixture screenshot server did not start")
        page = browser.new_page(viewport={"width": 1440, "height": 1100}, device_scale_factor=2)
        for scenario, heading, filename in [
            ("routine", "Payment approved", "pitch-approve.png"),
            ("scam_transfer", "Payment held", "pitch-hold.png"),
            ("sim_swap", "Payment blocked", "pitch-block.png"),
        ]:
            page.goto(url)
            page.locator("#scenarioSelect").select_option(scenario)
            page.get_by_role("button", name="Review payment", exact=True).click()
            expect(page.locator("#outcomeTitle")).to_have_text(heading)
            target = ROOT / "artifacts" / filename if scenario == "scam_transfer" else CHECKS / filename
            page.locator(".outcome").screenshot(path=str(target))
        request = urllib.request.Request(url + "/api/v1/evaluations", method="POST")
        with urllib.request.urlopen(request, timeout=15) as response:
            evaluation = json.load(response)
        assert evaluation["passed"] == 36 and evaluation["failed"] == 0
        (CHECKS / "evaluation.json").write_text(json.dumps(evaluation, indent=2), encoding="utf-8")
        page.close()
    finally:
        process.terminate()
        process.wait(timeout=15)


def build(capture=False):
    CHECKS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            if capture:
                capture_app(browser)
            page = browser.new_page(viewport={"width": 1600, "height": 1000})
            page.goto(SOURCE.as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
            checks = page.evaluate("""() => [...document.querySelectorAll('.slide')].map((slide, i) => {
                const bounds = slide.getBoundingClientRect();
                const bad = [...slide.querySelectorAll('*')].filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width && r.height && (r.left < bounds.left - 1 || r.right > bounds.right + 1
                        || r.top < bounds.top - 1 || r.bottom > bounds.bottom + 1
                        || el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).display !== 'inline');
                }).map(el => ({tag: el.tagName, class: el.className, text: el.innerText?.slice(0, 80)}));
                const content = slide.querySelector('.content').getBoundingClientRect();
                const footer = slide.querySelector('footer').getBoundingClientRect();
                return {page: i + 1, bad, footerClear: content.bottom <= footer.top - 10,
                    footerGap: Math.round(footer.top - content.bottom)};
            })""")
            (CHECKS / "layout.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
            failures = [item for item in checks if item["bad"] or not item["footerClear"]]
            if failures:
                raise AssertionError(json.dumps(failures, indent=2))
            page.pdf(path=str(OUTPUT), width="1600px", height="900px", print_background=True,
                     prefer_css_page_size=True, display_header_footer=False)
            page.close()
        finally:
            browser.close()
    pdf = PdfReader(OUTPUT)
    assert len(pdf.pages) == 17, f"Unexpected page count: {len(pdf.pages)}"
    for index, page in enumerate(pdf.pages, 1):
        assert len(page.extract_text()) > 120, f"Blank PDF page {index}"
        assert abs(float(page.mediabox.width) / float(page.mediabox.height) - 16 / 9) < 0.01
    document = pdfium.PdfDocument(OUTPUT)
    sheet = Image.new("RGB", (1600, ((len(pdf.pages) + 2) // 3) * 325), "#e5e7eb")
    draw = ImageDraw.Draw(sheet)
    for index in range(len(document)):
        image = document[index].render(scale=1.0).to_pil().convert("RGB")
        image.save(CHECKS / f"slide-{index + 1:02}.png")
        image.thumbnail((512, 288))
        x, y = (index % 3) * 534, (index // 3) * 325
        sheet.paste(image, (x, y))
        draw.text((x + 10, y + 295), f"{index + 1:02}", fill="#17211b")
    sheet.save(CHECKS / "contact-sheet.png")
    print(json.dumps({"pdf": str(OUTPUT), "pages": len(pdf.pages), "layout": "pass",
                      "links": sum(len(page.get("/Annots", [])) for page in pdf.pages),
                      "bytes": OUTPUT.stat().st_size, "preview": str(CHECKS / "contact-sheet.png")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", action="store_true")
    build(parser.parse_args().capture)
