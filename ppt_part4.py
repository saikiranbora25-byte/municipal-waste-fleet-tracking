# -*- coding: utf-8 -*-
"""Slides 13 to 16: Testing, Justification Matrix, Limitations & Future Scope, Conclusion"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_slides_13_to_16(prs, helpers):
    apply_background = helpers['apply_background']
    add_header = helpers['add_header']
    add_card = helpers['add_card']
    blank_layout = helpers['blank_layout']
    C_PRIMARY = helpers['C_PRIMARY']
    C_PRIMARY_DK = helpers['C_PRIMARY_DK']
    C_TEXT_SUB = helpers['C_TEXT_SUB']
    C_SUCCESS = helpers['C_SUCCESS']
    C_DANGER = helpers['C_DANGER']
    C_DARK_BG = helpers['C_DARK_BG']
    C_WHITE = helpers['C_WHITE']

    # ==========================================================
    # SLIDE 13: TESTING & QUALITY ASSURANCE RESULTS
    # ==========================================================
    slide13 = prs.slides.add_slide(blank_layout)
    apply_background(slide13)
    add_header(slide13, "System Testing & Validation: Quality Assurance Suite", "12 | TESTING & VALIDATION", 13)

    # Left: Test Matrix Table
    t_shape = slide13.shapes.add_table(rows=9, cols=5, left=Inches(0.8), top=Inches(1.65), width=Inches(8.2), height=Inches(4.9))
    table = t_shape.table
    table.columns[0].width = Inches(0.9)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.4)
    table.columns[3].width = Inches(1.9)
    table.columns[4].width = Inches(0.8)

    headers = ["TC ID", "Test Case Objective", "Input Conditions", "Observed Output", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY_DK

    tc_data = [
        ("TC01", "Valid Role Authentication", "EmpID: EMP-088, Pass: Valid", "Redirects to Supervisor GIS Map", "PASS"),
        ("TC02", "Invalid Credentials Handling", "EmpID: EMP-088, Pass: Wrong", "Access Denied; clear error message", "PASS"),
        ("TC03", "Live GPS Telemetry Update", "Lat: 17.8974, Lng: 83.4485", "Truck marker moves; 24 km/h logged", "PASS"),
        ("TC04", "Geofenced Proof Collection", "Proximity: 5m <= 15m radius", "Stop marked 'Collected'; proof stored", "PASS"),
        ("TC05", "Out-of-Bounds Block Check", "Proximity: 450m > 15m radius", "Blocks collection; error alert shown", "PASS"),
        ("TC06", "Structured Skip Stop Log", "Reason: Road excavation logged", "Stop flagged 'Skipped'; red icon on map", "PASS"),
        ("TC07", "Citizen Grievance Submission", "Name, Phone, GPS Pin, Photo", "Ticket generated (CMP-2026-106)", "PASS"),
        ("TC08", "Live Ticket Status Tracking", "Ticket ID: CMP-2026-104", "3-stage timeline rendered correctly", "PASS")
    ]

    for row_idx, row_vals in enumerate(tc_data):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(8.5)
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_SUCCESS
            else:
                p.font.color.rgb = C_TEXT_SUB

    # Right: QA Summary Card
    card_qa, tf_qa = add_card(slide13, Inches(9.2), Inches(1.65), Inches(3.333), Inches(4.9),
                              "Quality Assurance Metrics", title_color=C_PRIMARY_DK)

    qa_metrics = [
        ("100% Test Pass Rate:", "All 8 core system test cases executed with zero defects across modules."),
        ("Sub-250ms API Latency:", "Stateless REST endpoints respond in under 250ms under concurrent requests."),
        ("Sub-10m GPS Precision:", "Field testing confirmed high-precision geofencing matching using smartphone A-GPS."),
        ("Boundary Edge Testing:", "Verified basis paths for boundary violations (>15m) and offline local storage buffering.")
    ]
    for lbl, desc in qa_metrics:
        p = tf_qa.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 14: COMPARATIVE JUSTIFICATION MATRIX
    # ==========================================================
    slide14 = prs.slides.add_slide(blank_layout)
    apply_background(slide14)
    add_header(slide14, "Comparative Analysis: Solution 2 Strategic Justification", "13 | JUSTIFICATION MATRIX", 14)

    # Comparison Table
    t_shape2 = slide14.shapes.add_table(rows=8, cols=4, left=Inches(0.8), top=Inches(1.65), width=Inches(11.733), height=Inches(4.3))
    t2 = t_shape2.table
    t2.columns[0].width = Inches(2.7)
    t2.columns[1].width = Inches(3.0)
    t2.columns[2].width = Inches(3.0)
    t2.columns[3].width = Inches(3.033)

    c_headers = ["Evaluation Criteria", "Legacy Manual System", "IoT Hardware Sensor (Sol 1)", "CivicClean GIS (Sol 2 - Proposed)"]
    for i, h in enumerate(c_headers):
        cell = t2.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_PRIMARY_DK if i == 3 else RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE if i == 3 else C_PRIMARY_DK

    comp_rows = [
        ("Hardware Procurement Cost", "Zero (Paper sheets)", "Extremely High (Rs. 5,000 / bin)", "ZERO (Uses existing smartphones)"),
        ("Vandalism & Theft Risk", "Not Applicable", "High Risk (Stolen / Damaged sensors)", "ZERO RISK (Hardware stays with driver)"),
        ("Maintenance & Battery Overhead", "Low (Manual)", "Very High (Recurring battery swaps)", "LOW (Over-the-air web app updates)"),
        ("Proof-of-Service Verification", "0% (Paper falsification common)", "Partial (Detects fill level only)", "100% (GPS + Geotagged Photo Proof)"),
        ("Obstruction / Skip Logging", "None (Bins bypassed silently)", "None (Sensors cannot detect obstacles)", "Automated (Categorized driver reasons)"),
        ("Citizen Engagement", "Nil (Delayed phone complaints)", "Nil (Closed hardware network)", "Direct Active Crowdsourcing Portal"),
        ("Municipal Scalability", "Inherently Inefficient", "Difficult (Requires physical installs)", "INSTANT (Deployable across any ward)")
    ]

    for r_idx, r_data in enumerate(comp_rows):
        for c_idx, val in enumerate(r_data):
            cell = t2.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if c_idx == 3:
                cell.fill.fore_color.rgb = RGBColor(239, 246, 255)
            else:
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(9)
            if c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = C_PRIMARY
            else:
                p.font.color.rgb = C_TEXT_SUB

    # Bottom summary callout
    b_box = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.65))
    b_box.fill.solid()
    b_box.fill.fore_color.rgb = RGBColor(236, 253, 245)
    b_box.line.color.rgb = RGBColor(167, 243, 208)
    tf_bb = b_box.text_frame
    tf_bb.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_bb = tf_bb.paragraphs[0]
    p_bb.text = "CONCLUSION: Solution 2 delivers 100% of smart city tracking benefits at <5% of the cost of physical sensor deployments!"
    p_bb.font.name = "Segoe UI"
    p_bb.font.size = Pt(10.5)
    p_bb.font.bold = True
    p_bb.font.color.rgb = RGBColor(6, 95, 70)

    # ==========================================================
    # SLIDE 15: LIMITATIONS & FUTURE ROADMAP
    # ==========================================================
    slide15 = prs.slides.add_slide(blank_layout)
    apply_background(slide15)
    add_header(slide15, "Limitations & Engineering Roadmap: Path to Future Scale", "14 | LIMITATIONS & ROADMAP", 15)

    # Left: Current Limitations
    c_lim, tf_lim = add_card(slide15, Inches(0.8), Inches(1.7), Inches(5.75), Inches(4.9),
                             "Current Operational Limitations",
                             border_color=RGBColor(245, 158, 11), title_color=RGBColor(180, 83, 9))
    lim_points = [
        ("Driver Smartphone Dependency:", "Fleet tracking is contingent on driver device battery life and keeping location permissions active during the shift."),
        ("Cellular Network Dead Zones:", "Temporary 4G signal loss in deep valleys or peripheral coastal alleys pauses real-time telemetry streaming (buffered locally)."),
        ("Absence of Direct Weight Scales:", "Because bins lack physical load cells, collected garbage weights rely on driver visual estimation or volumetric heuristics."),
        ("Compliance Reliance:", "Requires driver cooperation to tap 'Mark Collected' and upload photo proof at every scheduled checkpoint.")
    ]
    for lbl, desc in lim_points:
        p = tf_lim.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # Right: Future Scope
    c_fut, tf_fut = add_card(slide15, Inches(6.8), Inches(1.7), Inches(5.75), Inches(4.9),
                             "Future Engineering Enhancements",
                             border_color=C_PRIMARY, title_color=C_PRIMARY_DK)
    fut_points = [
        ("Offline-First PWA Synchronization:", "Implement SQLite / IndexedDB client caching so full shift telemetry and photos sync seamlessly when connectivity resumes."),
        ("Computer Vision (YOLOv8) AI:", "Automatically analyze driver collection photos using deep learning to verify bin fullness percentage and classify waste segregation."),
        ("Dynamic Route Optimization (VRP):", "Integrate Vehicle Routing Problem (VRP) algorithms to dynamically reorder stops based on live traffic and citizen hotspot reports."),
        ("Automated Municipal WhatsApp Bot:", "Allow residents to report garbage overflow via WhatsApp photo sharing with automated geolocation extraction.")
    ]
    for lbl, desc in fut_points:
        p = tf_fut.add_paragraph()
        p.text = f"\u2022 {lbl} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_SUB
        p.space_after = Pt(6)

    # ==========================================================
    # SLIDE 16: CONCLUSION & DELIVERABLES
    # ==========================================================
    slide16 = prs.slides.add_slide(blank_layout)
    apply_background(slide16, C_DARK_BG)

    # Top accent line
    top_bar16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar16.fill.solid()
    top_bar16.fill.fore_color.rgb = C_PRIMARY
    top_bar16.line.fill.background()

    # Header Box
    h_box16 = slide16.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.2))
    tf_h16 = h_box16.text_frame
    p_ht = tf_h16.paragraphs[0]
    p_ht.text = "Conclusion: Transforming Municipal Waste Logistics"
    p_ht.font.name = "Segoe UI"
    p_ht.font.size = Pt(24)
    p_ht.font.bold = True
    p_ht.font.color.rgb = C_WHITE

    p_hs = tf_h16.add_paragraph()
    p_hs.text = "A complete, verifiable, zero-hardware smart city software platform delivering real civic impact"
    p_hs.font.name = "Segoe UI"
    p_hs.font.size = Pt(12)
    p_hs.font.color.rgb = RGBColor(148, 163, 184)

    # 3 Deliverable Cards
    d_cards = [
        ("Full-Stack GIS Web Platform",
         "\u2022 Node.js & Express REST Backend\n"
         "\u2022 Leaflet.js & OpenStreetMap Canvas\n"
         "\u2022 Live Telemetry & Audit Trail\n"
         "\u2022 Running on: http://localhost:3000",
         RGBColor(30, 58, 138), RGBColor(59, 130, 246)),
        ("Streamlit Community Cloud App",
         "\u2022 Streamlit + Folium Interactive App\n"
         "\u2022 Mobile-friendly Driver Manifest\n"
         "\u2022 Public Citizen Grievance Portal\n"
         "\u2022 GitHub: saikiranbora25-byte",
         RGBColor(6, 95, 70), RGBColor(16, 185, 129)),
        ("Academic Mini Project Report",
         "\u2022 8,123-word Comprehensive Book\n"
         "\u2022 Strict ANITS Template Compliance\n"
         "\u2022 11 Tables & 20 Embedded Figures\n"
         "\u2022 Formatted for Spiral Binding",
         RGBColor(120, 53, 15), RGBColor(245, 158, 11))
    ]

    for idx, (title, text, bg, border) in enumerate(d_cards):
        cx = Inches(0.8 + idx * 3.95)
        c_del = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.85), Inches(3.8), Inches(2.9))
        c_del.fill.solid()
        c_del.fill.fore_color.rgb = RGBColor(15, 23, 42)
        c_del.line.color.rgb = border
        c_del.line.width = Pt(1.5)
        tf_cd = c_del.text_frame
        tf_cd.word_wrap = True
        tf_cd.margin_left = Inches(0.25)
        tf_cd.margin_top = Inches(0.25)
        
        p = tf_cd.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = border
        p.space_after = Pt(6)
        
        for line in text.split('\n'):
            p_l = tf_cd.add_paragraph()
            p_l.text = line
            p_l.font.name = "Segoe UI"
            p_l.font.size = Pt(10)
            p_l.font.color.rgb = RGBColor(226, 232, 240)
            p_l.space_after = Pt(2)

    # Big Centered Callout Card
    ty_card = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.85))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    ty_card.line.color.rgb = RGBColor(51, 65, 85)
    ty_card.line.width = Pt(1.5)
    tf_ty = ty_card.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_top = Inches(0.2)
    
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU!"
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.font.name = "Segoe UI"
    p_ty.font.size = Pt(22)
    p_ty.font.bold = True
    p_ty.font.color.rgb = RGBColor(56, 189, 248)
    p_ty.space_after = Pt(4)

    p_qa = tf_ty.add_paragraph()
    p_qa.text = "Questions & Technical Discussion Welcome"
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.font.name = "Segoe UI"
    p_qa.font.size = Pt(13)
    p_qa.font.bold = True
    p_qa.font.color.rgb = C_WHITE
    p_qa.space_after = Pt(4)

    p_sig = tf_ty.add_paragraph()
    p_sig.text = "SAIKIRAN BORA (Roll No: A24126510006) | Branch: CSE, Section - A | ANITS (Autonomous), Visakhapatnam"
    p_sig.alignment = PP_ALIGN.CENTER
    p_sig.font.name = "Segoe UI"
    p_sig.font.size = Pt(10)
    p_sig.font.color.rgb = RGBColor(148, 163, 184)

    print("Slides 13 to 16 generated successfully.")
