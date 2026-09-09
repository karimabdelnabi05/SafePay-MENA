"""Run against a local server: SAFEPAY_BROWSER_URL=http://127.0.0.1:8120 pytest tests/test_browser.py."""
import json
import os

import pytest
from playwright.sync_api import expect, sync_playwright

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
        expect(page.locator("#evidenceBody")).to_contain_text("No network evidence was returned")
        expect(page.locator("#evidenceBody")).not_to_contain_text("routine payment")
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


def test_failed_enrollment_offers_an_honest_device_verification_retry():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option("enrollment_outage")
        page.get_by_role("button", name="Verify device", exact=True).click()
        expect(page.get_by_role("heading", name="Verification incomplete", exact=True)).to_be_visible()
        retry = page.get_by_role("button", name="Retry device verification", exact=True)
        expect(retry).to_be_visible()
        retry.click()
        expect(page.get_by_role("heading", name="Verification incomplete", exact=True)).to_be_visible()
        expect(retry).to_be_visible()
        browser.close()


@pytest.mark.parametrize("scenario,heading", [
    ("identity_mismatch", "Payment held"),
    ("scam_transfer", "Payment held"),
    ("sim_swap", "Payment blocked"),
    ("card_misuse", "Payment blocked"),
    ("combined_attack", "Payment blocked"),
    ("legitimate_travel", "Payment approved"),
    ("velocity", "Payment held"),
    ("provider_outage", "Verification incomplete"),
])
def test_tester_can_inspect_each_payment_outcome(scenario, heading):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option(scenario)
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name=heading, exact=True)).to_be_visible()
        expect(page.locator("#evidenceBody tbody tr")).not_to_have_count(0)
        expect(page.locator("#externalCalls")).to_have_text("0")
        expect(page.locator("#reasonList li")).not_to_have_count(0)
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()


def test_tester_can_cancel_a_held_payment():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option("scam_transfer")
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment held", exact=True)).to_be_visible()
        page.get_by_role("button", name="Cancel review", exact=True).click()
        expect(page.get_by_role("heading", name="Review cancelled", exact=True)).to_be_visible()
        expect(page.get_by_role("button", name="Cancel review", exact=True)).not_to_be_visible()
        browser.close()


def test_expired_session_retry_starts_a_fresh_session():
    calls = {"sessions": 0, "payments": 0}
    catalog = {
        "countries": {"EG": {"name": "Egypt", "currency": "EGP", "rail": "InstaPay / IPN"}},
        "scenarios": [{"id": "routine", "name": "Everyday payment", "description": "Routine"}],
        "live_enabled": False,
    }
    approved = {
        "id": "fresh", "decision": "APPROVE", "pre_call_score": 0, "final_risk_score": 0,
        "telecom_calls": 0, "model_calls": 0, "evidence": [], "reasons": [],
        "decision_source": "LOCAL_SCREENING",
    }

    def route_api(route):
        path = route.request.url.split("/api/v1/")[-1]
        if path == "catalog":
            body, status = catalog, 200
        elif path == "health":
            body, status = {"status": "healthy"}, 200
        elif path == "sessions":
            calls["sessions"] += 1
            body, status = {}, 200
        else:
            calls["payments"] += 1
            fresh_session = calls["sessions"] >= 2
            body = approved if fresh_session else {"detail": "Demo session expired"}
            status = 200 if fresh_session else 401
        route.fulfill(status=status, content_type="application/json", body=json.dumps(body))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 800})
        page.route("**/api/v1/**", route_api)
        page.goto(BASE)
        review = page.get_by_role("button", name="Review payment", exact=True)
        review.click()
        expect(page.locator("#formError")).to_contain_text("expired")
        review.click()
        expect(page.get_by_role("heading", name="Payment approved", exact=True)).to_be_visible()
        assert calls == {"sessions": 2, "payments": 2}
        browser.close()


def test_delayed_cancellation_cannot_overwrite_a_new_context():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option("scam_transfer")
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment held", exact=True)).to_be_visible()
        page.evaluate("""
          const originalFetch = window.fetch.bind(window);
          window.fetch = (url, options) => String(url).includes('/cancel')
            ? new Promise((resolve) => setTimeout(() => resolve(new Response(JSON.stringify({
                id: 'old', decision: 'CANCELLED', reasons: [], evidence: [],
                telecom_calls: 0, model_calls: 0, decision_source: 'LOCAL_SCREENING'
              }), {status: 200, headers: {'Content-Type': 'application/json'}})), 500))
            : originalFetch(url, options);
        """)
        page.get_by_role("button", name="Cancel review", exact=True).click()
        page.locator("#scenarioSelect").select_option("sim_swap")
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment blocked", exact=True)).to_be_visible()
        page.wait_for_timeout(700)
        expect(page.get_by_role("heading", name="Payment blocked", exact=True)).to_be_visible()
        browser.close()


def test_tester_can_run_the_visible_quality_gate():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.get_by_role("button", name="Run 36-case evaluation", exact=True).click()
        expect(page.locator("#evaluationResult")).to_contain_text("36 passed")
        expect(page.locator("#evaluationResult")).to_contain_text("0 failed")
        browser.close()


def test_switching_scenario_or_market_clears_stale_decision_state():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 900}, reduced_motion="reduce")
        page.goto(BASE)
        page.locator("#scenarioSelect").select_option("sim_swap")
        expect(page.locator("#channelSelect")).to_have_value("INSTANT_PAYMENT")
        page.get_by_role("button", name="Review payment", exact=True).click()
        expect(page.get_by_role("heading", name="Payment blocked", exact=True)).to_be_visible()

        page.locator("#scenarioSelect").select_option("card_misuse")
        expect(page.get_by_role("heading", name="Ready for review", exact=True)).to_be_visible()
        expect(page.locator("#channelSelect")).to_have_value("CARD_CHECKOUT")
        expect(page.locator("#preScore")).to_have_text("-")
        expect(page.locator("#evidenceBody")).to_contain_text("No network evidence requested")

        page.get_by_role("button", name="Saudi Arabia", exact=True).click()
        expect(page.locator("#currencyHelp")).to_have_text("SAR")
        expect(page.locator("#railContext")).to_contain_text("sarie")
        page.get_by_role("button", name="United Arab Emirates", exact=True).click()
        expect(page.locator("#currencyHelp")).to_have_text("AED")
        expect(page.locator("#railContext")).to_contain_text("Aani")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
