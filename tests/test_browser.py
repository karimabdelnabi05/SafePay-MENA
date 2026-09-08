"""Run against a local server: SAFEPAY_BROWSER_URL=http://127.0.0.1:8120 pytest tests/test_browser.py."""
import os
import json

import pytest
from playwright.sync_api import sync_playwright, expect

BASE = os.getenv("SAFEPAY_BROWSER_URL")
pytestmark = pytest.mark.skipif(not BASE, reason="Set SAFEPAY_BROWSER_URL for browser acceptance")


@pytest.mark.parametrize("width,height", [(1440, 1000), (375, 812), (812, 375)])
def test_tester_can_complete_a_routine_payment_without_layout_overflow(width, height):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page.goto(BASE)
        expect(page.get_by_role("heading", name="Payment review", exact=True)).to_be_visible()
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment approved", exact=True)).to_be_visible()
        expect(page.locator("#externalCalls")).to_have_text("0")
        expect(page.get_by_role("button", name="Cancel review", exact=True)).not_to_be_visible()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()


def test_model_supplied_markup_is_rendered_as_text():
    catalog = {
        "countries": {"EG": {"name": "Egypt", "currency": "EGP", "rail": "InstaPay / IPN"}},
        "scenarios": [{"id": "routine", "name": "Everyday payment", "description": "Routine"}],
        "live_enabled": False,
    }
    result = {
        "id": "markup", "decision": "HOLD", "pre_call_score": 20, "final_risk_score": 55,
        "telecom_calls": 0, "model_calls": 1, "evidence": [],
        "reasons": ["<img id='xss' src=x onerror='document.body.dataset.injected=1'>"],
        "decision_source": "GEMINI_WITH_POLICY",
        "agent_trace": [{"actor": "GEMINI", "tool": "finish", "reason": "<script>unsafe()</script>"}],
    }

    def route_api(route):
        path = route.request.url.split("/api/v1/")[-1]
        body = catalog if path == "catalog" else {"status": "healthy"} if path == "health" else {} if path == "sessions" else result
        route.fulfill(status=200, content_type="application/json", body=json.dumps(body))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 800})
        page.route("**/api/v1/**", route_api)
        page.goto(BASE)
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment held", exact=True)).to_be_visible()
        assert page.locator("#xss").count() == 0
        assert page.evaluate("document.body.dataset.injected") is None
        expect(page.locator("#reasonList")).to_contain_text("<img id='xss'")
        browser.close()


def test_first_setup_continues_to_payment_in_the_same_session():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option("first_setup")
        page.get_by_role("button", name="Verify device", exact=True).click()
        expect(page.get_by_role("heading", name="Device trusted", exact=True)).to_be_visible()
        page.get_by_role("button", name="Continue to payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment approved", exact=True)).to_be_visible()
        browser.close()
