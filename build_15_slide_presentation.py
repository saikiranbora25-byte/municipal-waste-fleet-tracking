# -*- coding: utf-8 -*-
"""
15-Slide Presentation Generator for CivicClean Fleet Tracking & Route Verification System
Accurately follows the design, aesthetic, and layout of Smart_Parking_Project_Presentation_10_Slides.pptx
Author: Saikiran Bora (A24126510006) | Branch: CSE, Section - A | ANITS
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Exact Palette from Reference Presentation
C_NAVY       = RGBColor(13, 34, 64)      # #0D2240 (Slide 1 background, Headings)
C_STEEL      = RGBColor(54, 111, 145)    # #366F91 (Primary accent, Top bar)
C_TEAL       = RGBColor(33, 123, 146)    # #217B92 (Secondary accent)
C_ICE        = RGBColor(216, 231, 241)   # #D8E7F1 (Card fill tint)
C_WHITE      = RGBColor(255, 255, 255)   # #FFFFFF
C_BORDER     = RGBColor(204, 216, 226)   # #CCD8E2 (Card border, divider lines)
C_TITLE      = RGBColor(13, 34, 64)      # #0D2240 (Main titles)
C_SUBTITLE   = RGBColor(95, 104, 112)    # #5F6870 (Muted subtitles & footer)
C_BODY       = RGBColor(36, 42, 48)      # #242A30 (Charcoal body text - 12pt)
C_ACCENT_BG  = RGBColor(241, 245, 249)   # #F1F5F9 (Light gray tint)
C_GREEN      = RGBColor(22, 101, 52)     # #166534 (Pass/Verified)
C_GREEN_BG   = RGBColor(240, 253, 244)   # #F0FDF4
C_RED        = RGBColor(185, 28, 28)     # #B91C1C (Danger/Fallacy)
C_RED_BG     = RGBColor(254, 242, 242)   # #FEF2F2
C_AMBER      = RGBColor(180, 83, 9)      # #B45309 (Warning/Obstruction)
C_AMBER_BG   = RGBColor(254, 243, 199)   # #FEF3C7

def add_header(slide, title_text, subtitle_text, slide_num):
    # Top Accent Bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_STEEL
    top_bar.line.fill.background()

    # Slide Title
    t_box = slide.shapes.add_textbox(Inches(0.67), Inches(0.40), Inches(11.94), Inches(0.50))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Aptos"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TITLE

    # Slide Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.68), Inches(0.98), Inches(11.88), Inches(0.35))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.name = "Aptos"
    p_s.font.size = Pt(12)
    p_s.font.color.rgb = C_SUBTITLE

    # Bottom Divider Line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.67), Inches(6.98), Inches(12.00), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = C_BORDER
    div.line.fill.background()

    # Footer Left Text
    fl_box = slide.shapes.add_textbox(Inches(0.68), Inches(7.05), Inches(9.72), Inches(0.25))
    tf_fl = fl_box.text_frame
    p_fl = tf_fl.paragraphs[0]
    p_fl.text = "CIVICCLEAN  |  GPS FLEET TRACKING & ROUTE VERIFICATION"
    p_fl.font.name = "Aptos"
    p_fl.font.size = Pt(9)
    p_fl.font.bold = True
    p_fl.font.color.rgb = C_SUBTITLE

    # Footer Right Slide Number
    fr_box = slide.shapes.add_textbox(Inches(12.00), Inches(7.03), Inches(0.65), Inches(0.25))
    tf_fr = fr_box.text_frame
    p_fr = tf_fr.paragraphs[0]
    p_fr.alignment = PP_ALIGN.RIGHT
    p_fr.text = f"{slide_num:02d}"
    p_fr.font.name = "Aptos"
    p_fr.font.size = Pt(10)
    p_fr.font.color.rgb = C_SUBTITLE

def add_card(slide, left, top, width, height, title="", fill_color=C_ICE, border_color=C_BORDER, title_color=C_TITLE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.0)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.20)
    tf.margin_right = Inches(0.20)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.18)
    
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Aptos"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(4)
    return card, tf

def add_callout(slide, text, prefix="Boundary: "):
    c_box = slide.shapes.add_textbox(Inches(0.68), Inches(6.45), Inches(11.95), Inches(0.40))
    tf = c_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    
    r1 = p.add_run()
    r1.text = prefix
    r1.font.name = "Aptos"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = C_TITLE

    r2 = p.add_run()
    r2.text = text
    r2.font.name = "Aptos"
    r2.font.size = Pt(12)
    r2.font.color.rgb = C_BODY

# ==============================================================================
# SLIDE 1: TITLE SLIDE (Exact Smart Parking Cover Aesthetic)
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_NAVY
bg1.line.fill.background()

# Decorative Ovals (Reference exact positions)
ov1 = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.58), Inches(-1.32), Inches(5.21), Inches(5.21))
ov1.fill.solid()
ov1.fill.fore_color.rgb = C_STEEL
ov1.line.fill.background()

ov2 = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.83), Inches(4.44), Inches(3.12), Inches(3.12))
ov2.fill.solid()
ov2.fill.fore_color.rgb = C_TEAL
ov2.line.fill.background()

# ANITS College Logo in top right
logo_path = 'report_assets/anits_logo.jpeg'
if os.path.exists(logo_path):
    slide1.shapes.add_picture(logo_path, Inches(11.35), Inches(0.65), width=Inches(1.2))

# Category Tag
cat1 = slide1.shapes.add_textbox(Inches(0.88), Inches(0.78), Inches(8.61), Inches(0.28))
p_cat = cat1.text_frame.paragraphs[0]
p_cat.text = "SOFTWARE ENGINEERING  |  MINI PROJECT"
p_cat.font.name = "Aptos"
p_cat.font.size = Pt(13)
p_cat.font.bold = True
p_cat.font.color.rgb = RGBColor(164, 194, 215) # #A4C2D7

# Main Title
t1 = slide1.shapes.add_textbox(Inches(0.83), Inches(1.50), Inches(9.72), Inches(0.85))
p_t1 = t1.text_frame.paragraphs[0]
p_t1.text = "CIVICCLEAN"
p_t1.font.name = "Aptos Display"
p_t1.font.size = Pt(44)
p_t1.font.bold = True
p_t1.font.color.rgb = C_WHITE

# Subtitle
sub1 = slide1.shapes.add_textbox(Inches(0.88), Inches(2.45), Inches(9.03), Inches(0.55))
p_sub = sub1.text_frame.paragraphs[0]
p_sub.text = "GPS Fleet Tracking & Route Verification Platform"
p_sub.font.name = "Aptos"
p_sub.font.size = Pt(25)
p_sub.font.color.rgb = RGBColor(240, 228, 217) # #F0E4D9

# Tagline
tag1 = slide1.shapes.add_textbox(Inches(0.90), Inches(3.15), Inches(9.20), Inches(0.65))
p_tag = tag1.text_frame.paragraphs[0]
p_tag.text = "A browser-based, zero-hardware platform for municipal solid waste logistics, driver verification, and citizen grievances."
p_tag.font.name = "Aptos"
p_tag.font.size = Pt(13)
p_tag.font.color.rgb = C_WHITE

# Divider Line
conn1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.90), Inches(4.00), Inches(6.00), Inches(0.015))
conn1.fill.solid()
conn1.fill.fore_color.rgb = RGBColor(164, 194, 215)
conn1.line.fill.background()

# Student Details
st1 = slide1.shapes.add_textbox(Inches(0.90), Inches(4.25), Inches(8.50), Inches(0.40))
p_st1 = st1.text_frame.paragraphs[0]
p_st1.text = "Saikiran Bora  |  A24126510006"
p_st1.font.name = "Aptos"
p_st1.font.size = Pt(17)
p_st1.font.bold = True
p_st1.font.color.rgb = C_WHITE

st2 = slide1.shapes.add_textbox(Inches(0.90), Inches(4.75), Inches(9.50), Inches(0.35))
p_st2 = st2.text_frame.paragraphs[0]
p_st2.text = "Department of Computer Science and Engineering  •  ANITS (UGC Autonomous)"
p_st2.font.name = "Aptos"
p_st2.font.size = Pt(12)
p_st2.font.color.rgb = RGBColor(240, 228, 217)

st3 = slide1.shapes.add_textbox(Inches(0.90), Inches(5.15), Inches(9.50), Inches(0.35))
p_st3 = st3.text_frame.paragraphs[0]
p_st3.text = "B.Tech III Year, Section - A  •  Course: 23CS4219 Software Engineering Lab  •  2026–2027"
p_st3.font.name = "Aptos"
p_st3.font.size = Pt(11)
p_st3.font.color.rgb = RGBColor(240, 228, 217)

st4 = slide1.shapes.add_textbox(Inches(0.90), Inches(5.55), Inches(9.50), Inches(0.35))
p_st4 = st4.text_frame.paragraphs[0]
p_st4.text = "Project Guide: Prof. A. Rohini (Faculty Incharge)  •  HOD: Prof. G. Srinivas (Dept. of CSE)"
p_st4.font.name = "Aptos"
p_st4.font.size = Pt(11)
p_st4.font.color.rgb = RGBColor(240, 228, 217)

# Bottom Badge
bot1 = slide1.shapes.add_textbox(Inches(0.90), Inches(7.10), Inches(11.39), Inches(0.25))
p_bot1 = bot1.text_frame.paragraphs[0]
p_bot1.text = "ZERO-HARDWARE ARCHITECTURE  •  COMMODITY SMARTPHONE SENSING & 15M GEOFENCING"
p_bot1.font.name = "Aptos"
p_bot1.font.size = Pt(9.5)
p_bot1.font.bold = True
p_bot1.font.color.rgb = RGBColor(164, 194, 215)

print("Slide 1 generated.")

# ==============================================================================
# SLIDE 2: MUNICIPAL WASTE PROBLEM, OBJECTIVES & SCOPE (Reference Slide 2 Pattern)
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Municipal waste problem, objectives & scope",
           "The platform brings real-time fleet tracking, proof-of-service verification and citizen grievance logging into one browser application.", 1)

# Top 3 Problem Cards
prob_data = [
    ("Limited visibility", "Supervisors cannot verify truck locations, speed or bin coverage in real time."),
    ("Manual operations", "Paper sheets permit post-shift falsification with zero verifiability of actual visits."),
    ("Disconnected loop", "Residents discover unserviced bins days later with no formal tracking channel.")
]
for idx, (title, desc) in enumerate(prob_data):
    cx = Inches(0.68 + idx * 4.05)
    card, tf = add_card(slide2, cx, Inches(1.65), Inches(3.85), Inches(1.85), title, fill_color=C_ICE, border_color=C_BORDER)
    p = tf.add_paragraph()
    p.text = desc
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY

# Bottom 2 Cards (Implemented vs Out of Scope)
c_imp, tf_imp = add_card(slide2, Inches(0.68), Inches(3.70), Inches(5.88), Inches(2.55), "Implemented (Solution 2)",
                         fill_color=C_WHITE, border_color=C_BORDER)
imp_points = [
    "Real-time GPS fleet tracking on interactive Leaflet GIS map",
    "Touch-optimized driver mobile manifest with 15m geofencing lock",
    "Tamper-resistant proof-of-service logs with coordinate & time hashes",
    "Crowdsourced citizen grievance portal with one-tap phone GPS pin-drop",
    "Public ward collection timetable roster for community visibility"
]
for pt in imp_points:
    p = tf_imp.add_paragraph()
    p.text = f"• {pt}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(2)

c_out, tf_out = add_card(slide2, Inches(6.80), Inches(3.70), Inches(5.88), Inches(2.55), "Out of scope (Deliberate Hardware Omission)",
                         fill_color=C_WHITE, border_color=C_BORDER)
out_points = [
    "No physical ultrasonic level sensors mounted inside roadside bins",
    "No proprietary OBD-II vehicle tracking hardware or dashboard retrofits",
    "No dedicated LoRaWAN gateways or physical transmission towers",
    "No vehicle weighbridge hardware (relies on driver volumetric heuristics)",
    "No multi-instance database in demo (single-process in-memory store)"
]
for pt in out_points:
    p = tf_out.add_paragraph()
    p.text = f"• {pt}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(2)

add_callout(slide2, "all tracked coordinates utilize driver smartphone GPS and web APIs—requiring zero hardware sensors mounted on physical bins.", prefix="Boundary: ")

# ==============================================================================
# SLIDE 3: THE IOT SENSOR FALLACY VS. SOFTWARE REALITY (Deep Justification)
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "The IoT sensor fallacy vs. software reality",
           "Why dedicated hardware in-bin sensors consistently fail in municipal deployments, and why software solves the root cause.", 2)

# Left: IoT Sensor Fallacy
c_fail, tf_fail = add_card(slide3, Inches(0.68), Inches(1.65), Inches(5.88), Inches(4.60),
                           "The Fallacy of Dedicated IoT Hardware (Solution 1)",
                           fill_color=C_RED_BG, border_color=C_RED, title_color=C_RED)
fail_points = [
    ("Prohibitive Capital Outlay (CapEx):", "Procuring thousands of ultrasonic level sensors and LoRa gateways costs crores in municipal funds (≈ ₹5,000 per bin)."),
    ("Rampant Vandalism & Theft:", "Sensors mounted in public roadside bins are stolen by scavengers or smashed by hydraulic compactor arms during lifting."),
    ("Corrosive Chemical Damage:", "Acidic leachate fluids, heavy monsoon moisture, and methane gas rapidly corrode exposed electronic circuitry."),
    ("Crushing Battery Maintenance (OpEx):", "Replacing lithium batteries across thousands of dispersed city bins creates an unsustainable recurring operational burden.")
]
for lbl, desc in fail_points:
    p = tf_fail.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

# Right: The Software-First Reality
c_real, tf_real = add_card(slide3, Inches(6.80), Inches(1.65), Inches(5.88), Inches(4.60),
                           "The Software-First Reality (Solution 2 - Proposed)",
                           fill_color=C_GREEN_BG, border_color=C_GREEN, title_color=C_GREEN)
real_points = [
    ("Zero Hardware Procurement Cost:", "Leverages drivers' existing commodity Android/iOS smartphones already carried inside the truck cab."),
    ("Protected Environmental Envelope:", "The sensing device remains safely inside the vehicle cab, 100% immune to trash leachate, weather, and roadside vandalism."),
    ("Over-The-Air Software Updates:", "Zero physical bin visits or battery swaps required; application updates deploy instantly across all vehicles via web standards."),
    ("Crowdsourced Civic Sensing:", "Citizens act as distributed visual sensors, reporting overflowing bins with phone cameras and GPS pins for targeted collection.")
]
for lbl, desc in real_points:
    p = tf_real.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

add_callout(slide3, "Municipal solid waste collection fails due to the lack of a real-time digital feedback loop—not a lack of electronic chips in bins.", prefix="Root Cause: ")

# ==============================================================================
# SLIDE 4: STRATEGIC JUSTIFICATION: SOLUTION 1 VS. SOLUTION 2
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Strategic justification: Solution 1 vs. Solution 2",
           "Comprehensive engineering and financial evaluation of hardware sensors versus driver-centric GPS tracking.", 3)

# Comparison Table (4 cols x 8 rows)
t_shape = slide4.shapes.add_table(rows=8, cols=4, left=Inches(0.68), top=Inches(1.65), width=Inches(12.00), height=Inches(4.55))
t = t_shape.table
t.columns[0].width = Inches(2.70)
t.columns[1].width = Inches(2.80)
t.columns[2].width = Inches(3.20)
t.columns[3].width = Inches(3.30)

tbl_headers = ["Evaluation Metric", "Legacy Manual System", "IoT Bin Sensors (Solution 1)", "CivicClean Software (Solution 2)"]
for i, h in enumerate(tbl_headers):
    cell = t.cell(0, i)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_STEEL if i == 3 else C_ICE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Aptos"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE if i == 3 else C_TITLE

matrix_rows = [
    ("Hardware Procurement Cost", "Zero (Paper sheets)", "Extremely High (₹5,000 / bin)", "ZERO (Uses existing smartphones)"),
    ("Vandalism & Theft Risk", "Not Applicable", "High Risk (Stolen / smashed)", "ZERO RISK (Device stays in truck cab)"),
    ("Maintenance & Battery Overhead", "Low (Manual entry)", "Very High (Recurring battery swaps)", "LOW (Over-the-air web app updates)"),
    ("Proof-of-Service Verification", "0% (Paper falsification common)", "Partial (Detects fill level only)", "100% (15m GPS + Photo Proof)"),
    ("Obstruction / Skip Logging", "None (Bins bypassed silently)", "None (Sensors cannot detect obstacles)", "Automated (Categorized driver reasons)"),
    ("Citizen Engagement Channel", "Nil (Delayed phone complaints)", "Nil (Closed hardware network)", "Direct Active Crowdsourcing Portal"),
    ("Municipal Ward Scalability", "Inherently Inefficient", "Difficult (Requires physical installs)", "INSTANT (Deployable across any ward)")
]

for r_idx, r_data in enumerate(matrix_rows):
    for c_idx, val in enumerate(r_data):
        cell = t.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        if c_idx == 3:
            cell.fill.fore_color.rgb = RGBColor(239, 246, 255)
        else:
            cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_ACCENT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Aptos"
        p.font.size = Pt(11)
        if c_idx == 3:
            p.font.bold = True
            p.font.color.rgb = C_STEEL
        else:
            p.font.color.rgb = C_BODY

add_callout(slide4, "Solution 2 delivers 100% of municipal route verifiability at <5% of the capital expenditure of physical sensor deployments.", prefix="Justification: ")

# ==============================================================================
# SLIDE 5: A SINGLE PLATFORM WITH THREE OPERATING ROLES (Reference Slide 3 Pattern)
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "A single platform with three operating roles",
           "Driver mobile manifest, supervisor GIS command hub, and public citizen portal sharing a unified data model.", 4)

roles_data = [
    ("Field Driver Manifest",
     "Touch-optimized mobile PWA for drivers\n"
     "\u2022 Continuous GPS satellite accuracy lock\n"
     "\u2022 15m geofenced collection verification\n"
     "\u2022 One-tap camera photo evidence capture\n"
     "\u2022 Structured road skip exception logging\n"
     "\u2022 Dynamic route completion percentage",
     C_STEEL),
    ("Supervisor Command Hub",
     "Desktop GIS monitoring & auditing\n"
     "\u2022 Interactive Leaflet map with truck telemetry\n"
     "\u2022 Real-time speed (24 km/h) & heading display\n"
     "\u2022 Dynamic ward collection completion gauge\n"
     "\u2022 Instant route deviation & delay alerts\n"
     "\u2022 Immutable tamper-resistant audit trail",
     C_TEAL),
    ("Citizen Grievance Portal",
     "Public crowdsourced accountability\n"
     "\u2022 One-tap smartphone GPS pin-drop placement\n"
     "\u2022 Overflowing garbage photo evidence upload\n"
     "\u2022 3-stage live ticket tracker (#CMP-2026-104)\n"
     "\u2022 Public ward collection timetable roster\n"
     "\u2022 Frictionless submission (zero login wall)",
     C_NAVY)
]

for idx, (title, body, col) in enumerate(roles_data):
    cx = Inches(0.68 + idx * 4.05)
    card, tf = add_card(slide5, cx, Inches(1.65), Inches(3.85), Inches(4.60), title, fill_color=C_ICE, border_color=C_BORDER, title_color=col)
    lines = body.split('\n')
    # First line subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = lines[0].encode('utf-8').decode('unicode_escape')
    p_sub.font.name = "Aptos"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_TITLE
    p_sub.space_after = Pt(6)
    
    for l in lines[1:]:
        p = tf.add_paragraph()
        p.text = l.encode('utf-8').decode('unicode_escape')
        p.font.name = "Aptos"
        p.font.size = Pt(12)
        p.font.color.rgb = C_BODY
        p.space_after = Pt(4)

add_callout(slide5, "Drivers and citizens access role-specific views; only authenticated sanitation supervisors access administrative audit logs.", prefix="Security Boundary: ")

print("Slides 2 to 5 generated.")

# ==============================================================================
# SLIDE 6: SYSTEM ARCHITECTURE (Reference Slide 4 Pattern)
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "System architecture",
           "Layered Node.js application utilizing browser-native client interfaces, RESTful services, and an in-memory telemetry state store.", 5)

# 4 Layer Cards across top
layer_data = [
    ("Client UI", "HTML5 • CSS3\nVanilla JS • Leaflet GIS"),
    ("HTTP Server", "Node.js built-ins\nExpress REST API Gateway"),
    ("Domain Logic", "Haversine Geofencing\nProof & Exception Engine"),
    ("State Store", "In-Memory Telemetry Cache\nImmutable Audit Log Store")
]
for idx, (title, sub) in enumerate(layer_data):
    cx = Inches(0.68 + idx * 3.05)
    card, tf = add_card(slide6, cx, Inches(1.60), Inches(2.85), Inches(1.20), title, fill_color=C_ICE, border_color=C_STEEL)
    for l in sub.split('\n'):
        p = tf.add_paragraph()
        p.text = l
        p.font.name = "Aptos"
        p.font.size = Pt(11)
        p.font.color.rgb = C_BODY

# Bottom Half: Diagram on Left, Deployment Card on Right
arch_img = 'report_assets/system_architecture.png'
if os.path.exists(arch_img):
    slide6.shapes.add_picture(arch_img, Inches(0.68), Inches(2.95), width=Inches(5.85))

c_dep, tf_dep = add_card(slide6, Inches(6.80), Inches(2.95), Inches(5.88), Inches(3.35), "Deployment & Runtime Boundary",
                         fill_color=C_WHITE, border_color=C_BORDER)
dep_points = [
    "Containerized Docker / Node.js 20+ runtime with sub-250ms API latency",
    "Responsive single-codebase web application accessible on any Android/iOS browser",
    "Lightweight in-memory telemetry state engine for sub-second GPS position caching",
    "Cloud-ready architecture easily deployed to Streamlit Community Cloud or Render",
    "Strict client-server boundary: vehicle sensors operate strictly on client edge"
]
for pt in dep_points:
    p = tf_dep.add_paragraph()
    p.text = f"• {pt}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(4)

add_callout(slide6, "In-memory store provides sub-millisecond vehicle updates; production scaling bridges to PostgreSQL/PostGIS.", prefix="Architectural Trade-off: ")

# ==============================================================================
# SLIDE 7: TWO CORE OPERATIONAL WORKFLOWS (Reference Slide 5 Arrow Pattern)
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Two core operational workflows",
           "Driver collection manifest tracks physical route progress; citizen grievance portal crowdsources unserviced hotspots.", 6)

# Section 1 Header
h1_box = slide7.shapes.add_textbox(Inches(0.68), Inches(1.55), Inches(8.0), Inches(0.30))
p_h1 = h1_box.text_frame.paragraphs[0]
p_h1.text = "FIELD COLLECTION & PROOF-OF-SERVICE WORKFLOW"
p_h1.font.name = "Aptos"
p_h1.font.size = Pt(12)
p_h1.font.bold = True
p_h1.font.color.rgb = C_STEEL

# Pipeline 1 (4 Steps)
wf1_steps = [
    ("1  Dispatch truck", "Driver starts shift;\nGPS stream begins"),
    ("2  Arrive at bin", "Haversine check\nvalidates <=15m radius"),
    ("3  Verify service", "Photo capture unlocks;\nproof hash recorded"),
    ("4  Update status", "Stop turns green;\nroute counter advances")
]
for i, (st_t, st_b) in enumerate(wf1_steps):
    bx = Inches(0.68 + i * 3.05)
    card, tf = add_card(slide7, bx, Inches(1.90), Inches(2.65), Inches(1.45), st_t, fill_color=C_ICE, border_color=C_STEEL)
    tf.paragraphs[0].font.size = Pt(13.5)
    for l in st_b.split('\n'):
        p = tf.add_paragraph()
        p.text = l
        p.font.name = "Aptos"
        p.font.size = Pt(11)
        p.font.color.rgb = C_BODY
    
    # Arrow connector
    if i < 3:
        arr = slide7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(0.68 + i * 3.05 + 2.70), Inches(2.50), Inches(0.30), Inches(0.20))
        arr.fill.solid()
        arr.fill.fore_color.rgb = C_STEEL
        arr.line.fill.background()

# Divider line
div_wf = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.68), Inches(3.65), Inches(12.00), Inches(0.015))
div_wf.fill.solid()
div_wf.fill.fore_color.rgb = C_BORDER
div_wf.line.fill.background()

# Section 2 Header
h2_box = slide7.shapes.add_textbox(Inches(0.68), Inches(3.85), Inches(8.0), Inches(0.30))
p_h2 = h2_box.text_frame.paragraphs[0]
p_h2.text = "CITIZEN GRIEVANCE REDRESSAL WORKFLOW"
p_h2.font.name = "Aptos"
p_h2.font.size = Pt(12)
p_h2.font.bold = True
p_h2.font.color.rgb = C_TEAL

# Pipeline 2 (4 Steps)
wf2_steps = [
    ("1  Pin location", "Citizen drops GPS pin\non phone browser"),
    ("2  Upload photo", "Photo evidence attached\nwith garbage category"),
    ("3  Ticket issued", "Tracking ticket\n#CMP-2026-104 generated"),
    ("4  Verified close", "Truck cleans location;\ntimeline marks resolved")
]
for i, (st_t, st_b) in enumerate(wf2_steps):
    bx = Inches(0.68 + i * 3.05)
    card, tf = add_card(slide7, bx, Inches(4.20), Inches(2.65), Inches(1.45), st_t, fill_color=C_ICE, border_color=C_TEAL)
    tf.paragraphs[0].font.size = Pt(13.5)
    for l in st_b.split('\n'):
        p = tf.add_paragraph()
        p.text = l
        p.font.name = "Aptos"
        p.font.size = Pt(11)
        p.font.color.rgb = C_BODY
    
    if i < 3:
        arr = slide7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(0.68 + i * 3.05 + 2.70), Inches(4.80), Inches(0.30), Inches(0.20))
        arr.fill.solid()
        arr.fill.fore_color.rgb = C_TEAL
        arr.line.fill.background()

add_callout(slide7, "Citizen overflow reports dynamically flag adjacent checkpoints on the active supervisor manifest.", prefix="Operational Sync: ")

# ==============================================================================
# SLIDE 8: PROOF-OF-SERVICE & GEOFENCING ENGINE (Core Technical Justification)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Proof-of-service & geofencing engine",
           "Mathematical proximity enforcement eliminates ghost trips and guarantees authentic physical waste collection.", 7)

# Left: Audit Screenshot
aud_img = 'report_assets/screenshot_audit.png'
if os.path.exists(aud_img):
    slide8.shapes.add_picture(aud_img, Inches(0.68), Inches(1.65), width=Inches(5.85))

# Right: Haversine & Integrity Card
c_geo, tf_geo = add_card(slide8, Inches(6.80), Inches(1.65), Inches(5.88), Inches(4.60), "Geospatial Proximity & Integrity Verification",
                         fill_color=C_WHITE, border_color=C_BORDER)

geo_sections = [
    ("Mathematical Proximity Enforcement:",
     "Great-circle distance d is computed in real time between the truck GPS and scheduled bin coordinates. Collection is strictly LOCKED if d > 15.0 meters."),
    ("Immutable Audit Trail Logging:",
     "Every collection and skip event records timestamp, vehicle registration, driver identity, and GPS tolerance accuracy (e.g., '5 meters - VALID')."),
    ("Elimination of Service Falsification:",
     "Completely prevents post-shift log fabrication or collection claims from home; drivers must be physically co-located at the bin with photo proof."),
    ("Structured Exception Audits:",
     "When access is blocked, drivers select verified skip categories (Road Excavation, Lane Blocked) which are flagged in red for supervisor audit.")
]
for lbl, desc in geo_sections:
    p = tf_geo.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

add_callout(slide8, "Driver collection action is cryptographically blocked unless Haversine distance d <= 15.0 meters from scheduled bin.", prefix="Verification Rule: ")

# ==============================================================================
# SLIDE 9: MODULE 1: SUPERVISOR GIS COMMAND CENTER
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Module 1: Supervisor GIS command center",
           "Real-time OpenStreetMap canvas displaying live vehicle telemetry, dynamic route completion, and operational alerts.", 8)

dash_img = 'report_assets/screenshot_dashboard.png'
if os.path.exists(dash_img):
    slide9.shapes.add_picture(dash_img, Inches(0.68), Inches(1.65), width=Inches(6.20))

c_sup, tf_sup = add_card(slide9, Inches(7.15), Inches(1.65), Inches(5.53), Inches(4.60), "Centralized Municipal Fleet Control",
                         fill_color=C_WHITE, border_color=C_BORDER)
sup_feats = [
    ("Interactive GIS Map Canvas:", "Renders OpenStreetMap canvas with color-coded stop checkpoints (Green: Collected, Amber: Next, Gray: Pending, Red: Skipped)."),
    ("Real-Time Vehicle Telemetry:", "Displays truck speed (e.g. 24 km/h), vehicle heading, driver identity, and GPS satellite lock status in real time."),
    ("Dynamic Route Progress Gauge:", "Computes route completion dynamically (e.g. 4 of 6 Stops Collected - 67%) with live cumulative waste payload tally."),
    ("Immediate Anomaly Alerts:", "Instantly flags delays, unauthorized route deviations, or bypassed stops for supervisor intervention.")
]
for lbl, desc in sup_feats:
    p = tf_sup.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(8)

add_callout(slide9, "Eliminates reliance on post-shift verbal claims by visualizing exact vehicle positions, speeds, and stop states.", prefix="Supervisor Benefit: ")

# ==============================================================================
# SLIDE 10: MODULE 2: DRIVER TOUCH-OPTIMIZED MANIFEST
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Module 2: Driver touch-optimized manifest",
           "Mobile-first web application designed for single-hand truck cab operation with continuous GPS accuracy monitoring.", 9)

drv_img = 'report_assets/screenshot_driver.png'
if os.path.exists(drv_img):
    slide10.shapes.add_picture(drv_img, Inches(0.68), Inches(1.65), width=Inches(6.20))

c_drv, tf_drv = add_card(slide10, Inches(7.15), Inches(1.65), Inches(5.53), Inches(4.60), "Field Driver Interface & Workflows",
                         fill_color=C_WHITE, border_color=C_BORDER)
drv_feats = [
    ("Cab-Friendly Touch UI:", "Designed with large tap targets for effortless one-hand operation on drivers' commodity smartphones mounted in the cab."),
    ("GNSS Satellite Status Banner:", "Continuously monitors active satellite connectivity and displays location precision (e.g. ±4m accuracy)."),
    ("15m Geofenced Proof Capture:", "The 'Mark Collected' button unlocks ONLY when the vehicle is physically within 15 meters of the scheduled bin."),
    ("Structured Exception Workflows:", "When encountering road blockages or construction, drivers log verified skip reasons (Narrow Lane, Excavation) without penalty.")
]
for lbl, desc in drv_feats:
    p = tf_drv.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(8)

add_callout(slide10, "Transparent exception logging protects drivers by recording legitimate road blockages without penalizing performance.", prefix="Driver Experience: ")

print("Slides 6 to 10 generated.")

# ==============================================================================
# SLIDE 11: MODULE 3: CITIZEN GRIEVANCE & TRACKING PORTAL
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Module 3: Citizen grievance & tracking portal",
           "Residents act as intelligent distributed sensors, crowdsourcing bin fill status and tracking complaint redressal.", 10)

cit_img = 'report_assets/screenshot_citizen.png'
if os.path.exists(cit_img):
    slide11.shapes.add_picture(cit_img, Inches(0.68), Inches(1.65), width=Inches(6.20))

c_cit, tf_cit = add_card(slide11, Inches(7.15), Inches(1.65), Inches(5.53), Inches(4.60), "Citizen Empowerment & Transparency",
                         fill_color=C_WHITE, border_color=C_BORDER)
cit_feats = [
    ("One-Tap GPS Pin Placement:", "Residents mark overflowing public bins or roadside waste dumps using their smartphone's accurate GPS."),
    ("Visual Photo Evidence Upload:", "Uploads photo proof of uncollected waste for supervisory verification and dispatch triage."),
    ("3-Stage Progress Timeline:", "Unique ticket ID (e.g. #CMP-2026-104) displays live status: Submitted → Dispatched → Resolved."),
    ("Public Ward Collection Timetable:", "Public schedule informs residents of daily collection timings to prevent premature waste dumping.")
]
for lbl, desc in cit_feats:
    p = tf_cit.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(8)

add_callout(slide11, "Direct tracking ticket ID (#CMP-2026-104) ensures accountability and transparent municipal service delivery.", prefix="Citizen Empowerment: ")

# ==============================================================================
# SLIDE 12: SOFTWARE ENGINEERING DESIGN & ACTOR MODELS
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "Software engineering design & actor models",
           "Object-oriented modeling and use case decomposition ensure strict separation of concerns and scalable code.", 11)

uc_img = 'report_assets/use_case_diagram.png'
if os.path.exists(uc_img):
    slide12.shapes.add_picture(uc_img, Inches(0.68), Inches(1.65), width=Inches(5.85))

c_uml, tf_uml = add_card(slide12, Inches(6.80), Inches(1.65), Inches(5.88), Inches(4.60), "Actor Responsibilities & OO Architecture",
                         fill_color=C_WHITE, border_color=C_BORDER)
uml_feats = [
    ("Field Driver Actor:", "Interacts via mobile manifest; capabilities include viewing route sequence, geofenced collection proof, and skip reporting."),
    ("Sanitation Supervisor Actor:", "Interacts via GIS command center; monitors real-time fleet, verifies proof photos, and conducts route replays."),
    ("Resident / Citizen Actor:", "Interacts via public web portal; files geotagged grievance tickets and tracks resolution progress."),
    ("Autonomous Platform Engine:", "Ingests GPS telemetry, computes Haversine distances, assigns complaint tickets, and seals audit trails.")
]
for lbl, desc in uml_feats:
    p = tf_uml.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(8)

add_callout(slide12, "Clean boundary separation ensures the geofencing engine remains independent of presentation and storage layers.", prefix="Engineering Practice: ")

# ==============================================================================
# SLIDE 13: SYSTEM VALIDATION & QUALITY ASSURANCE (Reference Table Pattern)
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "System validation & quality assurance",
           "End-to-end verification of authentication, GPS streaming, geofence radius enforcement, and citizen ticket lifecycles.", 12)

# Left: 5-Row Test Execution Table
t_s13 = slide13.shapes.add_table(rows=6, cols=5, left=Inches(0.68), top=Inches(1.65), width=Inches(7.60), height=Inches(4.60))
tb13 = t_s13.table
tb13.columns[0].width = Inches(0.90)
tb13.columns[1].width = Inches(2.10)
tb13.columns[2].width = Inches(2.20)
tb13.columns[3].width = Inches(1.60)
tb13.columns[4].width = Inches(0.80)

tc_headers = ["TC ID", "Test Case Objective", "Input Conditions", "Observed Output", "Status"]
for i, h in enumerate(tc_headers):
    cell = tb13.cell(0, i)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_ICE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Aptos"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TITLE

tc_data = [
    ("TC01", "Role-Based Access Control", "Valid Supervisor Credentials", "Access granted to GIS map", "PASS"),
    ("TC02", "Live GPS Telemetry Stream", "Lat: 17.8974, Lng: 83.4485", "Vehicle marker moves at 24 km/h", "PASS"),
    ("TC03", "Geofenced Proof Collection", "Vehicle within 5m (<=15m)", "Collection validated; proof logged", "PASS"),
    ("TC04", "Out-of-Bounds Rejection", "Vehicle at 450m (>15m)", "Action locked; warning shown", "PASS"),
    ("TC05", "Citizen Ticket Redressal", "Phone GPS Pin + Photo", "Ticket #CMP-2026-106 tracked live", "PASS")
]

for r_idx, r_data in enumerate(tc_data):
    for c_idx, val in enumerate(r_data):
        cell = tb13.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_ACCENT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Aptos"
        p.font.size = Pt(11)
        if c_idx == 4:
            p.font.bold = True
            p.font.color.rgb = C_GREEN
        else:
            p.font.color.rgb = C_BODY

# Right: QA Summary Card
c_qa, tf_qa = add_card(slide13, Inches(8.50), Inches(1.65), Inches(4.18), Inches(4.60), "Quality Assurance Benchmarks",
                       fill_color=C_WHITE, border_color=C_BORDER)
qa_pts = [
    ("100% Core Test Pass Rate:", "All functional test cases executed successfully across all three user modules with zero defects."),
    ("Sub-250ms API Latency:", "Stateless REST endpoints maintain rapid response times under simulated concurrent requests."),
    ("Sub-10m GPS Precision:", "Field testing confirmed high-accuracy geofencing matching using commodity smartphone A-GPS."),
    ("Edge Boundary Resilience:", "Confirmed strict rejection of unauthorized coordinates and network disconnect recovery.")
]
for lbl, desc in qa_pts:
    p = tf_qa.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

add_callout(slide13, "Zero boundary violations observed; out-of-bounds collection requests (>15m) are strictly blocked with 100% consistency.", prefix="Quality Benchmark: ")

# ==============================================================================
# SLIDE 14: OPERATIONAL BOUNDARIES & FUTURE ROADMAP
# ==============================================================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "Operational boundaries & future engineering roadmap",
           "Recognizing physical-world constraints and mapping the technical transition to automated artificial intelligence.", 13)

# Left: Current Boundaries
c_bnd, tf_bnd = add_card(slide14, Inches(0.68), Inches(1.65), Inches(5.88), Inches(4.60),
                         "Current Operational Boundaries",
                         fill_color=C_AMBER_BG, border_color=C_AMBER, title_color=C_AMBER)
bnd_pts = [
    ("Driver Phone Dependency:", "Fleet tracking is contingent on the driver keeping their phone charged and location permissions enabled."),
    ("Cellular Dead Zones:", "Signal drops in dense valleys temporarily pause telemetry streaming (buffered in local storage)."),
    ("Absence of In-Bin Scales:", "Because bins lack physical load cells, collected garbage weights rely on driver volumetric estimation."),
    ("Driver Compliance Reliance:", "Requires driver cooperation to tap 'Mark Collected' and capture photos at scheduled stops.")
]
for lbl, desc in bnd_pts:
    p = tf_bnd.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

# Right: Future AI Roadmap
c_fut, tf_fut = add_card(slide14, Inches(6.80), Inches(1.65), Inches(5.88), Inches(4.60),
                         "Future Engineering Roadmap",
                         fill_color=C_ICE, border_color=C_STEEL, title_color=C_STEEL)
fut_pts = [
    ("Computer Vision (YOLOv8) AI:", "Automatically analyzes driver collection photos to verify bin fullness percentage and detect unsegregated waste."),
    ("Dynamic Route Optimization (VRP):", "Integrates Vehicle Routing Problem algorithms to dynamically reorder stops based on live traffic."),
    ("Offline-First SQLite Caching:", "Client-side database caching ensures zero data loss during prolonged cellular blackouts."),
    ("Municipal WhatsApp Bot:", "Allows residents to submit garbage complaints directly via WhatsApp with automated location extraction.")
]
for lbl, desc in fut_pts:
    p = tf_fut.add_paragraph()
    p.text = f"• {lbl} {desc}"
    p.font.name = "Aptos"
    p.font.size = Pt(12)
    p.font.color.rgb = C_BODY
    p.space_after = Pt(6)

add_callout(slide14, "Integrating YOLOv8 computer vision will automatically estimate bin fill percentage from driver arrival photos.", prefix="Roadmap: ")

# ==============================================================================
# SLIDE 15: KEY TAKEAWAYS & PROJECT DELIVERABLES (Reference Slide 9 Pattern)
# ==============================================================================
slide15 = prs.slides.add_slide(blank_layout)
add_header(slide15, "Key takeaways & project deliverables",
           "A complete software platform demonstrating that smart city waste logistics can be solved through software alone.", 14)

# 3 Deliverable Cards
d_cards = [
    ("Full-Stack GIS Web Platform",
     "• Node.js & Express REST Backend\n"
     "• Leaflet.js & OpenStreetMap Canvas\n"
     "• Live Telemetry & Audit Trail Engine\n"
     "• Running on: http://localhost:3000",
     C_STEEL),
    ("Streamlit Community Cloud App",
     "• Interactive Streamlit + Folium App\n"
     "• Driver Manifest & Citizen Portal\n"
     "• Public Repo: saikiranbora25-byte\n"
     "• 1-Click Cloud Deployment",
     C_TEAL),
    ("Academic Project Report",
     "• 8,123-word Comprehensive Book\n"
     "• Strict ANITS Template Compliance\n"
     "• 11 Tables & 20 Embedded Figures\n"
     "• Formatted for Spiral Binding",
     C_NAVY)
]

for idx, (title, body, col) in enumerate(d_cards):
    cx = Inches(0.68 + idx * 4.05)
    card, tf = add_card(slide15, cx, Inches(1.65), Inches(3.85), Inches(2.65), title, fill_color=C_WHITE, border_color=C_BORDER, title_color=col)
    for l in body.split('\n'):
        p = tf.add_paragraph()
        p.text = l
        p.font.name = "Aptos"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_BODY
        p.space_after = Pt(2)

# Bottom Half: Large Executive Thank You Card
c_ty = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.68), Inches(4.50), Inches(12.00), Inches(1.85))
c_ty.fill.solid()
c_ty.fill.fore_color.rgb = C_NAVY
c_ty.line.color.rgb = C_STEEL
c_ty.line.width = Pt(1.5)

tf_ty = c_ty.text_frame
tf_ty.word_wrap = True
tf_ty.margin_top = Inches(0.18)

p_ty = tf_ty.paragraphs[0]
p_ty.text = "THANK YOU!"
p_ty.alignment = PP_ALIGN.CENTER
p_ty.font.name = "Aptos Display"
p_ty.font.size = Pt(24)
p_ty.font.bold = True
p_ty.font.color.rgb = RGBColor(56, 189, 248) # #38BDF8
p_ty.space_after = Pt(3)

p_qa = tf_ty.add_paragraph()
p_qa.text = "Questions & Technical Discussion Welcome"
p_qa.alignment = PP_ALIGN.CENTER
p_qa.font.name = "Aptos"
p_qa.font.size = Pt(13.5)
p_qa.font.bold = True
p_qa.font.color.rgb = C_WHITE
p_qa.space_after = Pt(3)

p_sig = tf_ty.add_paragraph()
p_sig.text = "SAIKIRAN BORA (Roll No: A24126510006)  •  B.Tech III Year CSE (Section - A)  •  ANITS (Autonomous), Visakhapatnam"
p_sig.alignment = PP_ALIGN.CENTER
p_sig.font.name = "Aptos"
p_sig.font.size = Pt(11)
p_sig.font.color.rgb = RGBColor(148, 163, 184)

p_gd = tf_ty.add_paragraph()
p_gd.text = "Faculty Guide: Prof. A. Rohini  •  Head of Department: Prof. G. Srinivas  •  Academic Year 2026–2027"
p_gd.alignment = PP_ALIGN.CENTER
p_gd.font.name = "Aptos"
p_gd.font.size = Pt(10.5)
p_gd.font.color.rgb = RGBColor(148, 163, 184)

add_callout(slide15, "CivicClean delivers complete municipal fleet tracking and verification with ZERO hardware expenditure.", prefix="Final Takeaway: ")

# Save Presentation
out_file = "CivicClean_Municipal_Waste_Fleet_Tracking_Presentation.pptx"
prs.save(out_file)
print(f"Presentation successfully generated and saved to: {out_file}")
print(f"Total Slides: {len(prs.slides)}")
