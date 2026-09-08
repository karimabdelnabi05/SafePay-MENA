"""Build the evidence-backed SafePay MENA Phase 2 pitch deck."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "docs_and_presentations" / "SafePay_MENA_Phase2_Pitch_Deck.pdf"
SCREENSHOT = ROOT / "artifacts" / "safepay-desktop.png"
WIDTH, HEIGHT = landscape(letter)

INK = HexColor("#17211B")
MUTED = HexColor("#506057")
BRAND = HexColor("#086C4F")
BRAND_DARK = HexColor("#064B39")
GOLD = HexColor("#D69D16")
BG = HexColor("#F4F6F3")
SURFACE = HexColor("#FFFFFF")
SOFT = HexColor("#E7F5EE")
LINE = HexColor("#CBD5CE")
WARN = HexColor("#FFF4D4")
RED = HexColor("#A12B2B")


def wrapped(text, font, size, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Deck:
    def __init__(self, output):
        self.canvas = canvas.Canvas(str(output), pagesize=(WIDTH, HEIGHT))
        self.page = 0

    def begin(self, title, kicker=None):
        self.page += 1
        c = self.canvas
        c.setFillColor(BG)
        c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
        c.setFillColor(BRAND)
        c.rect(0, HEIGHT - 8, WIDTH, 8, fill=1, stroke=0)
        if kicker:
            c.setFillColor(BRAND)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(42, HEIGHT - 46, kicker.upper())
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(42, HEIGHT - 76, title)
        c.setStrokeColor(LINE)
        c.line(42, HEIGHT - 90, WIDTH - 42, HEIGHT - 90)

    def text(self, x, y, text, width, size=11, leading=15, color=INK, bold=False):
        font = "Helvetica-Bold" if bold else "Helvetica"
        self.canvas.setFillColor(color)
        self.canvas.setFont(font, size)
        for line in wrapped(text, font, size, width):
            self.canvas.drawString(x, y, line)
            y -= leading
        return y

    def card(self, x, y, w, h, heading, body, tone="white"):
        fills = {"white": SURFACE, "green": SOFT, "gold": WARN}
        c = self.canvas
        c.setFillColor(fills[tone])
        c.setStrokeColor(BRAND if tone == "green" else GOLD if tone == "gold" else LINE)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 14, y + h - 24, heading)
        self.text(x + 14, y + h - 45, body, w - 28, 9.5, 13, MUTED)

    def bullets(self, x, y, items, width, size=10, gap=8):
        for item in items:
            self.canvas.setFillColor(BRAND)
            self.canvas.circle(x + 3, y + 3, 2.3, fill=1, stroke=0)
            y = self.text(x + 14, y + 8, item, width - 14, size, size + 4, INK)
            y -= gap
        return y

    def arrow(self, x1, y, x2):
        c = self.canvas
        c.setStrokeColor(GOLD)
        c.setFillColor(GOLD)
        c.setLineWidth(2)
        c.line(x1, y, x2, y)
        c.line(x2, y, x2 - 7, y + 5)
        c.line(x2, y, x2 - 7, y - 5)

    def end(self):
        c = self.canvas
        c.setStrokeColor(LINE)
        c.line(42, 36, WIDTH - 42, 36)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        c.drawString(42, 22, "SafePay MENA | Phase 2 working prototype | Sandbox and synthetic evidence")
        c.drawRightString(WIDTH - 42, 22, f"{self.page} / 10")
        c.showPage()

    def save(self):
        self.canvas.save()


def build_pitch_deck(output=OUTPUT):
    output.parent.mkdir(parents=True, exist_ok=True)
    deck = Deck(output)
    c = deck.canvas

    # 1. Cover
    deck.page += 1
    c.setFillColor(BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    c.setFillColor(BRAND_DARK)
    c.rect(0, 0, 250, HEIGHT, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(250, 0, 8, HEIGHT, fill=1, stroke=0)
    c.setFillColor(SURFACE)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(42, 410, "SafePay")
    c.drawString(42, 366, "MENA")
    c.setFont("Helvetica", 11)
    c.drawString(42, 330, "GSMA MENA Ignite")
    c.drawString(42, 314, "Phase 2 live demo")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 27)
    c.drawString(300, 415, "Adaptive telecom evidence")
    c.drawString(300, 380, "before instant payments move")
    deck.text(300, 338,
              "A working prototype that keeps routine payments on a zero-call path, then lets a bounded AI agent select the CAMARA evidence needed for elevated-risk cases.",
              430, 13, 19, MUTED)
    c.setFillColor(SOFT)
    c.roundRect(300, 195, 420, 78, 6, fill=1, stroke=0)
    c.setFillColor(BRAND)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(320, 245, "DEMO PROMISE")
    deck.text(320, 222, "Fast for normal users. Evidence-led when risk changes. Policy-controlled at release.", 380, 11, 15, INK)
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(300, 78, "Nokia Network as Code sandbox + CAMARA APIs + Gemini function calling")
    deck.end()

    # 2. Problem and use cases
    deck.begin("One decision point, multiple fraud paths", "Problem")
    deck.text(42, 492,
              "Payment systems see accounts and transactions. Mobile networks can add fresh evidence about the number, SIM, device, and network state before release.",
              700, 12, 17, MUTED)
    deck.card(42, 270, 168, 180, "Coerced transfer",
              "A customer is instructed to send money to a new payee. Identity may verify, but intent is still unsafe.", "gold")
    deck.card(224, 270, 168, 180, "SIM takeover",
              "An unusual session appears after a recent SIM or device change. Combined evidence can justify a protective block.", "green")
    deck.card(406, 270, 168, 180, "Card leakage",
              "A checkout cannot verify the registered number and shows independent device anomalies.", "white")
    deck.card(588, 270, 162, 180, "First setup",
              "A new installation must establish fresh number and SIM evidence before it becomes trusted.", "white")
    deck.text(42, 225,
              "SafePay does not claim that one telecom signal proves fraud. It combines bank context, network observations, and explicit release policy.",
              700, 11, 16, INK, True)
    deck.end()

    # 3. Friction model
    deck.begin("Use evidence only when the context earns it", "User experience")
    c.setFillColor(SOFT)
    c.roundRect(42, 335, 215, 125, 6, fill=1, stroke=0)
    deck.text(60, 430, "1  Local pre-screen", 175, 12, 15, BRAND, True)
    deck.text(60, 398, "Amount, recipient relationship, session anomaly, intent warning, travel and velocity.", 175, 10, 14, MUTED)
    deck.arrow(265, 398, 296)
    deck.card(304, 335, 215, 125, "2  Selective investigation",
              "Only elevated-risk cases invoke Gemini and the relevant network tools.", "gold")
    deck.arrow(527, 398, 558)
    deck.card(566, 335, 184, 125, "3  Policy outcome",
              "Approve, hold, block, retry, or verify device.", "green")
    deck.card(42, 155, 330, 130, "Routine payment",
              "Pre-call score 0. No Gemini turn. No telecom tool. The user sees an immediate approval path.", "green")
    deck.card(420, 155, 330, 130, "Elevated-risk payment",
              "The agent chooses tools from payment facts, observes results, then policy validates the disposition.", "white")
    deck.end()

    # 4. Agent architecture
    deck.begin("Agentic orchestration with hard boundaries", "Technical approach")
    stages = [
        (42, "BANK CONTEXT", "Amount, recipient, market, channel, anomaly"),
        (196, "GEMINI AGENT", "Chooses one tool at a time; max five evidence calls"),
        (350, "NOKIA ADAPTER", "Approved simulator subjects and fixed endpoints only"),
        (504, "POLICY", "Unknown never becomes clean; protective block is not weakened"),
        (658, "OUTCOME", "Stored result with evidence and trace"),
    ]
    for index, (x, heading, body) in enumerate(stages):
        c.setFillColor(SURFACE)
        c.setStrokeColor(LINE)
        c.roundRect(x, 330, 125, 145, 6, fill=1, stroke=1)
        deck.text(x + 10, 448, heading, 105, 9, 12, BRAND, True)
        deck.text(x + 10, 416, body, 105, 8.5, 12, MUTED)
        if index < len(stages) - 1:
            deck.arrow(x + 128, 402, x + 148)
    deck.bullets(54, 275, [
        "Scenario labels are hidden from the model; it receives observable transaction facts.",
        "Repeated, unsupported, malformed, or over-budget tool requests fail closed to RETRY.",
        "A deterministic policy owns the final release decision and can override unsafe approval.",
        "No active-call API is claimed or simulated as Nokia evidence.",
    ], 680, 10, 7)
    deck.end()

    # 5. Verified APIs
    deck.begin("What is actually integrated and verified", "Open Gateway")
    columns = [42, 228, 414, 600]
    entries = [
        ("SIM Swap", "Check a recent SIM change within the requested window.", "Used"),
        ("Number Verification", "OAuth-bound match between bearer and expected number.", "Used"),
        ("Device Swap", "Independent evidence of a recent network device change.", "Used"),
        ("Roaming", "Travel context; never treated as fraud by itself.", "Used"),
    ]
    for x, (name, role, status) in zip(columns, entries):
        deck.card(x, 300, 166, 165, name, role, "green" if name in {"SIM Swap", "Number Verification"} else "white")
        c.setFillColor(BRAND)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 14, 320, status.upper())
    deck.card(42, 145, 345, 105, "Reachability",
              "Available through the adapter for targeted investigation; non-reachability is not proof of fraud.", "white")
    deck.card(405, 145, 345, 105, "Evidence boundary",
              "Verified against Nokia Network as Code sandbox on 8 Sep 2026. Production operators and subscriber traffic are not connected.", "gold")
    deck.end()

    # 6. Demo
    deck.begin("The live demo leads with the decision", "Working prototype")
    if SCREENSHOT.exists():
        image = ImageReader(str(SCREENSHOT))
        c.drawImage(image, 42, 83, width=520, height=408, preserveAspectRatio=True, anchor="c", mask="auto")
    else:
        deck.card(42, 150, 520, 330, "Screenshot unavailable", "Run the browser capture before building the final deck.", "white")
    deck.text(590, 464, "JUDGE FLOW", 155, 10, 13, BRAND, True)
    deck.bullets(590, 430, [
        "Choose Egypt, Saudi Arabia, or UAE.",
        "Select a fraud or enrollment scenario.",
        "Run fixture mode for repeatability.",
        "Switch to Nokia sandbox for the live wire.",
        "Inspect evidence and agent trace only when needed.",
        "Run the 36-case acceptance evaluation.",
    ], 160, 9, 8)
    deck.end()

    # 7. Regional fit
    deck.begin("One orchestration layer, three market contexts", "MENA impact")
    deck.card(42, 300, 220, 170, "Egypt",
              "InstaPay / IPN context. Demonstrates routine transfers, new payees, account takeover, and first setup.", "green")
    deck.card(286, 300, 220, 170, "Saudi Arabia",
              "sarie context. The same decision contract can sit before a bank's release step with locally configured policy.", "white")
    deck.card(530, 300, 220, 170, "United Arab Emirates",
              "Aani context. Supports the same evidence vocabulary without claiming production operator availability.", "white")
    deck.text(42, 244, "The prototype localizes currency, rail name, and transaction context. It does not claim certification, regulatory compliance, or live operator coverage in these markets.", 700, 11, 16, MUTED)
    deck.card(42, 120, 708, 85, "Why it can scale",
              "CAMARA-style contracts separate bank workflow from operator implementation. Commercial rollout still requires operator/API availability, consent design, bank integration, security review, and measured pilots.", "gold")
    deck.end()

    # 8. QA
    deck.begin("Evaluation is part of the product, not a slide claim", "Quality assurance")
    c.setFillColor(BRAND)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(54, 390, "36 / 36")
    deck.text(54, 360, "synthetic acceptance cases across three markets", 210, 11, 15, MUTED)
    deck.card(304, 330, 205, 145, "Failure behavior",
              "Timeouts, invalid JSON, malformed OAuth, missing evidence, and exhausted tool budgets return UNKNOWN or RETRY.", "green")
    deck.card(529, 330, 221, 145, "Workflow integrity",
              "Idempotency, session isolation, cancellation, expiry, enrollment, velocity and policy override are tested.", "white")
    deck.card(42, 145, 330, 130, "Browser acceptance",
              "Desktop and 375px mobile journeys verify the routine zero-call path, enrollment continuation, no overflow, and literal rendering of model markup.", "white")
    deck.card(420, 145, 330, 130, "What this does not prove",
              "Synthetic acceptance tests demonstrate software behavior. They are not real-world fraud detection accuracy, production latency, or business ROI.", "gold")
    deck.end()

    # 9. Commercial path
    deck.begin("Commercially simple; evidence still required", "Viability")
    deck.card(42, 310, 220, 165, "Buyer",
              "Banks, wallets, payment service providers, and fraud platforms that need network evidence at a release decision.", "green")
    deck.card(286, 310, 220, 165, "Model",
              "Platform subscription plus metered orchestrated checks. Carrier charges and model use remain explicit cost inputs.", "white")
    deck.card(530, 310, 220, 165, "Integration",
              "Session, enrollment, payment decision, cancellation, audit evidence, and evaluation endpoints.", "white")
    deck.text(42, 260, "Pilot scorecard", 708, 12, 15, BRAND, True)
    deck.bullets(54, 228, [
        "Measure fraud loss, false positives, abandonment, API availability, and cost per reviewed transaction.",
        "Calibrate bank-owned thresholds by rail, segment, and jurisdiction.",
        "Confirm operator/API coverage and consent flows before making production claims.",
    ], 680, 10, 7)
    deck.end()

    # 10. Ask and sources
    deck.begin("The ask: move from sandbox evidence to a measured pilot", "Next step")
    deck.card(42, 320, 220, 150, "1  Operator access",
              "Confirm target-country API and operator coverage for SIM Swap and Number Verification.", "green")
    deck.card(286, 320, 220, 150, "2  Bank workflow",
              "Connect a non-production release decision and define approved fallback actions.", "white")
    deck.card(530, 320, 220, 150, "3  Pilot evidence",
              "Measure safety, friction, reliability, latency, and unit economics with agreed baselines.", "gold")
    deck.text(42, 270, "Primary references", 708, 11, 14, BRAND, True)
    sources = [
        "CAMARA Number Verification: github.com/camaraproject/NumberVerification",
        "CAMARA SIM Swap: github.com/camaraproject/SimSwap",
        "Nokia Network as Code sandbox: networkascode.nokia.io",
        "SAMA sarie: sama.gov.sa/en-us/payment/pages/Sarie.aspx",
        "CBUAE retail payment rules: rulebook.centralbank.ae",
    ]
    deck.bullets(54, 240, sources, 680, 8.5, 4)
    deck.text(42, 82,
              "SafePay MENA is a working hackathon prototype. All bank context is synthetic. Nokia results use simulator subjects. No production payment is executed.",
              708, 9, 13, RED, True)
    deck.end()

    deck.save()
    return output


if __name__ == "__main__":
    print(build_pitch_deck())
