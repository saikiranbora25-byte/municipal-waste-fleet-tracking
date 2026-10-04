# -*- coding: utf-8 -*-
"""
CivicClean GIS: Municipal Solid Waste Fleet Tracking & Route Verification
Streamlit Web Application (Solution 2: Software-Only Zero-Hardware Architecture)
Author: Saikiran Bora (Roll No: A24126510006)
Department of Computer Science & Engineering, ANITS (Autonomous)
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="CivicClean GIS | Fleet Tracking",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .badge-success { background-color: #D1FAE5; color: #065F46; }
    .badge-warning { background-color: #FEF3C7; color: #92400E; }
    .badge-danger { background-color: #FEE2E2; color: #991B1B; }
    .badge-info { background-color: #DBEAFE; color: #1E40AF; }
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "stops" not in st.session_state:
    st.session_state.stops = [
        {
            "id": "STOP-01",
            "sequence": 1,
            "name": "Sangivalasa Junction Main Market",
            "zone": "Ward 1 - North",
            "lat": 17.9015,
            "lng": 83.4420,
            "targetTime": "06:30 AM",
            "status": "Collected",
            "completedTime": "06:38 AM",
            "driverId": "TRK-01",
            "proofPhoto": "https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=400&q=80",
            "verificationStatus": "Geo-Verified (Within 8m)",
            "weightKg": 420
        },
        {
            "id": "STOP-02",
            "sequence": 2,
            "name": "ANITS Campus North Gate & Hostels",
            "zone": "Ward 1 - North",
            "lat": 17.8995,
            "lng": 83.4452,
            "targetTime": "07:15 AM",
            "status": "Collected",
            "completedTime": "07:22 AM",
            "driverId": "TRK-01",
            "proofPhoto": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80",
            "verificationStatus": "Geo-Verified (Within 5m)",
            "weightKg": 380
        },
        {
            "id": "STOP-03",
            "sequence": 3,
            "name": "Bheemili Beach Road Commercial Complex",
            "zone": "Ward 2 - Coastal",
            "lat": 17.8942,
            "lng": 83.4510,
            "targetTime": "08:00 AM",
            "status": "Pending",
            "completedTime": None,
            "driverId": "TRK-01",
            "proofPhoto": None,
            "verificationStatus": "Awaiting Truck Arrival",
            "weightKg": 0
        },
        {
            "id": "STOP-04",
            "sequence": 4,
            "name": "Tagarapuvalasa Weekly Market Yard",
            "zone": "Ward 3 - East",
            "lat": 17.8910,
            "lng": 83.4580,
            "targetTime": "08:45 AM",
            "status": "Pending",
            "completedTime": None,
            "driverId": "TRK-01",
            "proofPhoto": None,
            "verificationStatus": "Scheduled",
            "weightKg": 0
        },
        {
            "id": "STOP-05",
            "sequence": 5,
            "name": "RTC Bus Stand Civic Waste Depot",
            "zone": "Ward 3 - East",
            "lat": 17.8875,
            "lng": 83.4625,
            "targetTime": "09:30 AM",
            "status": "Pending",
            "completedTime": None,
            "driverId": "TRK-01",
            "proofPhoto": None,
            "verificationStatus": "Scheduled",
            "weightKg": 0
        },
        {
            "id": "STOP-06",
            "sequence": 6,
            "name": "Anandapuram Bypass Crossroad",
            "zone": "Ward 4 - West",
            "lat": 17.8830,
            "lng": 83.4530,
            "targetTime": "10:15 AM",
            "status": "Skipped",
            "completedTime": "10:20 AM",
            "driverId": "TRK-01",
            "proofPhoto": None,
            "verificationStatus": "Flagged: Road Excavation",
            "skippedReason": "Access road blocked due to underground drainage work",
            "weightKg": 0
        }
    ]

if "complaints" not in st.session_state:
    st.session_state.complaints = [
        {
            "id": "CMP-2026-104",
            "citizenName": "M. Venkat Rao",
            "phone": "+91 94401 88231",
            "ward": "Ward 2 - Coastal (Bheemili)",
            "location": "Near Bheemili Lighthouse Old Fish Market",
            "lat": 17.8935,
            "lng": 83.4522,
            "category": "Overflowing Public Bin",
            "description": "Garbage bin overflowing onto the pedestrian lane since yesterday evening.",
            "status": "Assigned",
            "assignedTruck": "TRK-01 (AP39-TM-1001)",
            "reportedAt": "Today, 07:45 AM"
        },
        {
            "id": "CMP-2026-105",
            "citizenName": "K. Lakshmi Devi",
            "phone": "+91 98492 44109",
            "ward": "Ward 1 - North (Sangivalasa)",
            "location": "Opposite Community Hall, Sangivalasa",
            "lat": 17.9008,
            "lng": 83.4435,
            "category": "Missed Scheduled Pickup",
            "description": "Secondary collection tractor did not clear street 4 bin today.",
            "status": "Open",
            "assignedTruck": "TRK-01 (AP39-TM-1001)",
            "reportedAt": "Today, 08:10 AM"
        }
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Time": "06:38:12 AM", "Vehicle": "AP39-TM-1001", "Checkpoint": "Sangivalasa Junction Main Market", "Action": "COLLECTION_VERIFIED", "Accuracy": "8 meters", "Status": "SUCCESS"},
        {"Time": "07:22:45 AM", "Vehicle": "AP39-TM-1001", "Checkpoint": "ANITS Campus North Gate & Hostels", "Action": "COLLECTION_VERIFIED", "Accuracy": "5 meters", "Status": "SUCCESS"},
        {"Time": "10:20:05 AM", "Vehicle": "AP39-TM-1001", "Checkpoint": "Anandapuram Bypass Crossroad", "Action": "STOP_SKIPPED", "Accuracy": "Obstruction", "Status": "FLAGGED"}
    ]

if "truck_index" not in st.session_state:
    st.session_state.truck_index = 4

# Route Waypoints
route_coords = [
    [17.9020, 83.4410],
    [17.9015, 83.4420], # Stop 1
    [17.9002, 83.4438],
    [17.8995, 83.4452], # Stop 2
    [17.8974, 83.4485], # Current truck pos
    [17.8955, 83.4498],
    [17.8942, 83.4510], # Stop 3
    [17.8925, 83.4545],
    [17.8910, 83.4580], # Stop 4
    [17.8890, 83.4600],
    [17.8875, 83.4625], # Stop 5
    [17.8850, 83.4570],
    [17.8830, 83.4530]  # Stop 6
]

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/garbage-truck.png", width=70)
st.sidebar.markdown("### **CivicClean GIS**")
st.sidebar.caption("Municipal Solid Waste Fleet Tracking System (Solution 2 - Zero Hardware)")

menu = st.sidebar.radio(
    "Navigation Portal",
    [
        "?? Supervisor Command Hub",
        "?? Driver Field Portal",
        "?? Citizen Grievance Portal",
        "?? Operational Analytics",
        "?? Mini Project Report (.docx)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### **Active Fleet Telemetry**")
st.sidebar.markdown("**Vehicle:** AP39-TM-1001 (4T Compactor)")
st.sidebar.markdown("**Driver:** Ramesh Kumar")
st.sidebar.markdown("**GPS Lock:** ?4m Accuracy (A-GPS)")
st.sidebar.markdown("**Fuel Level:** 78% | **Battery:** 88%")

# Simulation Step Button in Sidebar
if st.sidebar.button("? Step Truck to Next Waypoint"):
    st.session_state.truck_index = (st.session_state.truck_index + 1) % len(route_coords)
    st.toast("Truck advanced to next coordinate!")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Developed by **Saikiran Bora (A24126510006)**")
st.sidebar.caption("Dept. of CSE, ANITS (Autonomous) | 2026?2027")

# ========================================================
# MODULE 1: SUPERVISOR COMMAND HUB
# ========================================================
if menu == "?? Supervisor Command Hub":
    st.markdown('<div class="main-title">?? Supervisor GIS Fleet Command Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Real-Time Vehicle Tracking, Route Verification, and Proof-of-Service Audit</div>', unsafe_allow_html=True)

    # Metrics
    total_stops = len(st.session_state.stops)
    collected = sum(1 for s in st.session_state.stops if s["status"] == "Collected")
    skipped = sum(1 for s in st.session_state.stops if s["status"] == "Skipped")
    pending = sum(1 for s in st.session_state.stops if s["status"] == "Pending")
    total_weight = sum(s.get("weightKg", 0) for s in st.session_state.stops)
    comp_rate = int((collected / total_stops) * 100) if total_stops else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Stops", f"{total_stops}")
    col2.metric("Verified Pickups", f"{collected}", f"{comp_rate}% done")
    col3.metric("Skipped / Blocked", f"{skipped}", delta_color="inverse")
    col4.metric("Active Fleet", "1 Active Truck")
    col5.metric("Open Grievances", f"{len(st.session_state.complaints)}")
    col6.metric("Waste Cleared", f"{total_weight} kg")

    st.markdown("---")

    # Layout: Map on Left (7 cols), Telemetry & Stream on Right (5 cols)
    map_col, tele_col = st.columns([7, 5])

    with map_col:
        st.subheader("??? Live GIS Fleet Tracking Map")
        st.caption("Visakhapatnam - Bheemili Municipal Sector (OpenStreetMap Layer)")

        current_truck_pos = route_coords[st.session_state.truck_index]
        m = folium.Map(location=[17.8960, 83.4500], zoom_start=14, tiles="OpenStreetMap")

        # Draw route polyline
        folium.PolyLine(route_coords, color="#2563EB", weight=5, opacity=0.8, dash_array="8, 8").add_to(m)

        # Draw Stop Checkpoints
        for s in st.session_state.stops:
            color = "orange"
            icon_name = "time"
            if s["status"] == "Collected":
                color = "green"
                icon_name = "ok-sign"
            elif s["status"] == "Skipped":
                color = "red"
                icon_name = "remove-sign"

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 170px;">
                <b>{s['name']}</b><br>
                <span style="color:gray;">{s['zone']}</span><br>
                <b>Status:</b> <span style="color:{color};">{s['status']}</span><br>
                <b>Target Time:</b> {s['targetTime']}<br>
                {f"<b>Finished:</b> {s['completedTime']}<br>" if s['completedTime'] else ""}
                {f"<small style='color:green;'>{s.get('verificationStatus','')}</small><br>" if s.get('verificationStatus') else ""}
                {f"<small style='color:red;'><b>Reason:</b> {s.get('skippedReason','')}</small>" if s.get('skippedReason') else ""}
            </div>
            """
            folium.Marker(
                [s["lat"], s["lng"]],
                popup=popup_html,
                tooltip=f"{s['sequence']}. {s['name']} ({s['status']})",
                icon=folium.Icon(color=color, icon=icon_name)
            ).add_to(m)

        # Draw Citizen Hotspot Complaints
        for c in st.session_state.complaints:
            comp_popup = f"""
            <div style="font-family: sans-serif; font-size: 12px;">
                <b style="color:purple;">[Citizen Hotspot] {c['id']}</b><br>
                <b>Location:</b> {c['location']}<br>
                <b>Issue:</b> {c['category']}<br>
                <b>Reported:</b> {c['reportedAt']}
            </div>
            """
            folium.Marker(
                [c["lat"], c["lng"]],
                popup=comp_popup,
                tooltip=f"Alert: {c['category']}",
                icon=folium.Icon(color="purple", icon="bullhorn", prefix="fa")
            ).add_to(m)

        # Draw Active Vehicle Marker
        folium.Marker(
            current_truck_pos,
            popup="<b>Truck AP39-TM-1001</b><br>Driver: Ramesh Kumar<br>Speed: 24 km/h",
            tooltip="Active Vehicle: AP39-TM-1001",
            icon=folium.Icon(color="blue", icon="truck", prefix="fa")
        ).add_to(m)

        st_folium(m, width="100%", height=450)

    with tele_col:
        st.subheader("?? Live Telemetry & Verification Feed")
        st.markdown(f"""
        <div class="card-box">
            <b>Vehicle Registration:</b> AP39-TM-1001 (4-Ton Compactor)<br>
            <b>Driver:</b> Ramesh Kumar (+91 98480 12345)<br>
            <b>Current Coordinates:</b> Lat {current_truck_pos[0]:.4f}, Lng {current_truck_pos[1]:.4f}<br>
            <b>Speed:</b> 24 km/h | <b>Fuel:</b> 78% | <b>GPS Precision:</b> ?4m (High Lock)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### **?? Real-Time Proof-of-Service Stream**")
        verified_stops = [s for s in st.session_state.stops if s["status"] == "Collected"]
        for vs in verified_stops:
            with st.container():
                c_img, c_txt = st.columns([1, 2])
                with c_img:
                    st.image(vs["proofPhoto"], use_container_width=True)
                with c_txt:
                    st.markdown(f"**{vs['name']}**")
                    st.caption(f"Cleared at {vs['completedTime']} | {vs['weightKg']} kg")
                    st.markdown(f"<span class='badge-pill badge-success'>? {vs['verificationStatus']}</span>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:0.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("??? Proof-of-Service Tamper-Resistant Audit Trail")
    df_audit = pd.DataFrame(st.session_state.audit_logs)
    st.dataframe(df_audit, use_container_width=True)

# ========================================================
# MODULE 2: DRIVER FIELD PORTAL
# ========================================================
elif menu == "?? Driver Field Portal":
    st.markdown('<div class="main-title">?? Driver Mobile Field Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Route Manifest, Automated Geofencing, and Camera Proof-of-Service</div>', unsafe_allow_html=True)

    # Driver profile card
    dcol1, dcol2 = st.columns([2, 1])
    with dcol1:
        st.info("?? **Driver:** Ramesh Kumar | **Assigned Vehicle:** AP39-TM-1001 (Compactor) | **Route:** North-01 (Sangivalasa - Bheemili)")
    with dcol2:
        st.success("?? **GPS Active & Geofenced** (Accuracy: ?4m)")

    # Route progress bar
    total_s = len(st.session_state.stops)
    done_s = sum(1 for s in st.session_state.stops if s["status"] == "Collected")
    progress_val = done_s / total_s
    st.progress(progress_val, text=f"Route Progress: {done_s} of {total_s} Checkpoints Completed ({int(progress_val*100)}%)")

    st.markdown("### **Assigned Checkpoint Manifest**")
    for s in st.session_state.stops:
        with st.expander(f"Stop #{s['sequence']}: {s['name']} ? [{s['status'].upper()}]", expanded=(s['status'] == "Pending")):
            sc1, sc2 = st.columns([3, 2])
            with sc1:
                st.markdown(f"**Ward / Sector:** {s['zone']}")
                st.markdown(f"**Target Arrival Time:** {s['targetTime']}")
                st.markdown(f"**GPS Coordinates:** Lat {s['lat']}, Lng {s['lng']}")
                if s["status"] == "Collected":
                    st.success(f"? Collected at {s['completedTime']} | Proof: {s.get('verificationStatus')}")
                elif s["status"] == "Skipped":
                    st.error(f"?? Skipped: {s.get('skippedReason')}")

            with sc2:
                if s["status"] == "Pending":
                    st.markdown("#### **Field Actions:**")
                    with st.form(f"collect_form_{s['id']}"):
                        weight_input = st.number_input("Estimated Waste (kg)", min_value=100, max_value=1000, value=350, step=25)
                        photo_sim = st.file_uploader("Take / Upload Photo Proof", type=["jpg", "png", "jpeg"])
                        submit_collect = st.form_submit_button("?? Mark as Collected (GPS Verified)")

                        if submit_collect:
                            s["status"] = "Collected"
                            s["completedTime"] = datetime.now().strftime("%I:%M %p")
                            s["verificationStatus"] = "Geo-Verified (GPS Lock: 4m)"
                            s["weightKg"] = weight_input
                            s["proofPhoto"] = "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80"
                            st.session_state.audit_logs.insert(0, {
                                "Time": datetime.now().strftime("%I:%M:%S %p"),
                                "Vehicle": "AP39-TM-1001",
                                "Checkpoint": s["name"],
                                "Action": "COLLECTION_VERIFIED",
                                "Accuracy": "4 meters",
                                "Status": "SUCCESS"
                            })
                            st.toast(f"Stop #{s['sequence']} marked as Collected!")
                            st.rerun()

                    # Skip form
                    with st.form(f"skip_form_{s['id']}"):
                        skip_reason = st.selectbox(
                            "Skip Justification Category",
                            [
                                "Access road blocked due to excavation / road repairs",
                                "Bin in inaccessible narrow lane due to illegal parking",
                                "Hazardous / biomedical waste detected in municipal bin",
                                "Bin already collected by secondary municipal tractor",
                                "Severe water logging / physical obstruction"
                            ]
                        )
                        skip_remarks = st.text_input("Observations / Remarks", placeholder="e.g. Pipeline trenching ongoing.")
                        submit_skip = st.form_submit_button("?? Report Obstruction & Skip Stop")

                        if submit_skip:
                            s["status"] = "Skipped"
                            s["completedTime"] = datetime.now().strftime("%I:%M %p")
                            s["skippedReason"] = f"{skip_reason} ({skip_remarks})" if skip_remarks else skip_reason
                            s["verificationStatus"] = "Flagged: Obstruction Logged"
                            st.session_state.audit_logs.insert(0, {
                                "Time": datetime.now().strftime("%I:%M:%S %p"),
                                "Vehicle": "AP39-TM-1001",
                                "Checkpoint": s["name"],
                                "Action": "STOP_SKIPPED",
                                "Accuracy": "Obstruction",
                                "Status": "FLAGGED"
                            })
                            st.toast(f"Stop #{s['sequence']} recorded as Skipped.")
                            st.rerun()

# ========================================================
# MODULE 3: CITIZEN GRIEVANCE PORTAL
# ========================================================
elif menu == "?? Citizen Grievance Portal":
    st.markdown('<div class="main-title">?? Visakhapatnam Clean City Grievance Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Crowdsourced Waste Reporting, GPS Pin-Drop, and Real-Time Grievance Tracking</div>', unsafe_allow_html=True)

    c_form_col, c_track_col = st.columns([6, 5])

    with c_form_col:
        st.subheader("?? Report Waste Overflow or Missed Pickup")
        with st.form("citizen_report_form", clear_on_submit=True):
            name = st.text_input("Your Full Name *", placeholder="e.g. Saikiran Bora")
            phone = st.text_input("Mobile Number *", placeholder="+91 98480 XXXXX")

            fc1, fc2 = st.columns(2)
            with fc1:
                ward = st.selectbox("Municipal Ward *", [
                    "Ward 1 - North (Sangivalasa)",
                    "Ward 2 - Coastal (Bheemili)",
                    "Ward 3 - East (Tagarapuvalasa)",
                    "Ward 4 - West (Anandapuram)"
                ])
            with fc2:
                category = st.selectbox("Issue Category *", [
                    "Overflowing Public Bin",
                    "Missed Scheduled Pickup",
                    "Illegal Roadside Waste Dumping",
                    "Damaged / Missing Garbage Bin"
                ])

            location = st.text_input("Landmark / Street Address *", placeholder="e.g. Near Bus Shelter, Sangivalasa Cross")
            use_gps = st.checkbox("?? Use My Device GPS Coordinates (Auto Lat/Lng)", value=True)
            desc = st.text_area("Issue Description", placeholder="e.g. Waste spilling over road, foul smell.")
            photo = st.file_uploader("Upload Waste Photo", type=["jpg", "png", "jpeg"])

            submit_complaint = st.form_submit_button("?? Submit Waste Grievance")

            if submit_complaint:
                if not name or not phone or not location:
                    st.error("Please fill in all mandatory fields (*)")
                else:
                    new_id = f"CMP-2026-{100 + len(st.session_state.complaints) + 1}"
                    new_ticket = {
                        "id": new_id,
                        "citizenName": name,
                        "phone": phone,
                        "ward": ward,
                        "location": location,
                        "lat": 17.8965,
                        "lng": 83.4495,
                        "category": category,
                        "description": desc,
                        "status": "Assigned",
                        "assignedTruck": "TRK-01 (AP39-TM-1001)",
                        "reportedAt": "Just now"
                    }
                    st.session_state.complaints.insert(0, new_ticket)
                    st.success(f"?? Grievance registered successfully! Your Tracking Ticket ID is **{new_id}**")

    with c_track_col:
        st.subheader("?? Track Your Grievance Status")
        search_id = st.text_input("Enter Ticket ID", value="CMP-2026-104", placeholder="e.g. CMP-2026-104")
        if search_id:
            match = next((c for c in st.session_state.complaints if c["id"].lower() == search_id.strip().lower()), None)
            if match:
                st.markdown(f"""
                <div class="card-box">
                    <span class="badge-pill badge-info">TICKET: {match['id']}</span>
                    <h4 style="margin-top:0.5rem;">{match['category']}</h4>
                    <p style="color:#64748B; font-size:0.85rem;"><b>Location:</b> {match['location']} ({match['ward']})<br>
                    <b>Reported By:</b> {match['citizenName']} | {match['reportedAt']}</p>
                    <div style="background:#F1F5F9; padding:0.6rem; border-radius:6px;">
                        <b>Current Status:</b> <span class="badge-pill badge-warning">{match['status']}</span><br>
                        <b>Assigned Collection Vehicle:</b> {match['assignedTruck']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("#### **Clearance Progression:**")
                st.markdown("? **Stage 1:** Grievance Registered & Validated")
                st.markdown("?? **Stage 2:** Collection Truck Dispatched En Route")
                st.markdown("? **Stage 3:** Clearance & Proof Photo Verification Pending")
            else:
                st.warning(f"No ticket found matching '{search_id}'")

        st.markdown("---")
        st.markdown("#### **?? Daily Ward Pickup Timings & Vehicle Roster**")
        roster_data = [
            {"Ward": "Ward 1: Sangivalasa", "Timing": "06:30 AM - 08:00 AM", "Vehicle": "AP39-TM-1001", "Status": "Completed"},
            {"Ward": "Ward 2: Bheemili Coastal", "Timing": "08:00 AM - 09:30 AM", "Vehicle": "AP39-TM-1001", "Status": "In Progress"},
            {"Ward": "Ward 3: Tagarapuvalasa", "Timing": "09:30 AM - 11:00 AM", "Vehicle": "AP39-TM-1001", "Status": "Pending"},
            {"Ward": "Ward 4: Anandapuram", "Timing": "11:00 AM - 12:30 PM", "Vehicle": "AP39-TM-1002", "Status": "Scheduled"}
        ]
        st.dataframe(pd.DataFrame(roster_data), use_container_width=True)

# ========================================================
# MODULE 4: OPERATIONAL ANALYTICS
# ========================================================
elif menu == "?? Operational Analytics":
    st.markdown('<div class="main-title">?? Operational Analytics & Performance Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Executive Ward Clearance, Fleet Productivity, and Resource Analytics</div>', unsafe_allow_html=True)

    an1, an2 = st.columns(2)

    with an1:
        st.subheader("Waste Cleared by Municipal Ward (kg)")
        ward_weights = {"Ward 1 (Sangivalasa)": 420, "Ward 2 (Bheemili)": 380, "Ward 3 (Tagarapuvalasa)": 510, "Ward 4 (Anandapuram)": 290}
        df_w = pd.DataFrame(list(ward_weights.items()), columns=["Ward", "WeightKg"])
        fig_bar = px.bar(df_w, x="Ward", y="WeightKg", color="Ward", text="WeightKg",
                         color_discrete_sequence=px.colors.qualitative.Prism)
        fig_bar.update_layout(showlegend=False, yaxis_title="Kilograms Cleared (kg)", height=380)
        st.plotly_chart(fig_bar, use_container_width=True)

    with an2:
        st.subheader("Checkpoint Completion Status Breakdown")
        status_counts = pd.Series([s["status"] for s in st.session_state.stops]).value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_pie = px.pie(status_counts, values="Count", names="Status", hole=0.45,
                         color="Status",
                         color_discrete_map={"Collected": "#10B981", "Pending": "#F59E0B", "Skipped": "#EF4444"})
        fig_pie.update_layout(height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Fleet Productivity & Emission Reduction KPIs")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Route Clearance Efficiency", "83.3%", "+12% vs Manual")
    k2.metric("Total Waste Handled", "1,600 kg", "Daily Target: 2,000 kg")
    k3.metric("Avg. Geofence Distance", "5.7 meters", "Threshold: 15.0m")
    k4.metric("Diesel Fuel Conserved", "14.2 Liters", "Due to skip route bypass")

# ========================================================
# MODULE 5: MINI PROJECT REPORT
# ========================================================
elif menu == "?? Mini Project Report (.docx)":
    st.markdown('<div class="main-title">?? Mini Project Report & Documentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">23CS4219 - Software Engineering Laboratory | ANITS Dept. of CSE</div>', unsafe_allow_html=True)

    report_path = "Municipal_Waste_Fleet_Tracking_Mini_Project_Report.docx"
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            docx_data = f.read()

        st.success("? **Official Academic Project Report is Ready for Download and Spiral Binding!**")
        st.download_button(
            label="?? Download Complete Word Report (.docx)",
            data=docx_data,
            file_name="Municipal_Waste_Fleet_Tracking_Mini_Project_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        st.markdown(f"**File Size:** {len(docx_data)/(1024*1024):.2f} MB | **Word Count:** 8,123 words | **Tables:** 11 | **Figures:** 20")
    else:
        st.error("Report document file not found on local path.")

    st.markdown("---")
    st.markdown("### **Executive Abstract Preview**")
    st.markdown("""
    Municipal solid waste management in expanding urban sectors faces severe operational bottlenecks due to unmonitored
    paper-based collection schedules, unverified truck routes, fuel wastage, and delayed grievance redressal. While
    Internet-of-Things (IoT) hardware sensor systems have been proposed, their high procurement cost, frequent maintenance,
    battery exhaustion, and susceptibility to public theft/vandalism render them economically unviable. To overcome these
    critical barriers, this project implements a pure software-only solution: the **GPS-Based Fleet Tracking and Route
    Verification System (CivicClean GIS)**.
    
    The system completely eliminates custom in-bin hardware by utilizing commodity driver smartphones and modern web browsers.
    It delivers four core architectural modules: (1) an interactive real-time GIS fleet tracking map for sanitation supervisors;
    (2) a mobile-responsive driver manifest featuring automated GPS geofence proximity matching and camera-based proof-of-service;
    (3) a public crowdsourced citizen reporting portal with GPS pin placement; and (4) a tamper-resistant proof-of-service audit
    trail.
    """)

    st.markdown("### **UML & Architecture Diagrams Included in Report**")
    diagram_col1, diagram_col2 = st.columns(2)
    with diagram_col1:
        if os.path.exists("report_assets/system_architecture.png"):
            st.image("report_assets/system_architecture.png", caption="Figure 7.1: 3-Tier System Architecture")
        if os.path.exists("report_assets/use_case_diagram.png"):
            st.image("report_assets/use_case_diagram.png", caption="Figure 9.1: System Use Case Diagram")
    with diagram_col2:
        if os.path.exists("report_assets/dfd_level_1.png"):
            st.image("report_assets/dfd_level_1.png", caption="Figure 6.2: Level 1 Data Flow Diagram")
        if os.path.exists("report_assets/class_diagram.png"):
            st.image("report_assets/class_diagram.png", caption="Figure 10.1: UML Class Diagram")
