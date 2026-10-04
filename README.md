# 🚛 CivicClean GIS: Municipal Solid Waste Fleet Tracking & Route Verification System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-v20%2B-green.svg)](https://nodejs.org)
[![Leaflet & OSM](https://img.shields.io/badge/GIS-OpenStreetMap-brightgreen.svg)](https://leafletjs.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A Pure Software-Only (Zero Hardware) Smart Waste Management Solution**  
> **Course**: 23CS4219 - Software Engineering Laboratory  
> **Author**: Saikiran Bora (Roll No: **A24126510006**)  
> **Institution**: Anil Neerukonda Institute of Technology and Sciences (UGC Autonomous), Visakhapatnam  
> **Academic Year**: 2026-2027 | **Guide**: Prof. A. Rohini | **HOD**: Prof. G. Srinivas  

---

## 📌 Executive Overview

Urban municipal waste collection in expanding sectors faces severe bottlenecks due to static paper-based route schedules, missed pickups, fuel waste, and lack of proof-of-service verification. 

While Internet-of-Things (IoT) sensor platforms have been proposed, installing hardware sensors inside public bins suffers from **prohibitive procurement costs, sensor vandalism, theft in public thoroughfares, and battery failure**. 

**CivicClean GIS (Solution 2)** decisively solves these challenges through a **100% software-only deployment**:
- **Zero Dedicated Hardware**: Uses commodity driver smartphones and standard web browsers.
- **Geofence-Enforced Proof-of-Service**: Checks real-time proximity (within 15m) before enabling photo proof capture.
- **Crowdsourced Citizen Monitoring**: Replaces physical bin sensors with direct resident photo reporting and GPS pin-drops.
- **Tamper-Resistant Audit Trail**: Maintains immutable timestamps, coordinates, and skip justifications.

---

## 🚀 Key Modules & Capabilities

### 1. 🏢 Supervisor GIS Command Hub
- **Interactive Map**: Built with Leaflet.js / Folium & OpenStreetMap, displaying live vehicle markers, route polylines, and status checkpoints.
- **Real-Time Telemetry**: Live vehicle speed, fuel level, battery health, and GPS accuracy (?4m).
- **Simulation Engine**: Step-by-step truck transit simulation along the Bheemili - Sangivalasa municipal route.
- **Proof-of-Service Verification Stream**: Real-time photo stream with geofence distance accuracy.
- **Tamper-Resistant Audit Trail**: Searchable table of verified pickups, skips, and supervisor logs.

### 2. 🚛 Driver Mobile Field Portal
- **Mobile Smartphone Framing**: Designed for one-hand operation on vehicle-mounted phones.
- **Assigned Route Checklist**: Chronological stops with target arrival times and status indicators.
- **One-Tap "Mark Collected"**: Captures photo proof, stamps GPS coordinates, and records waste weight.
- **Structured "Skip Stop"**: Categorizes road obstructions (excavations, illegal parking, hazardous waste) with driver remarks.

### 3. 👥 Citizen Grievance Portal
- **Hotspot Reporting Form**: Report overflowing bins with one-click GPS pin placement and photo upload.
- **Live Grievance Tracker**: 3-stage visual progress timeline using tracking ticket IDs (e.g., `#CMP-2026-104`).
- **Ward Collection Roster**: Searchable daily collection schedule and vehicle assignments.

### 4. 📊 Operational Analytics Hub
- Ward-wise waste clearance bar charts and route completion distribution.
- Fuel conservation metrics and fleet efficiency KPIs.

---

## 🛠️ Tech Stack & Architecture

- **Web Frontend**: HTML5, Modern CSS3, JavaScript (ES6+), Leaflet.js GIS, Font Awesome.
- **Streamlit Application**: Python 3.10+, Streamlit, Folium, Streamlit-Folium, Plotly, Pandas.
- **Backend API**: Node.js & Express REST Services.
- **Persistence**: Structured In-Memory Database with Local Storage and JSON Audit Logs.
- **Documentation**: Microsoft Word (.docx) 8,123-word academic project report complying with ANITS template.

---

## 💻 How to Run Locally

### Option A: Run the Streamlit Application
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Launch Streamlit
streamlit run streamlit_app.py
```
App will open automatically at `http://localhost:8501`.

### Option B: Run the Node.js Full-Stack Application
```bash
# Launch server
node server.js
```
Open `http://localhost:3000` in your web browser.

---

## ☁️ Deployment on Streamlit Community Cloud

1. Fork or push this repository to your GitHub account (`saikiranbora25-byte`).
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
3. Click **"New app"**, select this repository: `saikiranbora25-byte/municipal-waste-fleet-tracking`.
4. Set Main file path: `streamlit_app.py`.
5. Click **"Deploy!"** ? Your app will be live with a public URL accessible to anyone!

---

## 📄 Academic Project Report (.docx)

The complete 8,123-word academic project report is available in the repository:
- **File**: `Municipal_Waste_Fleet_Tracking_Mini_Project_Report.docx`
- **Formatting**: Strict 14pt/12pt Times New Roman, 1.25" gutter margin for spiral binding, 11 tables, and 20 embedded figures.
