import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Widescreen 16:9 dimensions: 960 x 540 pt
PAGE_WIDTH = 960
PAGE_HEIGHT = 540

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages for footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Draw footer only (AFTER text is drawn)
            self.setFont("Helvetica-Bold", 10)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(40, 20, "SafePay MENA - Phase 1 Submission")
            self.drawRightString(PAGE_WIDTH - 40, 20, f"{self._pageNumber} / {num_pages}")
            super().showPage()
        super().save()


def draw_background(canvas_obj, doc_obj):
    """Draw dark navy background BEFORE text is rendered."""
    canvas_obj.saveState()
    # Fill dark navy background
    canvas_obj.setFillColor(colors.HexColor('#0A1628'))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    # Top teal accent bar
    canvas_obj.setFillColor(colors.HexColor('#00D4AA'))
    canvas_obj.rect(0, PAGE_HEIGHT - 6, PAGE_WIDTH, 6, fill=1, stroke=0)
    canvas_obj.restoreState()


def create_deck():
    pdf_filename = "SafePay_MENA_Pitch_Deck.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=50,
        rightMargin=50,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=42,
        leading=48,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor('#00D4AA'),
        alignment=1
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1
    )

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=15
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=19,
        textColor=colors.HexColor('#CBD5E1')
    )

    stat_num = ParagraphStyle(
        'StatNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=32,
        textColor=colors.HexColor('#00D4AA'),
        alignment=1
    )

    stat_label = ParagraphStyle(
        'StatLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#00D4AA'),
        spaceAfter=6
    )

    card_text = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#E2E8F0')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#00D4AA')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#E2E8F0')
    )

    story = []

    def add_card_box(data_matrix, col_widths, bg_color='#162036', border_color='#26334D'):
        t = Table(data_matrix, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(border_color)),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return t

    # -------------------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 80))
    story.append(Paragraph("SafePay <font color='#00D4AA'>MENA</font>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("The AI Fraud Shield for Instant Payments", subtitle_style))
    story.append(Spacer(1, 35))
    story.append(Paragraph("Theme 4: Secure Fintech, Payments &amp; Anti-Fraud Innovation &nbsp;|&nbsp; GSMA Open Gateway", meta_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Karim Mohamed Abdelnabi</b>", meta_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 2: THE HOOK
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 90))
    hook_text = ParagraphStyle(
        'HookText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=36,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=1
    )
    story.append(Paragraph('"1.1 billion instant transactions in Egypt.<br/><br/>Every single one is <font color="#EF4444">irreversible</font>.<br/><br/>What happens when the wrong person hits send?"', hook_text))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 3: THE PROBLEM - SCALE
    # -------------------------------------------------------------------------
    story.append(Paragraph("The MENA Payment Boom Has a <font color='#EF4444'>Fraud Problem</font>", slide_title))
    story.append(Spacer(1, 15))

    stats_data = [
        [
            Paragraph("$275.47B", stat_num),
            Paragraph("1.1B", stat_num),
            Paragraph("12.5M", stat_num),
            Paragraph("$469.9M", ParagraphStyle('RedNum', parent=stat_num, textColor=colors.HexColor('#EF4444'))),
            Paragraph("64%", ParagraphStyle('WarnNum', parent=stat_num, textColor=colors.HexColor('#F59E0B')))
        ],
        [
            Paragraph("MENA Digital Payments 2026", stat_label),
            Paragraph("Egypt InstaPay Tx H1'25", stat_label),
            Paragraph("UAE Aani Users", stat_label),
            Paragraph("Saudi Fraud Spend '25", stat_label),
            Paragraph("Arab Adults Unbanked", stat_label)
        ]
    ]

    t_stats = add_card_box(stats_data, [165, 165, 165, 165, 165])
    story.append(t_stats)

    story.append(Spacer(1, 35))
    story.append(Paragraph("• <b>Instant payments = instant fraud risk:</b> Egypt's InstaPay and UAE's Aani process non-refundable push transfers.<br/>• <b>Trust is the barrier:</b> 200M Arab adults remain unbanked. Fraud undermines trust in digital finance.<br/>• <b>Massive investment:</b> Saudi Arabia alone spent $470M on fraud detection infrastructure in 2025.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 4: THE ATTACK - SIM SWAP
    # -------------------------------------------------------------------------
    story.append(Paragraph("How SIM Swap Fraud <font color='#EF4444'>Destroys</font> Accounts", slide_title))
    story.append(Spacer(1, 10))

    attack_flow = [
        [
            Paragraph("<b>Step 1: Social Engineer</b>", card_title),
            Paragraph("<b>Step 2: SIM Swap</b>", card_title),
            Paragraph("<b>Step 3: Intercept OTP</b>", card_title),
            Paragraph("<b>Step 4: Drain Account</b>", ParagraphStyle('RedTitle', parent=card_title, textColor=colors.HexColor('#EF4444')))
        ],
        [
            Paragraph("Fraudster calls carrier: 'I lost my SIM card'", card_text),
            Paragraph("Carrier transfers victim's number to fraudster's SIM", card_text),
            Paragraph("Fraudster receives bank's SMS 2FA codes", card_text),
            Paragraph("Instant transfer drains account. <b>Irreversible.</b>", card_text)
        ]
    ]

    t_attack = add_card_box(attack_flow, [205, 205, 205, 205])
    story.append(t_attack)

    story.append(Spacer(1, 25))
    story.append(Paragraph("• <b>Individual losses:</b> Range from $270 to $160,000+ per SIM swap incident.<br/>• <b>UAE Case:</b> $1.5 million stolen in a single attack combining SIM swap + insider collusion.<br/>• <b>INTERPOL Action:</b> Operation Ramz (2025-2026) arrested 200+ suspects across 13 MENA countries.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 5: ROOT CAUSE - SILOS
    # -------------------------------------------------------------------------
    story.append(Paragraph("The <font color='#EF4444'>Fraud Gap</font>: Banks &amp; Telecoms Don't Talk", slide_title))
    story.append(Spacer(1, 15))

    silo_data = [
        [
            Paragraph("<font color='#3B82F6'>BANK WORLD</font>", card_title),
            Paragraph("<font color='#EF4444'>THE GAP</font>", ParagraphStyle('GapTitle', parent=card_title, textColor=colors.HexColor('#EF4444'), alignment=1)),
            Paragraph("<font color='#3B82F6'>TELECOM WORLD</font>", card_title)
        ],
        [
            Paragraph("• Sees transaction amount, recipient, timestamp<br/><br/><font color='#EF4444'><b>BLIND TO:</b></font><br/>SIM swaps, device changes, roaming status, network-level authentication", card_text),
            Paragraph("<font size=28 color='#EF4444'><b>✕</b></font><br/><br/>No real-time data sharing framework between banks and carriers", ParagraphStyle('GapText', parent=card_text, alignment=1)),
            Paragraph("• Sees SIM swaps, IMEI changes, roaming status, cell tower locations<br/><br/><font color='#EF4444'><b>BLIND TO:</b></font><br/>Bank transfers and payment authorization flows", card_text)
        ]
    ]

    t_silo = add_card_box(silo_data, [350, 140, 350])
    story.append(t_silo)

    story.append(Spacer(1, 25))
    story.append(Paragraph('<i>PwC 2025 GCC Fraud Report: "The critical intelligence gap between telecoms and financial institutions is the #1 vulnerability in digital banking."</i>', ParagraphStyle('ItalicQuote', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 6: THE SOLUTION
    # -------------------------------------------------------------------------
    story.append(Paragraph("SafePay MENA: <font color='#00D4AA'>The Bridge</font>", slide_title))
    story.append(Spacer(1, 10))

    story.append(Paragraph("An AI agent that asks the telecom network <b>'Is this person legit?'</b> before every high-risk payment.", ParagraphStyle('SolSub', parent=body_style, fontSize=16, leading=22, alignment=1, textColor=colors.HexColor('#FFFFFF'))))
    story.append(Spacer(1, 20))

    sol_grid = [
        [
            Paragraph("<b>Detect</b>", card_title),
            Paragraph("<b>Decide</b>", card_title),
            Paragraph("<b>Defend</b>", card_title)
        ],
        [
            Paragraph("Queries 4 CAMARA APIs via Nokia Network-as-Code for real-time carrier intelligence.", card_text),
            Paragraph("AI Agent (Google ADK + Gemini Flash) weighs signals into a risk score (0-100).", card_text),
            Paragraph("Autonomous decision: APPROVE (silent), STEP-UP, or BLOCK - before money moves.", card_text)
        ]
    ]

    t_sol = add_card_box(sol_grid, [275, 275, 275], bg_color='#111D33', border_color='#00D4AA')
    story.append(t_sol)

    story.append(Spacer(1, 25))
    story.append(Paragraph("• <b>Zero friction:</b> Low-risk payments proceed silently without user interaction.<br/>• <b>Carrier-level security:</b> Replaces interceptable SMS OTPs with silent network authentication.<br/>• <b>Audit trail:</b> Generates natural-language reasoning for regulatory compliance.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 7: 4 CAMARA APIs
    # -------------------------------------------------------------------------
    story.append(Paragraph("4 CAMARA APIs. One <font color='#00D4AA'>Intelligent</font> Decision.", slide_title))
    story.append(Spacer(1, 10))

    api_table_data = [
        [Paragraph("API", table_header), Paragraph("Endpoint", table_header), Paragraph("Fraud Signal Checked", table_header), Paragraph("Weight", table_header)],
        [
            Paragraph("<b>SIM Swap</b>", table_cell),
            Paragraph("<code>POST /sim-swap/v0/check</code>", table_cell),
            Paragraph("Was SIM card swapped recently? <font color='#EF4444'>Swapped &lt;24h = RED FLAG</font>", table_cell),
            Paragraph("<b>35%</b>", ParagraphStyle('W1', parent=table_cell, textColor=colors.HexColor('#00D4AA')))
        ],
        [
            Paragraph("<b>Number Verification</b>", table_cell),
            Paragraph("<code>POST /number-verification/v0/verify</code>", table_cell),
            Paragraph("Silent carrier auth: does device match phone number? Replaces SMS OTP.", table_cell),
            Paragraph("<b>30%</b>", ParagraphStyle('W2', parent=table_cell, textColor=colors.HexColor('#00D4AA')))
        ],
        [
            Paragraph("<b>Device Status</b>", table_cell),
            Paragraph("<code>POST /device-status/v0/roaming</code>", table_cell),
            Paragraph("Is device reachable? Is it roaming in an unexpected country?", table_cell),
            Paragraph("<b>15%</b>", ParagraphStyle('W3', parent=table_cell, textColor=colors.HexColor('#00D4AA')))
        ],
        [
            Paragraph("<b>Device Swap</b>", table_cell),
            Paragraph("<code>POST /device-swap/v0/check</code>", table_cell),
            Paragraph("Was SIM moved to a new physical handset (different IMEI)?", table_cell),
            Paragraph("<b>20%</b>", ParagraphStyle('W4', parent=table_cell, textColor=colors.HexColor('#00D4AA')))
        ]
    ]

    t_api = Table(api_table_data, colWidths=[140, 240, 350, 100])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#162036')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0A1628')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#26334D')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_api)

    story.append(Spacer(1, 15))
    story.append(Paragraph("All APIs accessed via <b>Nokia Network-as-Code</b> platform using official Python SDK.", ParagraphStyle('ApiSub', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 8: AI AGENT DESIGN
    # -------------------------------------------------------------------------
    story.append(Paragraph("Not a Pipeline. An <font color='#00D4AA'>Agent</font>.", slide_title))
    story.append(Spacer(1, 10))

    compare_data = [
        [Paragraph("Rule-Based Pipeline ❌", ParagraphStyle('CT1', parent=card_title, textColor=colors.HexColor('#EF4444'))), Paragraph("SafePay AI Agent ✅", card_title)],
        [
            Paragraph("• Calls ALL APIs on every transaction<br/>• Fixed if/else decision tree<br/>• Returns generic pass/fail<br/>• Same behavior for $10 and $50,000<br/>• Cannot handle edge cases or context", card_text),
            Paragraph("• <b>Plans:</b> Decides WHICH APIs to call based on risk context<br/>• <b>Reasons:</b> Weighs multiple signals dynamically<br/>• <b>Explains:</b> Generates natural-language reasoning trace<br/>• <b>Adapts:</b> Low-risk = 1 check; High-risk = 4 checks<br/>• <b>Approved tooling:</b> Built with Google ADK + Gemini 2.0 Flash", card_text)
        ]
    ]

    t_compare = add_card_box(compare_data, [415, 415])
    story.append(t_compare)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 9: THREE SCENARIOS
    # -------------------------------------------------------------------------
    story.append(Paragraph("Three Scenarios. Three <font color='#00D4AA'>Decisions</font>.", slide_title))
    story.append(Spacer(1, 10))

    scen_data = [
        [
            Paragraph("<b>Scenario A: Normal</b>", ParagraphStyle('SA', parent=card_title, textColor=colors.HexColor('#22C55E'))),
            Paragraph("<b>Scenario B: Attack</b>", ParagraphStyle('SB', parent=card_title, textColor=colors.HexColor('#EF4444'))),
            Paragraph("<b>Scenario C: Ambiguous</b>", ParagraphStyle('SC', parent=card_title, textColor=colors.HexColor('#F59E0B')))
        ],
        [
            Paragraph("<b>Tx:</b> 500 EGP to Mom (2 PM)<br/><br/>SIM Swap: No (0.0)<br/>Num Verify: Match (0.0)<br/>Context: Known recipient (0.05)<br/><br/><font size=20 color='#22C55E'><b>Score: 1 / 100</b></font><br/><br/><font color='#22C55E'><b>✅ APPROVE (silent)</b></font>", card_text),
            Paragraph("<b>Tx:</b> 45,000 EGP to stranger (4 AM)<br/><br/>SIM Swap: 3h ago (1.0)<br/>Num Verify: FAILED (1.0)<br/>Roaming: Nigeria (0.7)<br/><br/><font size=20 color='#EF4444'><b>Score: 93 / 100</b></font><br/><br/><font color='#EF4444'><b>🛑 BLOCK + ALERT</b></font>", card_text),
            Paragraph("<b>Tx:</b> 8,000 EGP to new contact (11 AM)<br/><br/>SIM Swap: 5 days ago (0.5)<br/>Num Verify: Match (0.0)<br/>Context: New recipient (0.3)<br/><br/><font size=20 color='#F59E0B'><b>Score: 24 / 100</b></font><br/><br/><font color='#22C55E'><b>✅ APPROVE (legit swap)</b></font>", card_text)
        ]
    ]

    t_scen = add_card_box(scen_data, [275, 275, 275])
    story.append(t_scen)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 10: ARCHITECTURE
    # -------------------------------------------------------------------------
    story.append(Paragraph("Technical <font color='#00D4AA'>Architecture</font>", slide_title))
    story.append(Spacer(1, 10))

    arch_boxes = [
        [
            Paragraph("<b>Payment Platform</b>", card_title),
            Paragraph("<b>SafePay Backend + Agent</b>", card_title),
            Paragraph("<b>Nokia NaC Sandbox</b>", card_title)
        ],
        [
            Paragraph("InstaPay / Aani / stc pay<br/><br/>Sends transaction JSON", card_text),
            Paragraph("<b>FastAPI + Google ADK + Gemini Flash</b><br/><br/>Orchestrates APIs &amp; Risk Scoring Engine", card_text),
            Paragraph("4 CAMARA APIs<br/><br/>Provides network signals", card_text)
        ]
    ]

    t_arch = add_card_box(arch_boxes, [275, 275, 275])
    story.append(t_arch)

    story.append(Spacer(1, 15))

    arch_bottom = [
        [Paragraph("<b>Supabase (PostgreSQL)</b>", card_title), Paragraph("<b>Next.js Frontend Dashboard</b>", card_title)],
        [Paragraph("Audit Log table (decision traces) + User Profiles table", card_text), Paragraph("Real-time risk gauge + Agent reasoning trace viewer", card_text)]
    ]

    t_arch_b = add_card_box(arch_bottom, [415, 415])
    story.append(t_arch_b)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 11: MARKET OPPORTUNITY
    # -------------------------------------------------------------------------
    story.append(Paragraph("Market <font color='#00D4AA'>Opportunity</font>", slide_title))
    story.append(Spacer(1, 15))

    mkt_data = [
        [
            Paragraph("<b>TAM</b>", card_title),
            Paragraph("<b>SAM</b>", card_title),
            Paragraph("<b>SOM</b>", card_title)
        ],
        [
            Paragraph("<font size=24 color='#00D4AA'><b>$275.47B</b></font><br/><br/>MENA Digital Payments Market (2026)", card_text),
            Paragraph("<font size=24 color='#3B82F6'><b>$6.35B</b></font><br/><br/>MENA Fintech Market Size (2026)", card_text),
            Paragraph("<font size=24 color='#00D4AA'><b>$44M</b></font><br/><br/>Egypt InstaPay alone at $0.02/check", card_text)
        ]
    ]

    t_mkt = add_card_box(mkt_data, [275, 275, 275])
    story.append(t_mkt)

    story.append(Spacer(1, 25))
    story.append(Paragraph("• <b>22 MENA Markets:</b> Every Arab League country + Turkiye has expanding digital payment systems.<br/>• <b>80+ Operators:</b> Globally committed to Open Gateway, making carrier-agnostic deployment seamless.<br/>• <b>Growth Runway:</b> Reducing fraud unlocks financial inclusion for 200 million unbanked Arabs.", body_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 12: BUSINESS MODEL
    # -------------------------------------------------------------------------
    story.append(Paragraph("Business <font color='#00D4AA'>Model</font>", slide_title))
    story.append(Spacer(1, 15))

    bm_data = [
        [Paragraph("Per-Transaction Fee", card_title), Paragraph("Monthly Subscription", card_title), Paragraph("Enterprise License", card_title)],
        [
            Paragraph("<font size=22 color='#00D4AA'><b>$0.01 - $0.05</b></font><br/><br/>Per fraud check.<br/>Paid by banks &amp; fintechs.", card_text),
            Paragraph("<font size=22 color='#00D4AA'><b>$500 - $5,000</b></font><br/><br/>Monthly tiered by volume.<br/>Mid-size banks &amp; wallets.", card_text),
            Paragraph("<font size=22 color='#00D4AA'><b>$50K - $200K</b></font><br/><br/>Annual license.<br/>Central banks &amp; large banks.", card_text)
        ]
    ]

    t_bm = add_card_box(bm_data, [275, 275, 275])
    story.append(t_bm)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Unit Economics:</b> Cost of fraud = $270 - $160,000+ per incident. Cost of SafePay check = &lt;$0.01 on Nokia NaC. SafePay pays for itself if it prevents just <b>1 fraud case per 10,000 transactions</b>.", ParagraphStyle('BmSub', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 13: IMPACT & SCALABILITY
    # -------------------------------------------------------------------------
    story.append(Paragraph("Impact &amp; <font color='#00D4AA'>Scalability</font>", slide_title))
    story.append(Spacer(1, 15))

    imp_data = [
        [Paragraph("Quantified Impact (Pilot Data)", card_title), Paragraph("Scalability Blueprint", card_title)],
        [
            Paragraph("• <b>-44% Scam Losses:</b> Proven in early CAMARA global pilot deployments.<br/>• <b>-55% False Positives:</b> Fewer legitimate transfers blocked unnecessarily.<br/>• <b>&lt;$0.01 Cost per Check:</b> Highly economical compared to $15-25 manual investigations.<br/>• <b>$270-$160K Saved:</b> Per prevented SIM swap attack.", card_text),
            Paragraph("• <b>Carrier-Agnostic:</b> CAMARA standards mean 1 integration works across e&amp;, stc, Ooredoo, Vodafone.<br/>• <b>Payment-Agnostic:</b> Integrates with InstaPay, Aani, stc pay, Fawry.<br/>• <b>200M Unbanked:</b> Fraud prevention builds the trust needed for digital onboarding.", card_text)
        ]
    ]

    t_imp = add_card_box(imp_data, [415, 415])
    story.append(t_imp)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 14: COMPETITIVE ADVANTAGE
    # -------------------------------------------------------------------------
    story.append(Paragraph("Why SafePay <font color='#00D4AA'>Wins</font>", slide_title))
    story.append(Spacer(1, 15))

    comp_data = [
        [Paragraph("What Exists Today", table_header), Paragraph("The Unsolved Missing Link", table_header), Paragraph("SafePay MENA", table_header)],
        [
            Paragraph("Individual CAMARA API launches (e&amp; UAE, Ooredoo Qatar)", table_cell),
            Paragraph("<font color='#EF4444'>No intelligent orchestration layer</font>", table_cell),
            Paragraph("<b>Multi-API AI Agent</b> that weighs signals together", table_cell)
        ],
        [
            Paragraph("Bank transaction monitoring systems", table_cell),
            Paragraph("<font color='#EF4444'>Zero telecom network signals</font>", table_cell),
            Paragraph("<b>Bridges the fraud gap</b> between banks &amp; carriers", table_cell)
        ],
        [
            Paragraph("SMS OTP for authentication", table_cell),
            Paragraph("<font color='#EF4444'>Interceptable, weakest link</font>", table_cell),
            Paragraph("<b>Carrier Number Verification</b> (silent &amp; unforgeable)", table_cell)
        ],
        [
            Paragraph("GSMA + FICO Scam Signal specification", table_cell),
            Paragraph("<font color='#EF4444'>Specification stage, not deployed</font>", table_cell),
            Paragraph("<b>Working prototype</b> with 4 integrated APIs", table_cell)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[260, 270, 300])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#162036')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0A1628')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#26334D')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_comp)

    story.append(Spacer(1, 20))
    story.append(Paragraph('<i>"The telecom APIs exist individually. SafePay is the intelligent brain that orchestrates them."</i>', ParagraphStyle('WinQuote', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 15: CALL TO ACTION
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 60))
    cta_title = ParagraphStyle(
        'CtaTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=34,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=1
    )
    story.append(Paragraph("The technology exists.<br/>The market is screaming for it.<br/><br/><font color='#00D4AA' size=28>SafePay is the bridge between $275 billion in payments<br/>and the network that can protect them.</font>", cta_title))

    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>Karim Mohamed Abdelnabi</b>", ParagraphStyle('CtaAuthor', parent=meta_style, fontSize=14, leading=20)))

    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background, canvasmaker=NumberedCanvas)
    print(f"Generated FIXED pitch deck PDF: {pdf_filename}")

if __name__ == '__main__':
    create_deck()
