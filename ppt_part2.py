# -*- coding: utf-8 -*-
"""Slides 5 to 8: Proposed Solution, 3-Tier Architecture, DFDs, Supervisor Dashboard"""
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
    add_header(slide5, "Proposed Solution: Zero-Hardware Smart Waste Architecture", "04 | PROPOSED SOLUTION", 5)

    # Top highlight banner
    ban = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.65))
    ban.fill.solid()
    ban.fill.fore_color.rgb = RGBColor(239, 246, 255)
    ban.line.color.rgb = RGBColor(191, 219, 254)
    tf_b = ban.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = "STRATEGIC PARADIGM SHIFT: Eliminating 100% of Physical In-Bin Sensors by Utilizing Commodity Smartphones & Web APIs"
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_PRIMARY_DK

    # 4 Pillars
    pillars = [
        ("1. Commodity Smartphone Telemetry",
         "\u2022 Field drivers use their existing Android/iOS phones mounted in the truck cab.\n"
         "\u2022 Built-in GPS chip continuously streams real-time coordinates, speed, and heading.\n"
         "\u2022 Zero vehicle retrofitting or dedicated OBD tracker hardware required.",
         C_PRIMARY),
        ("2. Geofence-Enforced Proof-of-Service",
         "\u2022 Spherical Haversine calculation verifies truck proximity to target bin coordinates.\n"
         "\u2022 Camera photo capture is unlocked ONLY when within 15 meters of the bin.\n"
         "\u2022 Creates immutable, tamper-resistant proof timestamps and coordinate hashes.",
         C_SUCCESS),
        ("3. Crowdsourced Citizen Reporting",
         "\u2022 Residents act as intelligent distributed sensors for citywide bin fill monitoring.\n"
         "\u2022 Upload geotagged photos of overflowing bins with one-click GPS pin-drops.\n"
         "\u2022 Eliminates the need for thousands of expensive ultrasonic level sensors.",
         RGBColor(139, 92, 246)),
        ("4. Transparent Exception Logging",
         "\u2022 When drivers encounter road excavations or blockages, they log structured skip reasons.\n"
         "\u2022 Instantly alerts supervisors and flags the checkpoint in red on the live map.\n"
         "\u2022 Distinguishes between legitimate operational impediments and driver negligence.",
         RGBColor(245, 158, 11))
    ]

    for idx, (title, desc, col) in enumerate(pillars):
        cx = Inches(0.8 + idx * 2.98)
        card, tf = add_card(slide5, cx, Inches(2.45), Inches(2.82), Inches(4.35), title, title_color=col)
        for line in desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_SUB
            p.space_after = Pt(3)

    # ==========================================================
    # SLIDE 6: 3-TIER SYSTEM ARCHITECTURE
    # ==========================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_background(slide6)
    add_header(slide6, "System Architecture: 3-Tier Enterprise Web Model", "05 | ARCHITECTURE", 6)

    # Left: Embedded Diagram
    arch_img = 'report_assets/system_architecture.png'
    if os.path.exists(arch_img):
        slide6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.65), width=Inches(6.2))

    # Right: Tier Breakdown Cards
    tiers = [
        ("Tier 1: Presentation Layer (Client Interfaces)",
         "\u2022 Supervisor Command Hub: Responsive Desktop browser (Leaflet.js GIS, Telemetry).\n"
         "\u2022 Driver Field Portal: Touch-optimized mobile PWA for one-hand in-cab operation.\n"
         "\u2022 Citizen Portal: Public responsive web interface for geotagged grievance reporting.",
         C_PRIMARY),
        ("Tier 2: Application / Logic Layer (Node.js & Express)",
         "\u2022 REST API Gateway: Handles stateless JSON endpoints (/api/vehicles, /api/stops).\n"
         "\u2022 Geofencing Engine: Haversine distance calculations and coordinate validation.\n"
         "\u2022 Telemetry & Simulation Router: Real-time coordinate interpolation and streaming.\n"
         "\u2022 Grievance Engine: Auto-dispatching tickets and managing resolution workflows.",
         C_SUCCESS),
        ("Tier 3: Data Persistence Layer (Storage)",
         "\u2022 In-Memory Cache: Sub-millisecond read/write access for live vehicle tracking.\n"
         "\u2022 Route & Geometry Store: Pre-registered ward stop coordinates and street waypoints.\n"
         "\u2022 Tamper-Resistant Audit Log: Immutable history of all verified pickups and skips.",
         RGBColor(245, 158, 11))
    ]

    for idx, (title, desc, col) in enumerate(tiers):
        cy = Inches(1.65 + idx * 1.7)
        card, tf = add_card(slide6, Inches(7.2), cy, Inches(5.333), Inches(1.58), title, title_color=col)
        for line in desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Segoe UI"
            p.font.size = Pt(9)
            p.font.color.rgb = C_TEXT_SUB
            p.space_after = Pt(2)

    # ==========================================================
    # SLIDE 7: DATA FLOW ARCHITECTURE (DFD Level 0 & 1)
    # ==========================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_background(slide7)
    add_header(slide7, "Data Flow Architecture: Process Decomposition & Data Stores", "06 | DATA FLOW DESIGN", 7)

    dfd_img = 'report_assets/dfd_level_1.png'
    if os.path.exists(dfd_img):
        slide7.shapes.add_picture(dfd_img, Inches(0.8), Inches(1.65), width=Inches(6.2))

    card_d, tf_d = add_card(slide7, Inches(7.2), Inches(1.65), Inches(5.333), Inches(4.95),
                            "Process Routing & Data Stores Analysis", title_color=C_PRIMARY_DK)

    dfd_points = [
        ("External Entities:", "Driver (Field Worker), Sanitation Supervisor (Admin), and Citizen (Resident)."),
        ("Process 1.0 (Fleet Telemetry Engine):", "Ingests periodic smartphone GPS latitude/longitude feeds and updates active vehicle coordinates in Data Store D1."),
        ("Process 2.0 (Checkpoint Geofencing):", "Matches real-time vehicle positions against target checkpoints in Master Route Store D2."),
        ("Process 3.0 (Proof-of-Service Verification):", "Validates 15m proximity, inspects camera photos, checks timestamp integrity, and commits records to Proof DB D3."),
        ("Process 4.0 (Citizen Grievance Redressal):", "Receives citizen complaints with photo evidence, generates ticket IDs, and stores records in Grievance DB D4."),
        ("Process 5.0 (Audit & Performance Reporting):", "Aggregates ward-wise waste weights, route completion rates, and fuel conservation KPIs.")
    ]
    for lbl, desc in dfd_points:
        p = tf_d.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    # ==========================================================
    # SLIDE 8: MODULE 1: SUPERVISOR GIS DASHBOARD
    # ==========================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_background(slide8)
    add_header(slide8, "Module 1: Supervisor Real-Time GIS Fleet Command Hub", "07 | SUPERVISOR DASHBOARD", 8)

    dash_img = 'report_assets/screenshot_dashboard.png'
    if os.path.exists(dash_img):
        slide8.shapes.add_picture(dash_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_s, tf_s = add_card(slide8, Inches(7.4), Inches(1.65), Inches(5.133), Inches(4.95),
                            "Supervisor Operational Capabilities", title_color=C_PRIMARY_DK)

    dash_features = [
        ("Interactive GIS Canvas (Leaflet & OSM):", "Renders Visakhapatnam / Bheemili sector with route polylines, vehicle positions, and checkpoint status markers."),
        ("Color-Coded Status Markers:", "Green for Verified Collected, Amber for Pending, Red for Skipped / Obstruction, Blue for Active Truck, Purple for Citizen Hotspots."),
        ("Real-Time Vehicle Telemetry:", "Monitors truck AP39-TM-1001 live speed (24 km/h), fuel level (78%), battery health, and GPS accuracy (\u20224m)."),
        ("Vehicle Simulation Controller:", "Includes Play, Pause, and Step Next controls allowing supervisors to simulate coordinate movements during driver training."),
        ("Live Proof-of-Service Stream:", "Displays live thumbnails of driver-uploaded collection photos alongside timestamp and geofence tolerance accuracy.")
    ]
    for lbl, desc in dash_features:
        p = tf_s.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    print("Slides 5 to 8 generated successfully.")
