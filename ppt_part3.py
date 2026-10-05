# -*- coding: utf-8 -*-
"""Slides 9 to 12: Driver App, Citizen Portal, Proof-of-Service Geofencing, System Design"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_slides_9_to_12(prs, helpers):
    apply_background = helpers['apply_background']
    add_header = helpers['add_header']
    add_card = helpers['add_card']
    blank_layout = helpers['blank_layout']
    C_PRIMARY = helpers['C_PRIMARY']
    C_PRIMARY_DK = helpers['C_PRIMARY_DK']
    C_TEXT_SUB = helpers['C_TEXT_SUB']
    C_SUCCESS = helpers['C_SUCCESS']

    # ==========================================================
    # SLIDE 9: MODULE 2: DRIVER MOBILE FIELD APP (12pt Font)
    # ==========================================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_background(slide9)
    add_header(slide9, "Module 2: Driver Touch-Optimized Mobile Manifest", "08 | DRIVER FIELD APP", 9)

    drv_img = 'report_assets/screenshot_driver.png'
    if os.path.exists(drv_img):
        slide9.shapes.add_picture(drv_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_drv, tf_drv = add_card(slide9, Inches(7.4), Inches(1.65), Inches(5.133), Inches(5.0),
                                "Field Driver Interface & Workflows", title_color=C_PRIMARY_DK)

    drv_features = [
        ("Cab-Friendly Touch UI:", "Designed with large tap targets for effortless one-hand operation on drivers' commodity smartphones."),
        ("GPS Satellite Status Banner:", "Continuously monitors active GNSS satellite connection and displays location precision (e.g. \u00B14m accuracy)."),
        ("Dynamic Route Progress:", "Live completion progress bar updates instantly upon every verified pickup (e.g., 2 of 6 Stops Completed - 33%)."),
        ("15m Geofenced Proof Capture:", "The 'Mark Collected' button unlocks ONLY when the vehicle is physically within 15 meters of the scheduled bin."),
        ("Structured Exception Logging:", "When encountering road blockages or construction, drivers log verified skip reasons (e.g., Narrow Lane, Excavation).")
    ]
    for lbl, desc in drv_features:
        p = tf_drv.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 10: MODULE 3: CITIZEN GRIEVANCE PORTAL (12pt Font)
    # ==========================================================
    slide10 = prs.slides.add_slide(blank_layout)
    apply_background(slide10)
    add_header(slide10, "Module 3: Citizen Crowdsourced Waste Grievance Portal", "09 | CITIZEN PORTAL", 10)

    cit_img = 'report_assets/screenshot_citizen.png'
    if os.path.exists(cit_img):
        slide10.shapes.add_picture(cit_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_cit, tf_cit = add_card(slide10, Inches(7.4), Inches(1.65), Inches(5.133), Inches(5.0),
                                "Citizen Empowerment & Tracking", title_color=C_PRIMARY_DK)

    cit_features = [
        ("One-Tap GPS Pin Drop:", "Residents mark overflowing public bins or illegal garbage heaps using their phone's exact GPS coordinates."),
        ("Photo Evidence Upload:", "Allows citizens to attach photos of uncollected waste for supervisory verification and dispatch triage."),
        ("Live 3-Stage Ticket Tracker:", "Unique complaint ID (e.g. #CMP-2026-104) shows real-time progress: Submitted -> Truck Dispatched -> Clearance Verified."),
        ("Public Collection Roster:", "Displays daily pickup schedules and assigned compactor trucks across wards to prevent premature bin dumping.")
    ]
    for lbl, desc in cit_features:
        p = tf_cit.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(8)

    # ==========================================================
    # SLIDE 11: PROOF-OF-SERVICE & AUDIT TRAIL (12pt Font)
    # ==========================================================
    slide11 = prs.slides.add_slide(blank_layout)
    apply_background(slide11)
    add_header(slide11, "Proof-of-Service Engine: Geofencing & Tamper-Resistant Audit", "10 | PROOF-OF-SERVICE", 11)

    aud_img = 'report_assets/screenshot_audit.png'
    if os.path.exists(aud_img):
        slide11.shapes.add_picture(aud_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_aud, tf_aud = add_card(slide11, Inches(7.4), Inches(1.65), Inches(5.133), Inches(5.0),
                                "Geospatial Proximity & Integrity Verification", title_color=C_PRIMARY_DK)

    aud_features = [
        ("Haversine Distance Validation:",
         "Calculates great-circle distance between truck GPS and bin location. Collection is permitted ONLY when d <= 15.0 meters."),
        ("Immutable Audit Trail Logging:",
         "Every collection and skip event records timestamp, vehicle registration, driver identity, and GPS tolerance accuracy (e.g., '5 meters - VALID')."),
        ("Elimination of Ghost Collections:",
         "Completely prevents post-shift log falsification; drivers must be physically present with geotagged photo proof."),
        ("Structured Exception Review:",
         "Bypassed bins are categorized with driver remarks and flagged in red on the supervisor map for administrative review.")
    ]
    for lbl, desc in aud_features:
        p = tf_aud.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 12: SYSTEM DESIGN & ACTOR INTERACTIONS (Reduced SE Theory, 12pt)
    # ==========================================================
    slide12 = prs.slides.add_slide(blank_layout)
    apply_background(slide12)
    add_header(slide12, "System Design: Role-Based Actor Interaction Model", "11 | SYSTEM DESIGN", 12)

    uc_img = 'report_assets/use_case_diagram.png'
    if os.path.exists(uc_img):
        slide12.shapes.add_picture(uc_img, Inches(0.8), Inches(1.65), width=Inches(6.0))

    card_uml, tf_uml = add_card(slide12, Inches(7.0), Inches(1.65), Inches(5.533), Inches(5.0),
                                "Stakeholder Roles & Core Capabilities", title_color=C_PRIMARY_DK)

    actor_points = [
        ("Field Driver Role:", "Receives digital route manifest, validates pickup via 15m geofencing, captures camera photos, and logs road obstruction skips."),
        ("Sanitation Supervisor Role:", "Monitors real-time vehicle fleet on GIS map, conducts route replays, reviews skipped stops, and validates daily completion KPIs."),
        ("Citizen Stakeholder Role:", "Submits geotagged garbage complaints with photos, tracks ticket resolution progress, and views ward collection schedules."),
        ("Automated Platform Engine:", "Enforces spatial geofence boundaries, processes live GPS telemetry, dispatches tickets, and generates tamper-resistant audit logs.")
    ]
    for lbl, desc in actor_points:
        p = tf_uml.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}".encode('utf-8').decode('unicode_escape')
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(8)

    print("Slides 9 to 12 generated successfully with 12pt fonts.")
