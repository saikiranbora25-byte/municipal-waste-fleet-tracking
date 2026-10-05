# -*- coding: utf-8 -*-
"""Slides 5 to 8: Proposed Solution, 3-Tier Architecture, Data Pipeline, Supervisor Dashboard"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_slides_5_to_8(prs, helpers):
    apply_background = helpers['apply_background']
    add_header = helpers['add_header']
    add_card = helpers['add_card']
    blank_layout = helpers['blank_layout']
    C_PRIMARY = helpers['C_PRIMARY']
    C_PRIMARY_DK = helpers['C_PRIMARY_DK']
    C_TEXT_SUB = helpers['C_TEXT_SUB']
    C_SUCCESS = helpers['C_SUCCESS']

    # ==========================================================
    # SLIDE 5: PROPOSED SOLUTION (Solution 2: Software-Only)
    # ==========================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_background(slide5)
    add_header(slide5, "Proposed Solution: Zero-Hardware Smart Waste Logistics", "04 | PROPOSED SOLUTION", 5)

    # Highlight Banner
    ban = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.65))
    ban.fill.solid()
    ban.fill.fore_color.rgb = RGBColor(239, 246, 255)
    ban.line.color.rgb = RGBColor(191, 219, 254)
    tf_b = ban.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = "STRATEGIC PARADIGM SHIFT: Eliminating 100% of Physical In-Bin Sensors by Utilizing Commodity Smartphones & Web APIs"
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(11.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_PRIMARY_DK

    # 4 Pillars (11.5pt - 12pt Font)
    pillars = [
        ("1. Smartphone Telemetry",
         "\u2022 Drivers use existing Android/iOS phones mounted inside the truck cab.\n"
         "\u2022 Continuous GPS streaming of real-time coordinates, speed, and heading.\n"
         "\u2022 Zero vehicle retrofitting or dedicated OBD hardware required.",
         C_PRIMARY),
        ("2. Geofenced Verification",
         "\u2022 Haversine proximity checks vehicle distance to target bin coordinates.\n"
         "\u2022 Camera photo capture unlocks ONLY when within 15 meters of the bin.\n"
         "\u2022 Creates immutable, tamper-resistant proof timestamps automatically.",
         C_SUCCESS),
        ("3. Citizen Crowdsourcing",
         "\u2022 Residents act as distributed sensors for citywide bin fill monitoring.\n"
         "\u2022 Geotagged photo reports with one-click GPS pin placement on phone.\n"
         "\u2022 Completely replaces costly physical ultrasonic level sensors.",
         RGBColor(139, 92, 246)),
        ("4. Transparent Exceptions",
         "\u2022 Drivers log structured skip reasons when facing road excavation or blocks.\n"
         "\u2022 Instantly flags checkpoints on supervisor GIS map for audit review.\n"
         "\u2022 Distinguishes between legitimate impediments and driver negligence.",
         RGBColor(245, 158, 11))
    ]

    for idx, (title, desc, col) in enumerate(pillars):
        cx = Inches(0.8 + idx * 2.98)
        card, tf = add_card(slide5, cx, Inches(2.45), Inches(2.82), Inches(4.35), title, title_color=col)
        for line in desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line.encode('utf-8').decode('unicode_escape')
            p.font.name = "Segoe UI"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT_SUB
            p.space_after = Pt(4)

    # ==========================================================
    # SLIDE 6: 3-TIER SYSTEM ARCHITECTURE (Streamlined SE, 12pt)
    # ==========================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_background(slide6)
    add_header(slide6, "System Architecture: End-to-End Enterprise Web Platform", "05 | ARCHITECTURE", 6)

    # Left: Architecture Diagram
    arch_img = 'report_assets/system_architecture.png'
    if os.path.exists(arch_img):
        slide6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.65), width=Inches(6.2))

    # Right: Practical 3-Tier Components
    tiers = [
        ("Tier 1: Presentation Layer (Client Portals)",
         "\u2022 Supervisor Command Hub: Desktop GIS dashboard with Leaflet map & telemetry.\n"
         "\u2022 Driver Mobile Manifest: Touch-friendly PWA for single-hand cab operation.\n"
         "\u2022 Public Citizen Portal: Responsive portal for reporting overflowing garbage.",
         C_PRIMARY),
        ("Tier 2: Application Layer (Node.js & Express)",
         "\u2022 REST API Gateway: High-performance endpoints for vehicle and stop data.\n"
         "\u2022 Geofencing Engine: Mathematical 15m radius proximity validation.\n"
         "\u2022 Grievance Engine: Auto-assigns complaint tickets and tracks clearance.",
         C_SUCCESS),
        ("Tier 3: Persistence Layer (Data & Audit)",
         "\u2022 Fleet State Store: Real-time coordinate cache for sub-second map updates.\n"
         "\u2022 Ward Route Store: Pre-mapped checkpoint waypoints and collection quotas.\n"
         "\u2022 Audit Trail: Immutable historical log of all verified collections and skips.",
         RGBColor(245, 158, 11))
    ]

    for idx, (title, desc, col) in enumerate(tiers):
        cy = Inches(1.65 + idx * 1.7)
        card, tf = add_card(slide6, Inches(7.2), cy, Inches(5.333), Inches(1.58), title, title_color=col)
        for line in desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line.encode('utf-8').decode('unicode_escape')
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_SUB
            p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 7: OPERATIONAL DATA PIPELINE (Reduced SE Textbook Jargon, 12pt)
    # ==========================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_background(slide7)
    add_header(slide7, "Operational Workflow & Telemetry Data Pipeline", "06 | DATA PIPELINE", 7)

    dfd_img = 'report_assets/dfd_level_1.png'
    if os.path.exists(dfd_img):
        slide7.shapes.add_picture(dfd_img, Inches(0.8), Inches(1.65), width=Inches(6.2))

    card_d, tf_d = add_card(slide7, Inches(7.2), Inches(1.65), Inches(5.333), Inches(5.0),
                            "End-to-End Information Pipeline", title_color=C_PRIMARY_DK)

    dfd_points = [
        ("Telemetry Streaming:", "Driver smartphone GPS broadcasts current coordinates and speed to the Node.js server every 5 seconds."),
        ("Spatial Geofence Matching:", "Backend continuously checks truck coordinates against scheduled ward stops using the Haversine equation."),
        ("Proof-of-Service Verification:", "When truck is within 15 meters, the driver captures photo proof. The system cryptographically stamps time and coordinates."),
        ("Citizen Redressal Synchronization:", "Residents log bin overflow tickets with GPS coordinates; resolved tickets update automatically upon vehicle clearance."),
        ("Supervisor Audit & KPI Aggregation:", "Computes real-time route completion percentages, missed pickups, and total daily waste tonnage collected.")
    ]
    for lbl, desc in dfd_points:
        p = tf_d.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 8: MODULE 1: SUPERVISOR GIS DASHBOARD (12pt Font)
    # ==========================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_background(slide8)
    add_header(slide8, "Module 1: Supervisor Real-Time GIS Fleet Command Center", "07 | SUPERVISOR DASHBOARD", 8)

    dash_img = 'report_assets/screenshot_dashboard.png'
    if os.path.exists(dash_img):
        slide8.shapes.add_picture(dash_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_dash, tf_dash = add_card(slide8, Inches(7.4), Inches(1.65), Inches(5.133), Inches(5.0),
                                  "Centralized Municipal Fleet Control", title_color=C_PRIMARY_DK)

    dash_features = [
        ("Live Interactive GIS Map:", "Renders OpenStreetMap canvas with color-coded stop checkpoints (Green: Collected, Amber: Next, Gray: Pending, Red: Skipped)."),
        ("Active Vehicle Telemetry:", "Displays truck speed (e.g. 24 km/h), vehicle heading, driver identity, and GPS satellite lock status in real time."),
        ("Ward Route Progress Gauge:", "Computes route completion dynamically (e.g. 4/6 Stops Collected - 67%) with live cumulative waste payload tally."),
        ("Immediate Anomaly Alerts:", "Instantly flags delays, unauthorized route deviations, or bypassed stops for supervisor intervention.")
    ]
    for lbl, desc in dash_features:
        p = tf_dash.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(8)

    print("Slides 5 to 8 generated successfully with 12pt fonts.")
