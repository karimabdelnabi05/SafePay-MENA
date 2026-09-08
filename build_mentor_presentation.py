"""
SafePay MENA - Master Presentation Deck for Eng. Abdullah A. Alkaoud (stc)
Clean 9-Slide Deck with Simple, Natural, Conversational Questions
Compiled via ReportLab (16:9 Landscape Format)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class PresentationCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PresentationCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_chrome(num_pages)
            super(PresentationCanvas, self).showPage()
        super(PresentationCanvas, self).save()

    def draw_slide_chrome(self, page_count):
        self.saveState()
        
        # Top Accent Color Bar
        self.setFillColor(colors.HexColor('#4338ca')) # Indigo 700
        self.rect(0, 606, 792, 6, fill=True, stroke=False)
        
        # Header (Slides > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#475569'))
            self.drawString(40, 582, "SafePay MENA • GSMA MENA Ignite Hackathon (Phase 2 Mentorship)")
            self.setFont("Helvetica", 8)
            self.drawRightString(752, 582, "Mentor Briefing: Eng. Abdullah A. Alkaoud (stc)")
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.75)
            self.line(40, 575, 752, 575)

        # Footer (All slides)
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.75)
        self.line(40, 42, 752, 42)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(40, 28, "SafePay MENA • Real-Time AI Telecom Fraud Shield • Meeting Date: Mon Sep 7, 2026 (3:00 PM)")
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#334155'))
        self.drawRightString(752, 28, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename="SafePay_MENA_Mentor_Presentation.pdf"):
    # 792 x 612 pt landscape letter (Printable width: 712 pt)
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )

    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#334155'),
        spaceAfter=14
    )

    slide_heading = ParagraphStyle(
        'SlideHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )

    card_h1 = ParagraphStyle(
        'CardH1',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )

    card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    card_body_bold = ParagraphStyle(
        'CardBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0f172a')
    )

    badge_text = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#3730a3')
    )

    formula_text = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f766e'),
        alignment=1
    )

    story = []

    # =========================================================================
    # SLIDE 1: Title & Executive Briefing
    # =========================================================================
    story.append(Spacer(1, 25))
    badge_data = [[Paragraph("<b>GSMA MENA IGNITE HACKATHON • THEME 4: SECURE FINTECH, PAYMENTS & ANTI-FRAUD</b>", badge_text)]]
    t_badge = Table(badge_data, colWidths=[712])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#818cf8')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 14))

    story.append(Paragraph("SafePay MENA", doc_title))
    story.append(Paragraph("Real-Time AI Fraud Shield for Instant Payments Powered by Telecom Network Intelligence (CAMARA)", doc_subtitle))
    story.append(Spacer(1, 10))

    meta_table_data = [
        [
            Paragraph("<b>Developer & Team Lead:</b><br/>Karim Mohamed Abdelnabi<br/><font color='#64748b'>Solo Full-Stack & AI Engineer<br/>Cairo, Egypt • +201159821098</font>", card_body),
            Paragraph("<b>Assigned Hackathon Mentor:</b><br/>Eng. Abdullah A. Alkaoud<br/><font color='#64748b'>Saudi Telecom Company (stc)<br/>mentor-contact-removed</font>", card_body),
            Paragraph("<b>Mentorship Session:</b><br/>Monday, September 7, 2026<br/><font color='#64748b'>3:00 PM – 3:30 PM (Cairo / Riyadh)<br/>30-Minute Technical Discussion</font>", card_body)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[237, 237, 238])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    overview_box = [
        [Paragraph("<b>Executive Summary:</b> SafePay MENA is an AI-orchestrated telecom-banking security middleware bridging the fraud gap between instant payment rails (InstaPay Egypt, Sarie / STC Bank Saudi, Aani UAE) and telecom operators (stc, Vodafone, e&). Using Gemini 2.0 Flash and 4 CAMARA APIs via Nokia Network-as-Code, SafePay detects SIM swaps, rogue device upgrades, and account takeover vectors in &lt;250ms with a 95% zero-call optimization strategy.", card_body)]
    ]
    t_ov = Table(overview_box, colWidths=[712])
    t_ov.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_ov)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: The Market Problem (Telecom-Banking Fraud Gap)
    # =========================================================================
    story.append(Paragraph("01 • Market Context & The Telecom-Banking Fraud Gap", slide_heading))
    story.append(Spacer(1, 6))

    prob_data = [
        [
            Paragraph("<font color='#b91c1c' size='13'><b>$275B+ Instant Rails</b></font><br/><b>Velocity Without Cross-Visibility</b>", card_h1),
            Paragraph("<font color='#c2410c' size='13'><b>SMS OTP is Broken</b></font><br/><b>Social Engineering Takeovers</b>", card_h1),
            Paragraph("<font color='#4338ca' size='13'><b>The Blind Banking Silo</b></font><br/><b>Zero Real-Time Carrier Signals</b>", card_h1)
        ],
        [
            Paragraph("• <b>Egypt (InstaPay):</b> 1.1B+ transactions in H1 2025 alone (EGP 2.4T volume, +110% YoY).<br/>• <b>Saudi Arabia (Sarie):</b> 593M+ transactions, STC Bank reaching 12M+ customers.<br/>• <b>Settlement Speed:</b> Transfers settle in &lt; 10 seconds, leaving zero time for traditional fraud investigation teams.", card_body),
            Paragraph("• <b>SIM Swap Epidemic:</b> Criminals social-engineer telecom branch clerks or forge paper IDs to reissue victim SIMs.<br/>• <b>SMS Interception:</b> Bank OTPs arrive directly on the scammer's handset.<br/>• <b>Midnight Draining:</b> Scammers reset PINs and drain funds at 3:00 AM while victims sleep.", card_body),
            Paragraph("• <b>Banks operate in isolation:</b> Banking core switches have zero API connectivity to mobile networks.<br/>• <b>The Blind Spot:</b> Banks cannot detect if a SIM card was replaced 45 minutes ago or if an IMEI changed.<br/>• <b>$50M+ Annual Losses:</b> Direct fraud reimbursement costs and brand reputation damage.", card_body)
        ]
    ]
    t_prob = Table(prob_data, colWidths=[237, 237, 238])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#fef2f2')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#fff7ed')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#eef2ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 12))

    comp_box = [
        [Paragraph("<b>SAMA 2026 & CBE Regulatory Pressure:</b> The Saudi Central Bank (SAMA) Counter-Fraud Framework (effective April 2026) and Central Bank of Egypt (CBE) mandate real-time fraud mitigation, strict MFA for out-of-pattern transactions, and auditable decision explainability. Legacy SMS OTP is no longer recognized as secure authentication for high-risk transfers.", card_body)]
    ]
    t_comp = Table(comp_box, colWidths=[712])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: System Architecture (Hybrid Deterministic + AI)
    # =========================================================================
    story.append(Paragraph("02 • System Architecture: 3-Layer Hybrid Defense", slide_heading))
    story.append(Spacer(1, 6))

    arch_data = [
        [
            Paragraph("<b>Layer 1: Deterministic Shield (&lt;15ms)</b><br/><font color='#0f766e'>Pure Python Core Gateway</font>", card_h1),
            Paragraph("<b>Layer 2: AI Reasoning Brain</b><br/><font color='#4338ca'>Google Gemini 2.0 Flash</font>", card_h1),
            Paragraph("<b>Layer 3: Carrier & Audit Tier</b><br/><font color='#854d0e'>Nokia NaC & Supabase</font>", card_h1)
        ],
        [
            Paragraph("• <b>E.164 Normalizer:</b> Standardizes Egypt (+20) and Saudi (+966) phone numbers.<br/>• <b>In-Memory Cache (Redis):</b> 3-minute TTL serves verified SIM status in 1ms.<br/>• <b>Mathematical Matrix:</b> Computes non-linear risk score deterministically.<br/>• <b>Hard Safety Override:</b> Math engine overrides AI for confirmed SIM swaps.", card_body),
            Paragraph("• <b>Dynamic Tool Calling:</b> Intelligently routes queries across CAMARA APIs only when anomalies trip thresholds.<br/>• <b>Behavioral Scorer:</b> Analyzes inter-transaction interval velocities.<br/>• <b>SAMA 2026 Trace Generator:</b> Formulates plain-language, non-hallucinated compliance audit trails.", card_body),
            Paragraph("• <b>Nokia Network-as-Code SDK:</b> Aggregates carrier 5G Core NEF APIs across stc, Vodafone, and e&.<br/>• <b>Local Mock Engine:</b> Offline deterministic fixture engine toggled via USE_MOCK.<br/>• <b>Supabase PostgreSQL:</b> Tamper-proof, cryptographically signed audit logs.<br/>• <b>Next.js Dashboard:</b> WebSocket live feed.", card_body)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[237, 237, 238])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f0fdfa')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#eef2ff')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#fefce8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 12))

    rule_box = [
        [Paragraph("<b>Architectural Rule of Law:</b> Financial authorization decisions (APPROVE, STEP_UP, BLOCK) are resolved in &lt;15ms before or alongside asynchronous LLM trace generation. The system is 100% immune to prompt injection because mathematical safety thresholds strictly govern fund movement.", card_body)]
    ]
    t_rule = Table(rule_box, colWidths=[712])
    t_rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_rule)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: 4 Core CAMARA APIs Deep-Dive
    # =========================================================================
    story.append(Paragraph("03 • The 4 Core CAMARA 5G Network APIs (Nokia NaC)", slide_heading))
    story.append(Spacer(1, 6))

    api_table_data = [
        [
            Paragraph("<b>CAMARA API</b>", card_body_bold),
            Paragraph("<b>OAuth Type</b>", card_body_bold),
            Paragraph("<b>OpenAPI Endpoint</b>", card_body_bold),
            Paragraph("<b>Role in SafePay Architecture</b>", card_body_bold),
            Paragraph("<b>SLA & Latency</b>", card_body_bold)
        ],
        [
            Paragraph("<b>1. SIM Swap</b>", card_body_bold),
            Paragraph("2-Legged<br/>(Server-to-Server)", card_body),
            Paragraph("<font size='7.5' color='#0f766e'>POST /sim-swap/v0/check<br/>POST /sim-swap/v0/retrieve-date</font>", card_body),
            Paragraph("Queries carrier HSS/UDM database for replacement timestamps within 24-48h. Detects recycled phone numbers by comparing activation date against account creation.", card_body),
            Paragraph("&lt; 150ms<br/>Cached (3m TTL)", card_body)
        ],
        [
            Paragraph("<b>2. Number Verification</b>", card_body_bold),
            Paragraph("3-Legged<br/>(Cellular Bearer)", card_body),
            Paragraph("<font size='7.5' color='#1d4ed8'>POST /number-verification/v0/verify<br/>GET /device-phone-number</font>", card_body),
            Paragraph("Silently verifies live cellular connection over 4G/5G mobile radio. Replaces SMS OTPs entirely. Bypasses need to manually type codes.", card_body),
            Paragraph("&lt; 300ms<br/>(First Setup)", card_body)
        ],
        [
            Paragraph("<b>3. Device Status</b>", card_body_bold),
            Paragraph("2-Legged<br/>(Server-to-Server)", card_body),
            Paragraph("<font size='7.5' color='#7c3aed'>POST /device-status/v0/roaming<br/>POST /device-status/v0/reachability</font>", card_body),
            Paragraph("Detects international roaming country codes (MCC/MNC) and unreachable handsets during sudden midnight large-value transactions.", card_body),
            Paragraph("&lt; 120ms<br/>Async parallel", card_body)
        ],
        [
            Paragraph("<b>4. Device Swap</b>", card_body_bold),
            Paragraph("2-Legged<br/>(Server-to-Server)", card_body),
            Paragraph("<font size='7.5' color='#be185d'>POST /device-swap/v0/check</font>", card_body),
            Paragraph("Checks if subscriber's SIM was inserted into a new hardware handset (IMEI change). Shuts down 72-hour sleeper SIM attacks completely.", card_body),
            Paragraph("&lt; 140ms<br/>Async parallel", card_body)
        ]
    ]
    t_api = Table(api_table_data, colWidths=[105, 95, 160, 262, 90])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    bonus_box = [
        [Paragraph("<b>Compliance Standards:</b> Fully aligned with GSMA Open Gateway Camara Commonalities v1.0.0, OpenAPI 3.0.3 YAML specifications, and RFC 6749 OAuth 2.0 Client Credentials & Authorization Code grant flows.", card_body)]
    ]
    t_bn = Table(bonus_box, colWidths=[712])
    t_bn.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_bn)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: Dynamic Risk Scoring Formula & Multipliers
    # =========================================================================
    story.append(Paragraph("04 • Dynamic Non-Linear Risk Formula & Compound Multipliers", slide_heading))
    story.append(Spacer(1, 6))

    f_box = [
        [Paragraph("RiskScore = min(100, max(0, [Base + SIM_Decay(t) + RelativeAmount + Multipliers] − TrustReservoir))", formula_text)]
    ]
    t_f = Table(f_box, colWidths=[712])
    t_f.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_f)
    story.append(Spacer(1, 8))

    math_data = [
        [
            Paragraph("<b>1. SIM Time Decay</b>", card_h1),
            Paragraph("<b>2. Relative Amount Ratio</b>", card_h1),
            Paragraph("<b>3. Compound Multipliers</b>", card_h1),
            Paragraph("<b>4. User Trust Reservoir</b>", card_h1)
        ],
        [
            Paragraph("SIM swaps are not binary 48h walls:<br/>• &lt; 1h ago: <b>+85 pts</b><br/>• 12h ago: <b>+50 pts</b><br/>• 24h ago: <b>+25 pts</b><br/>• 40h ago: <b>+5 pts</b><br/>Avoids blocking legit users who upgraded SIM yesterday.", card_body),
            Paragraph("Relative to user habits:<br/>• Ratio = Amount ÷ User Avg<br/>• Ratio &lt; 2.0x: <b>+0 pts</b><br/>• Ratio 2x–10x: <b>+10 pts</b><br/>• Ratio &gt; 20x: <b>+25 pts</b><br/>20k SAR is routine for business, anomaly for student.", card_body),
            Paragraph("Toxic combos multiply risk:<br/>• New IMEI Hardware: <b>1.5x</b><br/>• Burst Velocity (3tx/5m): <b>1.4x</b><br/>• Rogue Roaming IP: <b>1.3x</b><br/>• Dormant Hours (3 AM): <b>1.2x</b><br/>Spikes attacker score to 95+.", card_body),
            Paragraph("Anti-Frustration buffer:<br/>• Account age &gt; 1 yr: <b>-25 pts</b><br/>• Known phone token: <b>-30 pts</b><br/>• 50+ clean past txs: <b>-20 pts</b><br/>High-trust users absorb travel anomalies with 0 prompts.", card_body)
        ]
    ]
    t_m = Table(math_data, colWidths=[178, 178, 178, 178])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_m)
    story.append(Spacer(1, 8))

    tiers_data = [
        [
            Paragraph("<b>Score 0 – 25: SILENT APPROVE</b><br/><font color='#047857'>Instant 200ms background execution. Zero prompts, zero friction.</font>", card_body),
            Paragraph("<b>Score 26 – 60: STEP-UP BIOMETRIC</b><br/><font color='#b45309'>1-second Native Face ID challenge. Legitimate user passes instantly.</font>", card_body),
            Paragraph("<b>Score 61 – 85: HARD BLOCK</b><br/><font color='#b91c1c'>Transfer rejected. 24h cooling-off pause on new beneficiaries.</font>", card_body),
            Paragraph("<b>Score 86 – 100: EMERGENCY FREEZE</b><br/><font color='#701a75'>Total account lockdown. SMS alerts sent, branch re-auth required.</font>", card_body)
        ]
    ]
    t_tiers = Table(tiers_data, colWidths=[178, 178, 178, 178])
    t_tiers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#ecfdf5')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#fffbeb')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#fef2f2')),
        ('BACKGROUND', (3,0), (3,0), colors.HexColor('#fdf4ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 7)
    ]))
    story.append(t_tiers)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: The 95% Zero-Call Strategy (Cost & Latency Optimization)
    # =========================================================================
    story.append(Paragraph("05 • The 95% Zero-Call Strategy: Minimizing Telecom API Overhead", slide_heading))
    story.append(Spacer(1, 6))

    zero_data = [
        [
            Paragraph("<b>1. Hardware Device Token</b><br/><font color='#0f766e'>0ms Local Cryptographic Check</font>", card_h1),
            Paragraph("<b>2. 3-Minute Redis Cache</b><br/><font color='#1d4ed8'>Sub-1ms Memory Lookup</font>", card_h1),
            Paragraph("<b>3. Recipient Trust Graph</b><br/><font color='#4338ca'>Whitelisted Beneficiary Bypass</font>", card_h1)
        ],
        [
            Paragraph("• One-time device binding during initial app installation creates a cryptographic token stored in Apple Secure Enclave / Android Keystore.<br/>• When a user opens the app on their trusted daily phone, local device attestation approves routine transfers in 0ms.<br/>• <b>Result: Zero Telco API calls ($0.00 cost) for 90% of daily transactions.</b>", card_body),
            Paragraph("• When high-risk thresholds or new devices trigger a live CAMARA check, the clean status is cached in Redis with a 3-minute TTL.<br/>• Rapid sequential checkouts (e.g. Amazon checkout followed by food delivery) hit Redis in 1ms.<br/>• <b>High-Value Bypass: Any transfer &gt; 5,000 EGP strictly bypasses cache and queries telco live.</b>", card_body),
            Paragraph("• Outgoing transfers to phonebook contacts (persisted &gt; 30 days) and recurring historical payees (landlord, utility bills) are automatically whitelisted.<br/>• Zero carrier queries required for transfers within established trusted social graph.<br/>• Anti-mule engine overrides whitelist if recipient account exhibits abnormal velocity.", card_body)
        ]
    ]
    t_zero = Table(zero_data, colWidths=[237, 237, 238])
    t_zero.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f0fdfa')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#eff6ff')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#eef2ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_zero)
    story.append(Spacer(1, 10))

    dist_data = [
        [Paragraph("<b>Production Traffic Distribution (Per 1,000 Payment Ingress Requests):</b><br/>• <b>850 Transactions (85%):</b> Handled via Local Hardware Device Trust Token & Whitelist ➔ <b>0 Telco Calls ($0.00)</b><br/>• <b>100 Transactions (10%):</b> Served from 3-Minute Redis Cache (Multi-app checkouts) ➔ <b>1ms Response (0 Telco Calls)</b><br/>• <b>50 Transactions (5%):</b> High-risk anomalies (New device, SIM Swap, Roaming, &gt;5k EGP) ➔ <b>Trigger Live CAMARA Queries ($0.015)</b>", card_body)]
    ]
    t_dist = Table(dist_data, colWidths=[712])
    t_dist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ecfdf5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#10b981')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_dist)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: Prototype & 3 Live Demo Scenarios
    # =========================================================================
    story.append(Paragraph("06 • Prototype Validation: The 3 Core Live Demo Scenarios", slide_heading))
    story.append(Spacer(1, 6))

    scen_table = [
        [
            Paragraph("<b>Scenario 1: Clean Flow</b><br/><font color='#047857'>Everyday 200 EGP Transfer</font>", card_h1),
            Paragraph("<b>Scenario 2: SIM Swap Attack</b><br/><font color='#b91c1c'>35,000 SAR Midnight Takeover</font>", card_h1),
            Paragraph("<b>Scenario 3: Travel Step-Up</b><br/><font color='#b45309'>2,500 EGP UAE Roaming</font>", card_h1)
        ],
        [
            Paragraph("• <b>User:</b> Karim sends 200 EGP to brother Omar.<br/>• <b>Signals:</b> Known iPhone, SIM clean, contact in phonebook for 2 years.<br/>• <b>Telemetry:</b> Silent 3-legged Number Verification passes over 4G data in 280ms.<br/>• <b>Math Score:</b> <b>4 / 100</b> (Trust buffer absorbs base risk).<br/>• <b>Decision:</b> <b>INSTANT APPROVE (200ms)</b>.<br/>• <b>User Experience:</b> Zero prompts, zero friction.", card_body),
            Paragraph("• <b>Attacker:</b> Scammer initiates 35,000 SAR transfer at 3:00 AM to a new mule IBAN.<br/>• <b>Signals:</b> SIM swapped 2h ago, new burner phone IMEI, midnight sleeping hours.<br/>• <b>Telemetry:</b> CAMARA SIM Swap returns True + Device Swap returns IMEI mismatch.<br/>• <b>Math Score:</b> <b>96 / 100</b> (Compound Multipliers).<br/>• <b>Decision:</b> <b>HARD BLOCK + EMERGENCY FREEZE</b>.<br/>• <b>Trace:</b> SAMA 2026 tamper-proof audit trace.", card_body),
            Paragraph("• <b>User:</b> Legitimate user sends 2,500 EGP while attending a conference in Dubai.<br/>• <b>Signals:</b> Trusted phone hardware, but international roaming active on e& network.<br/>• <b>Telemetry:</b> CAMARA Roaming = UAE, SIM Swap = False.<br/>• <b>Math Score:</b> <b>42 / 100</b> (Moderate anomaly).<br/>• <b>Decision:</b> <b>STEP-UP CHALLENGE</b>.<br/>• <b>User Experience:</b> 1-sec Native Face ID glance ➔ Passes ➔ Money sent immediately.", card_body)
        ]
    ]
    t_sc = Table(scen_table, colWidths=[237, 237, 238])
    t_sc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ecfdf5')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#fef2f2')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#fffbeb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_sc)
    story.append(Spacer(1, 10))

    dash_box = [
        [Paragraph("<b>Next.js Split-Screen Interactive UI:</b> Left panel simulates the mobile banking app (InstaPay/stc pay transfer interface with interactive biometric challenge modal). Right panel displays real-time telemetry: Live Risk Score Gauge (0-100), parallel CAMARA API execution times, and Gemini 2.0 Flash compliance audit log streaming via WebSocket.", card_body)]
    ]
    t_dash = Table(dash_box, colWidths=[712])
    t_dash.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_dash)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: Financial Model & 3-Way Economic Win
    # =========================================================================
    story.append(Paragraph("07 • Proven Unit Economics: The 3-Way Financial Win", slide_heading))
    story.append(Spacer(1, 6))

    fin_data = [
        [
            Paragraph("<b>1. For Banks & FinTechs</b><br/><font color='#0f766e'>Cost Reduction & Trust</font>", card_h1),
            Paragraph("<b>2. For Telcos (stc / Vodafone)</b><br/><font color='#4338ca'>Wholesale API Monetization</font>", card_h1),
            Paragraph("<b>3. For SafePay MENA</b><br/><font color='#854d0e'>Scalable SaaS Platform</font>", card_h1)
        ],
        [
            Paragraph("• <b>$55,500 Net Monthly Savings:</b> Eliminates $40k/mo in SIM swap fraud losses + $25k/mo in SMS OTP carrier fees.<br/>• <b>693.7% Net ROI:</b> Less than 14-day payback period on SaaS subscription.<br/>• <b>Reduced Dispute Overhead:</b> Zero chargeback investigations, SAMA audit-ready.<br/>• <b>Higher Conversion:</b> 300ms silent check increases checkout success by 18%.", card_body),
            Paragraph("• <b>92% Gross Profit Margin:</b> Telecom networks have near-zero marginal cost for HSS/UDM database read queries.<br/>• <b>$1.2M+ ARR per 10M Calls:</b> Transforms cost-center network infrastructure into a high-margin enterprise revenue stream.<br/>• <b>Direct Enterprise Stickiness:</b> Deep API integration with commercial banks and FinTechs.", card_body),
            Paragraph("• <b>57.1% – 62.5% Gross Margin:</b> SafePay purchases CAMARA API calls at $0.012 wholesale and bundles into SaaS tier at $0.028 retail.<br/>• <b>$7.8M ARR by Year 3:</b> Scaling across Egypt, Saudi Arabia, and UAE payment volumes (34.3% Net Profit Margin).<br/>• <b>SaaS Tiers:</b> $1,500/mo Starter, $6,000/mo Enterprise Bank, $25,000/mo National Rails.", card_body)
        ]
    ]
    t_fin = Table(fin_data, colWidths=[237, 237, 238])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f0fdfa')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#eef2ff')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#fefce8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    roi_box = [
        [Paragraph("<b>The Bank Business Case:</b> For an average MENA commercial bank processing 2.5M transactions monthly, deploying SafePay costs $8,000/mo in SaaS and API fees, while recapturing $63,500/mo in prevented fraud losses and eliminated SMS OTP carrier costs. The net savings to the bank exceed $666,000 annually.", card_body)]
    ]
    t_roi = Table(roi_box, colWidths=[712])
    t_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_roi)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: Strategic Discussion Topics (Conversational & Natural)
    # =========================================================================
    story.append(Paragraph("08 • Strategic Technical Discussion with Eng. Abdullah A. Alkaoud (stc)", slide_heading))
    story.append(Spacer(1, 6))

    q_table_data = [
        [
            Paragraph("<b>Topic & Goal</b>", card_body_bold),
            Paragraph("<b>Natural Question to Ask Eng. Abdullah</b>", card_body_bold),
            Paragraph("<b>Why This Helps Us Build SafePay</b>", card_body_bold)
        ],
        [
            Paragraph("<b>1. Demo Focus</b><br/><font color='#b45309'>Phase 2 Priorities</font>", card_h1),
            Paragraph("<i>'Eng. Abdullah, what makes a prototype really stand out in Phase 2? Should I focus more on showing how the system handles network errors and delays, or on having a clean, simple user interface?'</i>", card_body),
            Paragraph("Tells us whether to spend our remaining days polishing the UI vs building error-handling circuit breakers.", card_body)
        ],
        [
            Paragraph("<b>2. Fraud vs Convenience</b><br/><font color='#047857'>User Experience</font>", card_h1),
            Paragraph("<i>'Since stc operates STC Bank, what is the best way to balance fraud security with user experience? We don't want to annoy legitimate customers with pop-ups, so when should we actually challenge the user?'</i>", card_body),
            Paragraph("Validates our 95/5 rule (invisible security for routine payments, biometrics only for extreme anomalies).", card_body)
        ],
        [
            Paragraph("<b>3. Latency & Speed</b><br/><font color='#1d4ed8'>Real-World SLA</font>", card_h1),
            Paragraph("<i>'In instant payments like Sarie or InstaPay, speed is everything. In the real world, how fast do these CAMARA APIs respond, and what is the best fallback if a telecom query takes too long?'</i>", card_body),
            Paragraph("Gives us real-world response time expectations and confirms our fail-secure biometric fallback plan.", card_body)
        ],
        [
            Paragraph("<b>4. Real Edge Cases</b><br/><font color='#7c3aed'>Phone Realities</font>", card_h1),
            Paragraph("<i>'From stc's experience, what are the most common real-world phone situations in the region—like dual-SIM phones, travel, or eSIMs—that we should be careful about?'</i>", card_body),
            Paragraph("Highlights real-world phone situations in Saudi Arabia and the Gulf so our test cases reflect true user habits.", card_body)
        ],
        [
            Paragraph("<b>5. Sandbox Testing</b><br/><font color='#be185d'>Developer Tooling</font>", card_h1),
            Paragraph("<i>'For testing on the developer platform, are there specific test phone numbers or scenarios you recommend we run to make sure everything works before our submission?'</i>", card_body),
            Paragraph("Gives us exact test phone numbers and sandbox fixtures to run live verification checks before recording our demo video.", card_body)
        ]
    ]
    t_q = Table(q_table_data, colWidths=[150, 362, 200])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#fffbeb')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#ecfdf5')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#eff6ff')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#fbf5ff')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#fdf2f8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_q)
    story.append(Spacer(1, 10))

    call_confirm_box = [
        [Paragraph("<b>Meeting Confirmed:</b> Monday, September 7, 2026 at 3:00 PM – 3:30 PM (Cairo / Riyadh time).<br/><b>Developer:</b> Karim Mohamed Abdelnabi • karim.abdelnabi2005@gmail.com • +201159821098 &nbsp;|&nbsp; <b>Mentor:</b> Eng. Abdullah A. Alkaoud • mentor-contact-removed (stc)", card_body)]
    ]
    t_cc = Table(call_confirm_box, colWidths=[712])
    t_cc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#6366f1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_cc)

    # Build PDF
    doc.build(story, canvasmaker=PresentationCanvas)
    print(f"[SUCCESS] Compiled clean, natural 9-slide PDF presentation: {filename}")

if __name__ == '__main__':
    build_pdf()
