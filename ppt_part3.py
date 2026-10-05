# -*- coding: utf-8 -*-
"""Slides 9 to 12: Driver App, Citizen Portal, Proof-of-Service Geofencing, UML Design"""
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
    # SLIDE 9: MODULE 2: DRIVER MOBILE FIELD APP
    # ==========================================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_background(slide9)
    add_header(slide9, "Module 2: Driver Touch-Optimized Mobile Field Manifest", "08 | DRIVER FIELD APP", 9)

    drv_img = 'report_assets/screenshot_driver.png'
    if os.path.exists(drv_img):
        slide9.shapes.add_picture(drv_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_drv, tf_drv = add_card(slide9, Inches(7.4), Inches(1.65), Inches(5.133), Inches(4.95),
                                "Field Driver Interface & Workflows", title_color=C_PRIMARY_DK)

    drv_features = [
        ("Mobile Frame Optimization:", "Specifically tailored for drivers operating compactor trucks with one-hand touch navigation on commodity Android phones."),
        ("GPS Geofencing Status Banner:", "Monitors active GNSS satellite connection, providing high-precision location lock (\u20224m accuracy)."),
        ("Dynamic Route Progress Tracking:", "Visual completion progress bar (e.g. 2 of 6 Stops Completed - 33%) updating instantly upon pickup verification."),
        ("One-Tap 'Mark Collected' Action:", "Unlocked only when vehicle is within 15 meters of bin. Prompts camera snapshot, captures coordinates, and records waste weight."),
        ("Structured 'Skip Stop' Exception Workflow:", "When access roads are blocked, the driver selects from standardized reasons (excavation, narrow lane, hazardous waste) with custom remarks.")
    ]
    for lbl, desc in drv_features:
        p = tf_drv.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    # ==========================================================
    # SLIDE 10: MODULE 3: CITIZEN GRIEVANCE PORTAL
    # ==========================================================
    slide10 = prs.slides.add_slide(blank_layout)
    apply_background(slide10)
    add_header(slide10, "Module 3: Citizen Crowdsourced Waste Grievance Portal", "09 | CITIZEN PORTAL", 10)

    cit_img = 'report_assets/screenshot_citizen.png'
    if os.path.exists(cit_img):
        slide10.shapes.add_picture(cit_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_cit, tf_cit = add_card(slide10, Inches(7.4), Inches(1.65), Inches(5.133), Inches(4.95),
                                "Citizen Empowerment & Tracking", title_color=C_PRIMARY_DK)

    cit_features = [
        ("Hotspot Reporting Form:", "Residents report overflowing public bins, missed scheduled pickups, or illegal roadside waste dumps directly from their phone browser."),
        ("One-Click GPS Pin Placement:", "Allows citizens to capture their phone's exact geolocation with a single tap, pinning the complaint on the municipal map."),
        ("Photo Evidence Upload:", "Attaches photographic proof of garbage accumulation for supervisory triage and dispatch prioritization."),
        ("Live Grievance Tracking Timeline:", "Unique tracking ticket ID (e.g. #CMP-2026-104) displays a 3-stage progress timeline: Submitted -> Truck Dispatched -> Clearance Verified."),
        ("Ward Collection Timings Roster:", "Public schedule displaying daily pickup time slots and assigned vehicles across municipal wards.")
    ]
    for lbl, desc in cit_features:
        p = tf_cit.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    # ==========================================================
    # SLIDE 11: PROOF-OF-SERVICE & AUDIT TRAIL
    # ==========================================================
    slide11 = prs.slides.add_slide(blank_layout)
    apply_background(slide11)
    add_header(slide11, "Proof-of-Service Engine: Geofencing & Tamper-Resistant Audit", "10 | PROOF-OF-SERVICE", 11)

    aud_img = 'report_assets/screenshot_audit.png'
    if os.path.exists(aud_img):
        slide11.shapes.add_picture(aud_img, Inches(0.8), Inches(1.65), width=Inches(6.4))

    card_aud, tf_aud = add_card(slide11, Inches(7.4), Inches(1.65), Inches(5.133), Inches(4.95),
                                "Geospatial Proximity & Integrity Verification", title_color=C_PRIMARY_DK)

    aud_features = [
        ("Haversine Spherical Distance Validation:",
         "Calculates great-circle distance between truck GPS (lat1, lon1) and bin coordinates (lat2, lon2):\n"
         "  d = 2R \u2022 arcsin(\u2022(sin\u2022(\u2022\u2022/2) + cos(\u20221)cos(\u20222)sin\u2022(\u2022\u2022/2)))\n"
         "If d <= 15.0 meters, collection action is unlocked; otherwise blocked."),
        ("Immutable Audit Trail Logging:", "Every collection and skip event records timestamp, vehicle registration, driver identity, and GPS tolerance accuracy (e.g., '5 meters - VALID')."),
        ("Elimination of Service Falsification:", "Drivers cannot fabricate collection logs after hours; completion requires physical proximity and real-time photo verification."),
        ("Automated Exception Flagging:", "Skipped stops are marked with categorized justifications and driver remarks for supervisor administrative audit.")
    ]
    for lbl, desc in aud_features:
        p = tf_aud.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    # ==========================================================
    # SLIDE 12: UML OBJECT-ORIENTED DESIGN HIGHLIGHTS
    # ==========================================================
    slide12 = prs.slides.add_slide(blank_layout)
    apply_background(slide12)
    add_header(slide12, "UML Design: Structural & Behavioral Software Models", "11 | UML DESIGN", 12)

    # Two diagrams side by side
    uc_img = 'report_assets/use_case_diagram.png'
    cls_img = 'report_assets/class_diagram.png'

    if os.path.exists(uc_img):
        slide12.shapes.add_picture(uc_img, Inches(0.8), Inches(1.65), width=Inches(5.7))

    card_uml, tf_uml = add_card(slide12, Inches(6.75), Inches(1.65), Inches(5.783), Inches(4.95),
                                "UML Architecture & OO Models Breakdown", title_color=C_PRIMARY_DK)

    uml_points = [
        ("Use Case Model (Figure 9.1):", "Defines 8 primary use cases spanning Driver (View Manifest, Mark Collected, Skip Stop), Citizen (Report Overflow, Track Status), and Supervisor (Live GIS Map, Verify Proof, Audit)."),
        ("Class Diagram Structure (Figure 10.1):", "Implements robust OOP principles with classes: Vehicle, StopCheckpoint, ProofOfService, CitizenComplaint, DriverUser, and SupervisorAdmin."),
        ("Sequence Diagram (Figure 10.2):", "Captures chronological message passing between Driver App, API Gateway, Haversine Validator, Database, and Supervisor Dashboard."),
        ("Activity & State Models (Figures 10.3 & 10.4):", "Traces driver operational branching (Accessible vs Blocked) and checkpoint lifecycle states (Scheduled -> In Progress -> Collected / Skipped)."),
        ("Component & Deployment Models (Figures 10.5 & 10.6):", "Maps logical software components across physical runtime nodes (Driver Phone, Cloud Node.js Server, Database).")
    ]
    for lbl, desc in uml_points:
        p = tf_uml.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(4)

    print("Slides 9 to 12 generated successfully.")
