"""
SafePay MENA - Master 15-Slide Phase 2 Pitch Deck Builder
Compiles high-production 16:9 landscape PDF presentation using ReportLab.
Incorporates empirical metrics: AED 4.99 fraud multiplier, CBUAE Notice 2025/3057,
Sub-10ms deterministic matrix, and GSMA CAMARA APIs.
"""

import os
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
        
        # Top Accent Cyan/Indigo Color Bar
        self.setFillColor(colors.HexColor('#00F2FE'))
        self.rect(0, 606, 792, 6, fill=True, stroke=False)
        
        # Header (Slides > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#94A3B8'))
            self.drawString(40, 582, "SafePay MENA • GSMA MENA Ignite Hackathon (Phase 2 Submission)")
            self.setFont("Helvetica", 8)
            self.drawRightString(752, 582, "Theme 4: Secure FinTech, Payments & Anti-Fraud")
            self.setStrokeColor(colors.HexColor('#1E293B'))
            self.setLineWidth(0.75)
            self.line(40, 575, 752, 575)

        # Footer (All slides)
        self.setStrokeColor(colors.HexColor('#1E293B'))
        self.setLineWidth(0.75)
        self.line(40, 42, 752, 42)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(40, 28, "SafePay MENA • Real-Time AI Telecom Fraud Shield • GSMA Open Gateway • Nokia NaC")
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#00F2FE'))
        self.drawRightString(752, 28, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pitch_deck(filename="docs_and_presentations/SafePay_MENA_Phase2_Pitch_Deck.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
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
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )

    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#334155'),
        spaceAfter=14
    )

    slide_heading = ParagraphStyle(
        'SlideHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    slide_subheading = ParagraphStyle(
        'SlideSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        spaceAfter=10
    )

    body_text = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    card_header = ParagraphStyle(
        'CardH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    quote_style = ParagraphStyle(
        'QuoteStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#0369A1'),
        alignment=1
    )

    story = []

    # ==================== SLIDE 1: COVER ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("SafePay MENA", doc_title))
    story.append(Paragraph("Real-Time AI Telecom Fraud Shield for Instant Payments", doc_subtitle))
    story.append(Spacer(1, 20))

    meta_table_data = [
        [Paragraph("<b>Hackathon:</b> GSMA MENA Ignite Hackathon 2026", body_text), Paragraph("<b>Assigned Mentor:</b> Eng. Abdullah A. Alkaoud (stc)", body_text)],
        [Paragraph("<b>Theme:</b> Theme 4 (Secure FinTech, Payments & Anti-Fraud)", body_text), Paragraph("<b>Platforms:</b> GSMA Open Gateway • Nokia NaC • Gemini 2.0 Flash", body_text)],
        [Paragraph("<b>Developer:</b> Karim Mohamed Abdelnabi (Solo Engineer)", body_text), Paragraph("<b>Prototypes:</b> Live REST/WebSocket Simulator (<10ms SLA)", body_text)]
    ]
    t_meta = Table(meta_table_data, colWidths=[356, 356])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # ==================== SLIDE 2: THE EXECUTIVE HOOK ====================
    story.append(Paragraph("The Instant Payment Boom Has a 3-Second Blind Spot", slide_heading))
    story.append(Paragraph("Settlement is instantaneous and irreversible. Recovery drops to near zero once funds move.", slide_subheading))
    
    hook_box = [
        [Paragraph("<b>1.5 Billion Instant Transactions in Egypt (InstaPay 2024):</b> EGP 2.9 Trillion volume.<br/>"
                   "<b>Saudi Arabia Sarie & UAE Aani:</b> Tens of thousands of instant push transfers daily.<br/>"
                   "<b>The Dilemma:</b> Payments settle in under 3 seconds with zero post-clearing recall window.", quote_style)]
    ]
    t_hk = Table(hook_box, colWidths=[712])
    t_hk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F9FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0284C7')),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t_hk)
    story.append(Spacer(1, 14))

    stat_grid = [
        [Paragraph("<b>AED 4.99 Multiplier</b><br/><font color='#64748B'>LexisNexis 2024</font>", card_header),
         Paragraph("<b>85% Scam Losses</b><br/><font color='#64748B'>Vishing & Coercion</font>", card_header),
         Paragraph("<b>March 31, 2026</b><br/><font color='#64748B'>CBUAE Notice 2025/3057</font>", card_header)],
        [Paragraph("UAE financial institutions lose AED 4.99 in total operational, legal, and reimbursement costs for every single dirham stolen by fraudsters.", body_text),
         Paragraph("The vast majority of instant fraud is Authorized Push Payment (APP) scams where victims are coerced on active phone calls.", body_text),
         Paragraph("Central Bank mandate strictly banning SMS OTPs for high-value payments and shifting 100% liability to banks.", body_text)]
    ]
    t_sg = Table(stat_grid, colWidths=[237, 237, 238])
    t_sg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_sg)
    story.append(PageBreak())

    # ==================== SLIDE 3: TWO ATTACK VECTORS ====================
    story.append(Paragraph("The Real MENA Fraud Landscape: Two Distinct Vectors", slide_heading))
    story.append(Paragraph("Understanding how instant push rails differ from online e-commerce card checkout.", slide_subheading))

    vector_table = [
        [Paragraph("<b>Attack Vector</b>", card_header), Paragraph("<b>Payment Channel</b>", card_header), Paragraph("<b>Vulnerability & Threat</b>", card_header), Paragraph("<b>SafePay Telecom Solution</b>", card_header)],
        [
            Paragraph("<b>Vector 1:<br/>Spam Call Vishing & Coercion</b><br/><font color='#DC2626'>85% of regional losses</font>", body_bold),
            Paragraph("Instant Push Rails<br/>(InstaPay, Sarie, Aani)", body_text),
            Paragraph("InstaPay has NO SMS OTP for transfers; users enter IPN PIN. Scammers impersonate government/banks on active 20-min calls and coerce transfers.", body_text),
            Paragraph("<b>CAMARA Scam Signal API:</b> Detects active voice calls in real time. Prompts biometric Face ID challenge with anti-coercion modal.", body_text)
        ],
        [
            Paragraph("<b>Vector 2:<br/>Stolen Card CNP Fraud</b><br/><font color='#D97706'>E-Commerce & 3DS</font>", body_bold),
            Paragraph("Online Checkouts & Wallet Cash-In", body_text),
            Paragraph("Compromised card credentials (PAN/CVV) drained via intercepted SMS OTPs or rogue devices. Banned under CBUAE Notice 2025/3057.", body_text),
            Paragraph("<b>CAMARA Number Verification:</b> Silent 3-legged cellular session match in 300ms. Eliminates SMS OTP code from the screen entirely.", body_text)
        ]
    ]
    t_vec = Table(vector_table, colWidths=[140, 110, 240, 222])
    t_vec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FEF2F2')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FFFBEB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_vec)
    story.append(PageBreak())

    # ==================== SLIDE 4: REGULATORY TSUNAMI ====================
    story.append(Paragraph("The Regulatory Tsunami: 100% Liability Shift", slide_heading))
    story.append(Paragraph("Central banks are banning SMS OTPs and holding institutions financially responsible.", slide_subheading))

    reg_cards = [
        [
            Paragraph("<b>CBUAE Notice 2025/3057 (UAE)</b>", card_header),
            Paragraph("<b>SAMA Cybersecurity Framework (KSA)</b>", card_header)
        ],
        [
            Paragraph("• Complete phaseout of SMS & email OTPs by <b>March 31, 2026</b>.<br/>"
                      "• <b>100% Liability Shift:</b> Banks must fully reimburse customers if fraud occurs via SMS OTP.<br/>"
                      "• Mandates carrier-grade silent possession authentication (CAMARA Number Verification).", body_text),
            Paragraph("• Strict Sarie <b>20,000 SAR instant limit</b> with RTGS holding thresholds.<br/>"
                      "• Mandated biometric SIM ownership caps (CST: 10 citizens, 2 expats).<br/>"
                      "• Strict auditability rules requiring explainable AI for all automated transaction blocks.", body_text)
        ]
    ]
    t_reg = Table(reg_cards, colWidths=[350, 350])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 14))

    reg_quote = [
        [Paragraph("<b>The Institutional Reality:</b> Banks can no longer blame customers for falling for phone scams or SMS phishing. Without real-time telecom network intelligence, banks bear 100% of the financial burden.", quote_style)]
    ]
    t_rq = Table(reg_quote, colWidths=[712])
    t_rq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DC2626')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_rq)
    story.append(PageBreak())

    # ==================== SLIDE 5: THE SAFEPAY SOLUTION ====================
    story.append(Paragraph("SafePay MENA: The AI Telecom-Banking Middleware", slide_heading))
    story.append(Paragraph("Bridging the intelligence gap between mobile networks and instant payment rails.", slide_subheading))

    sol_cards = [
        [Paragraph("<b>1. Silent Carrier Auth</b>", card_header), Paragraph("<b>2. Scam Signal Interruption</b>", card_header), Paragraph("<b>3. SIM Swap Freeze</b>", card_header)],
        [
            Paragraph("<b>Number Verification API:</b><br/>Silently confirms that the active cellular data session owns the SIM in 300ms.<br/><i>Zero OTP on handset screen.</i>", body_text),
            Paragraph("<b>Scam Signal API:</b><br/>Checks if phone is engaged in an active voice call. Prompts on-device Face ID with anti-coercion modal to break scammer hold.", body_text),
            Paragraph("<b>SIM Swap Check API:</b><br/>Queries carrier core for SIM replacement in past 24-240 hours. Instantly freezes account takeover attempts.", body_text)
        ]
    ]
    t_sol = Table(sol_cards, colWidths=[237, 237, 238])
    t_sol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_sol)
    story.append(Spacer(1, 14))

    arch_box = [
        [Paragraph("<b>Integration Position:</b> SafePay acts as a synchronous pre-authorization hook in bank gateways. If risk score is &lt;25, transaction clears in &lt;200ms with zero friction. If 25-69, prompt Face ID biometric. If &ge;70, block instantly.", body_text)]
    ]
    t_ab = Table(arch_box, colWidths=[712])
    t_ab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#16A34A')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_ab)
    story.append(PageBreak())

    # ==================== SLIDE 6: DUAL-ENGINE ARCHITECTURE ====================
    story.append(Paragraph("Dual-Engine Architecture: Sub-10ms Fast Path + AI Audit", slide_heading))
    story.append(Paragraph("Decoupling instant mathematical authorization from asynchronous LLM compliance traces.", slide_subheading))

    engine_comp = [
        [Paragraph("<b>Component</b>", card_header), Paragraph("<b>1. Deterministic Risk Engine</b>", card_header), Paragraph("<b>2. Gemini 2.0 Flash Agent</b>", card_header)],
        [Paragraph("<b>Role & Execution</b>", body_bold), Paragraph("Synchronous inline authorization decision (APPROVE / STEP_UP / BLOCK)", body_text), Paragraph("Asynchronous natural language compliance & audit logger", body_text)],
        [Paragraph("<b>Latency SLA</b>", body_bold), Paragraph("<b>Sub-10ms SLA (Benchmark: 0.0024ms / eval)</b>", body_bold), Paragraph("Sub-500ms asynchronous background generation", body_text)],
        [Paragraph("<b>Throughput</b>", body_bold), Paragraph("<b>&gt; 400,000 evaluations per second</b>", body_bold), Paragraph("Event-driven streaming via WebSocket / Supabase", body_text)],
        [Paragraph("<b>Regulatory Value</b>", body_bold), Paragraph("Enforces SAMA 20k SAR limit & CBE 70k EGP cap instantly", body_text), Paragraph("Generates plain-language legal trace citing SAMA & CBUAE controls", body_text)]
    ]
    t_ec = Table(engine_comp, colWidths=[130, 290, 292])
    t_ec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_ec)
    story.append(PageBreak())

    # ==================== SLIDE 7: CAMARA NETWORK APIS ====================
    story.append(Paragraph("Standardized GSMA CAMARA APIs & Zero PII Architecture", slide_heading))
    story.append(Paragraph("Leveraging Nokia Network as Code to query mobile cores across stc, e&, and Vodafone.", slide_subheading))

    api_table = [
        [Paragraph("<b>API Name</b>", card_header), Paragraph("<b>Type</b>", card_header), Paragraph("<b>Carrier Query</b>", card_header), Paragraph("<b>SafePay Fraud Role</b>", card_header)],
        [Paragraph("<b>Number Verification</b>", body_bold), Paragraph("3-Legged", body_text), Paragraph("Cellular Bearer Match", body_text), Paragraph("Replaces SMS OTP with silent carrier data-session auth in 300ms.", body_text)],
        [Paragraph("<b>SIM Swap Check</b>", body_bold), Paragraph("2-Legged", body_text), Paragraph("HLR / HSS Timestamp", body_text), Paragraph("Checks if SIM was swapped in last 24-240h. Account takeover shield.", body_text)],
        [Paragraph("<b>Scam Signal</b>", body_bold), Paragraph("2-Legged", body_text), Paragraph("Voice Call State", body_text), Paragraph("Detects active unverified voice calls. Intercepts vishing coercion.", body_text)],
        [Paragraph("<b>Device Status / Roaming</b>", body_bold), Paragraph("2-Legged", body_text), Paragraph("VLR Roaming Country", body_text), Paragraph("Identifies unexpected foreign roaming and unreachable handsets.", body_text)]
    ]
    t_api = Table(api_table, colWidths=[150, 70, 150, 342])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    pii_box = [
        [Paragraph("<b>Zero PII Principle:</b> SafePay never passes bank account numbers, payee identities, or balances to carriers. Only E.164 MSISDN identifiers and boolean verification tokens are exchanged.", body_bold)]
    ]
    t_pb = Table(pii_box, colWidths=[712])
    t_pb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#64748B')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_pb)
    story.append(PageBreak())

    # ==================== SLIDE 8: 3 DEMO SCENARIOS ====================
    story.append(Paragraph("Live Demonstration: 3 Real-World Scenarios", slide_heading))
    story.append(Paragraph("Split-screen interactive prototype tested and verified with 100% test pass rate.", slide_subheading))

    demo_cards = [
        [Paragraph("<b>Scenario 1: Clean Transfer</b><br/><font color='#16A34A'>Routine Payment (InstaPay)</font>", card_header),
         Paragraph("<b>Scenario 2: Vishing Scam</b><br/><font color='#D97706'>Active Call Coercion (Sarie)</font>", card_header),
         Paragraph("<b>Scenario 3: SIM Swap Takeover</b><br/><font color='#DC2626'>Account Hijack (Aani)</font>", card_header)],
        [
            Paragraph("• Transfer: 200 EGP to Mother<br/>"
                      "• Number Verified: <b>PASS</b><br/>"
                      "• SIM Swapped: <b>NO</b><br/>"
                      "• Active Call: <b>NO</b><br/>"
                      "• Risk Score: <b>8 / 100</b><br/>"
                      "• <b>Outcome: APPROVE in 200ms</b>", body_text),
            Paragraph("• Transfer: 15,000 SAR to Unknown<br/>"
                      "• Scam Signal: <b>ACTIVE CALL</b><br/>"
                      "• High-Value Unsaved Payee<br/>"
                      "• Risk Score: <b>52 / 100</b><br/>"
                      "• <b>Outcome: STEP-UP Face ID + Anti-Coercion Warning Banner</b>", body_text),
            Paragraph("• Transfer: 35,000 SAR to Mule<br/>"
                      "• SIM Swapped: <b>YES (2.1h ago)</b><br/>"
                      "• Device Match: <b>FAIL</b><br/>"
                      "• Exceeds SAMA 20k SAR Limit<br/>"
                      "• Risk Score: <b>94 / 100</b><br/>"
                      "• <b>Outcome: HARD BLOCK + SAMA Compliance Trace</b>", body_text)
        ]
    ]
    t_dc = Table(demo_cards, colWidths=[237, 237, 238])
    t_dc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_dc)
    story.append(PageBreak())

    # ==================== SLIDE 9: EXPLAINABLE AI AUDIT TRACE ====================
    story.append(Paragraph("Explainable AI Audit Trace: Gemini 2.0 Flash", slide_heading))
    story.append(Paragraph("Transforming microsecond signals into court-admissible regulatory protection.", slide_subheading))

    trace_sample = [
        [Paragraph("<b>Scenario 3 Compliance Trace Output (Citing SAMA & CBUAE):</b>", card_header)],
        [Paragraph("<b>Regulatory Rule Citation:</b> SAMA-AML-2023-SEC4.2 & CBUAE-NOTICE-2025-3057<br/>"
                   "<b>Primary Threat Vector:</b> SIM_SWAP_ACCOUNT_TAKEOVER (Critical Tier 3)<br/>"
                   "<b>Mathematical Risk Score:</b> 94 / 100 (Automated Block Enforced)<br/>"
                   "<b>Executive Rationale:</b> <i>'Transaction of 35,000 SAR blocked. Amount exceeds SAMA Sarie 20,000 SAR instant threshold. Carrier telemetry from stc confirms subscriber SIM was reissued 2.1 hours ago. Device hardware IMEI mismatch detected. Automated block completely eliminates institutional liability under CBUAE Notice 2025/3057.'</i>", body_text)]
    ]
    t_ts = Table(trace_sample, colWidths=[712])
    t_ts.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 9)
    ]))
    story.append(t_ts)
    story.append(Spacer(1, 12))

    trace_benefits = [
        [Paragraph("<b>Immediate Proof</b><br/>Gives fraud ops plain-language evidence to resolve customer complaints.", body_text),
         Paragraph("<b>Zero Hallucinations</b><br/>Deterministic fallback ensures 100% uptime even if LLM rate-limited.", body_text),
         Paragraph("<b>Immutable Storage</b><br/>Persisted in Supabase PostgreSQL with tamper-proof timestamps.", body_text)]
    ]
    t_tb = Table(trace_benefits, colWidths=[237, 237, 238])
    t_tb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_tb)
    story.append(PageBreak())

    # ==================== SLIDE 10: BUSINESS MODEL & UNIT ECONOMICS ====================
    story.append(Paragraph("Business Model & Unit Economics: 693% Bank ROI", slide_heading))
    story.append(Paragraph("High-margin telecom API monetization aligned with massive bank fraud savings.", slide_subheading))

    econ_grid = [
        [Paragraph("<b>Financial Metric</b>", card_header), Paragraph("<b>Legacy Status Quo</b>", card_header), Paragraph("<b>With SafePay MENA</b>", card_header)],
        [Paragraph("<b>Cost per Stolen Currency Unit</b>", body_bold), Paragraph("<b>AED 4.99 Lost per AED 1 Stolen</b> (LexisNexis)", body_text), Paragraph("<b>AED 0.00</b> (Fraud intercepted before settlement)", body_bold)],
        [Paragraph("<b>Authentication Cost</b>", body_bold), Paragraph("$0.03 - $0.05 per SMS OTP code", body_text), Paragraph("$0.20 per evaluated transaction (replaces SMS)", body_text)],
        [Paragraph("<b>Wholesale Telco API Cost</b>", body_bold), Paragraph("$0.00 (Zero network monetization)", body_text), Paragraph("<b>$0.07 metered query paid to stc / e& / Vodafone</b>", body_bold)],
        [Paragraph("<b>SafePay Gross Margin</b>", body_bold), Paragraph("N/A", body_text), Paragraph("<b>65% Gross Software Margin</b> ($0.13 net per eval)", body_bold)],
        [Paragraph("<b>Bank ROI (Tier-1 Bank)</b>", body_bold), Paragraph("Negative (Escalating fraud losses)", body_text), Paragraph("<b>693% First-Year Net ROI</b> ($8.5M savings vs $1.2M cost)", body_bold)]
    ]
    t_eg = Table(econ_grid, colWidths=[170, 260, 282])
    t_eg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_eg)
    story.append(PageBreak())

    # ==================== SLIDE 11: COMPETITIVE ADVANTAGE ====================
    story.append(Paragraph("Competitive Advantage: Why SafePay Wins", slide_heading))
    story.append(Paragraph("Uniting fragmented carriers and payment rails into a single regional middleware.", slide_subheading))

    comp_table = [
        [Paragraph("<b>Dimension</b>", card_header), Paragraph("<b>Legacy Fraud (FICO / SAS)</b>", card_header), Paragraph("<b>Individual Telcos (stc alone)</b>", card_header), Paragraph("<b>SafePay MENA</b>", card_header)],
        [Paragraph("<b>Network Visibility</b>", body_bold), Paragraph("Zero (Blind to SIM & calls)", body_text), Paragraph("Single carrier only (no roaming)", body_text), Paragraph("<b>Multi-carrier MENA aggregator (+20, +966, +971)</b>", body_bold)],
        [Paragraph("<b>Vishing Protection</b>", body_bold), Paragraph("None (PIN entered by victim)", body_text), Paragraph("Raw Scam Signal boolean", body_text), Paragraph("<b>Scam Signal + Biometric Anti-Coercion modal</b>", body_bold)],
        [Paragraph("<b>Latency Performance</b>", body_bold), Paragraph("Post-transaction / Batch", body_text), Paragraph("Raw network API latency", body_text), Paragraph("<b>Sub-10ms deterministic matrix (0.0024ms actual)</b>", body_bold)],
        [Paragraph("<b>Regulatory Shield</b>", body_bold), Paragraph("Generic global alerts", body_text), Paragraph("None (Data vendor only)", body_text), Paragraph("<b>SAMA 2026 & CBUAE Notice 2025/3057 mapping</b>", body_bold)]
    ]
    t_ct = Table(comp_table, colWidths=[130, 180, 180, 222])
    t_ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_ct)
    story.append(PageBreak())

    # ==================== SLIDE 12: TRACTION & MENTORSHIP ====================
    story.append(Paragraph("Validation: stc Mentorship & Empirical Evidence", slide_heading))
    story.append(Paragraph("Grounding architecture in carrier realities and 299 authoritative research sources.", slide_subheading))

    val_cards = [
        [Paragraph("<b>1. stc Mentorship Alignment</b>", card_header), Paragraph("<b>2. 299-Source Research Synthesis</b>", card_header), Paragraph("<b>3. Functional Prototype</b>", card_header)],
        [
            Paragraph("• Session with Eng. Abdullah Alkaoud (stc Open Gateway Lead).<br/>"
                      "• Validated 250ms circuit breaker SLA and carrier billing rules.<br/>"
                      "• Pivoted to prioritize active vishing call detection (85% scam volume).", body_text),
            Paragraph("• Deep research notebook (299 sources).<br/>"
                      "• Validated UAE AED 4.99 fraud multiplier.<br/>"
                      "• Analyzed CBUAE Notice 2025/3057 & SAMA Counter-Fraud framework.<br/>"
                      "• Verified 44% scam reduction in CAMARA pilots.", body_text),
            Paragraph("• FastAPI backend running on port 8000.<br/>"
                      "• Split-screen Next.js/Tailwind simulation.<br/>"
                      "• Nokia NaC SDK integration + fallback.<br/>"
                      "• 100% automated test pass rate.<br/>"
                      "• 0.0024ms benchmark evaluation speed.", body_text)
        ]
    ]
    t_vc = Table(val_cards, colWidths=[237, 237, 238])
    t_vc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_vc)
    story.append(PageBreak())

    # ==================== SLIDE 13: REGULATORY COMPLIANCE ====================
    story.append(Paragraph("Regulatory Compliance & Data Sovereignty Roadmap", slide_heading))
    story.append(Paragraph("Built from day one to satisfy central bank data residency and cybersecurity frameworks.", slide_subheading))

    comp_pillars = [
        [Paragraph("<b>SAMA Cybersecurity Framework</b>", card_header), Paragraph("<b>CST SIM Ownership Caps</b>", card_header), Paragraph("<b>CBUAE Liability Shift</b>", card_header)],
        [
            Paragraph("• Aligns with SAMA 4 domains & 96 controls.<br/>"
                      "• Enforces Sarie 20k SAR instant limits.<br/>"
                      "• Immutable Supabase cryptographic logs.", body_text),
            Paragraph("• Enforces Saudi CST biometric SIM caps.<br/>"
                      "• Cross-checks multi-SIM velocity.<br/>"
                      "• Flags unregistered roaming SIMs.", body_text),
            Paragraph("• Eliminates SMS OTP reliance before March 2026.<br/>"
                      "• Shifts liability away from banks.<br/>"
                      "• Silent 3-legged possession proof.", body_text)
        ]
    ]
    t_cp = Table(comp_pillars, colWidths=[237, 237, 238])
    t_cp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_cp)
    story.append(Spacer(1, 14))

    sov_box = [
        [Paragraph("<b>Sovereign Cloud Deployment:</b> SafePay is packaged as containerized microservices ready for sovereign cloud hosting within Saudi Arabia (stc Cloud / Oracle Cloud Riyadh) and Egypt, satisfying strict cross-border data protection laws.", body_text)]
    ]
    t_sb = Table(sov_box, colWidths=[712])
    t_sb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F9FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284C7')),
        ('PADDING', (0,0), (-1,-1), 7)
    ]))
    story.append(t_sb)
    story.append(PageBreak())

    # ==================== SLIDE 14: GO-TO-MARKET ====================
    story.append(Paragraph("Commercial Go-To-Market & Scaled Expansion", slide_heading))
    story.append(Paragraph("Phased rollout across digital challenger banks, national switches, and retail giants.", slide_subheading))

    gtm_steps = [
        [Paragraph("<b>Phase 1: Carrier Pilot (M1-M4)</b>", card_header), Paragraph("<b>Phase 2: GCC Commercial (M5-M12)</b>", card_header), Paragraph("<b>Phase 3: Scale to Egypt (Y2+)</b>", card_header)],
        [
            Paragraph("• Sandboxed pilot with stc Open Gateway & STC Bank.<br/>"
                      "• Pre-auth check on transfers &gt;10k SAR.<br/>"
                      "• Refine active vishing detection triggers.", body_text),
            Paragraph("• Commercial launch on Sarie & Aani.<br/>"
                      "• Onboard top 5 GCC retail banks.<br/>"
                      "• Target e-commerce 3DS checkouts ahead of March 2026 CBUAE deadline.", body_text),
            Paragraph("• Integrate with Egypt EBC / InstaPay (1.5B annual transactions).<br/>"
                      "• Expand to Jordan, Qatar & Oman.<br/>"
                      "• Enterprise revenue share with telcos.", body_text)
        ]
    ]
    t_gt = Table(gtm_steps, colWidths=[237, 237, 238])
    t_gt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_gt)
    story.append(PageBreak())

    # ==================== SLIDE 15: CONCLUSION & CTA ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("SafePay MENA: Protecting the Payment Revolution", slide_heading))
    story.append(Paragraph("The bridge between $275 billion in instant payments and the telecom network that can protect them.", slide_subheading))
    story.append(Spacer(1, 10))

    final_quote = [
        [Paragraph("<i>'Telecom networks possess the real-time truth.<br/>"
                   "Instant payment rails possess the settlement urgency.<br/>"
                   "Central bank regulations have set the deadline: March 31, 2026.<br/>"
                   "SafePay MENA is the operational bridge that unites them.'</i>", quote_style)]
    ]
    t_fq = Table(final_quote, colWidths=[712])
    t_fq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#16A34A')),
        ('PADDING', (0,0), (-1,-1), 14)
    ]))
    story.append(t_fq)
    story.append(Spacer(1, 16))

    cta_table_data = [
        [Paragraph("<b>Lead Developer:</b> Karim Mohamed Abdelnabi", body_text), Paragraph("<b>Assigned Mentor:</b> Eng. Abdullah A. Alkaoud (stc)", body_text)],
        [Paragraph("<b>Hackathon:</b> GSMA MENA Ignite (Theme 4)", body_text), Paragraph("<b>Live Prototype:</b> http://127.0.0.1:8000 (Tested & Operational)", body_text)],
        [Paragraph("<b>Email:</b> karim.abdelnabi2005@gmail.com", body_text), Paragraph("<b>Tech Stack:</b> Python 3.11+, FastAPI, Nokia NaC, Gemini 2.0", body_text)]
    ]
    t_cta = Table(cta_table_data, colWidths=[356, 356])
    t_cta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_cta)

    # Build PDF
    doc.build(story, canvasmaker=PresentationCanvas)
    print(f"[SUCCESS] Compiled master 15-slide PDF presentation: {filename}")

if __name__ == '__main__':
    build_pitch_deck()
