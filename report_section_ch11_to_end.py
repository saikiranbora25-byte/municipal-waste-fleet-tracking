# -*- coding: utf-8 -*-
"""Chapters 11 to 15 + Appendix: Testing, Screenshots, Limitations, Conclusion, References, Appendix"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapters_11_to_end(doc, helpers):
    add_heading_1 = helpers['add_heading_1']
    add_heading_2 = helpers['add_heading_2']
    add_heading_3 = helpers['add_heading_3']
    add_paragraph = helpers['add_paragraph']
    add_bullet = helpers['add_bullet']
    add_figure = helpers['add_figure']
    add_table_custom = helpers['add_table_custom']

    # ==========================================
    # CHAPTER 11: TESTING
    # ==========================================
    add_heading_1("11. Testing")
    
    add_heading_2("11.1 Test Plan & Methodology")
    add_paragraph(
        "A rigorous, multi-tiered testing strategy was executed throughout the development lifecycle to verify functional correctness, "
        "geospatial precision, data integrity, and system resilience under variable network conditions. The testing methodology adhered "
        "to standard Software Engineering quality assurance protocols, incorporating the following verification techniques:"
    )
    add_bullet("Unit Testing", "Individual algorithmic modules?such as the Haversine spherical distance calculation function, ISO timestamp parser, and ticket ID generator?were tested in isolation with boundary value test fixtures.")
    add_bullet("White-Box & Basis Path Testing", "Control logic within the geofencing verification routine and skip-reason validation flows was analyzed to derive Cyclomatic Complexity (V(G)), ensuring every independent execution path was exercised at least once.")
    add_bullet("Black-Box Testing", "Equivalence partitioning and boundary value analysis were applied to all client-facing forms and REST endpoints, verifying input sanitization for phone numbers, GPS coordinates, and file attachments.")
    add_bullet("System Integration Testing", "End-to-end integration between the driver mobile client, the Node.js API server, and the supervisor GIS map was validated under concurrent network simulations to ensure immediate synchronization.")
    add_bullet("Validation & Acceptance Testing", "The application was subjected to simulated real-world scenarios covering the Visakhapatnam municipal ward test sector, validating user journey satisfaction against the functional requirements.")

    add_heading_2("11.2 System Test Cases Execution Matrix")
    add_paragraph(
        "A comprehensive suite of test cases (TC01 through TC08) was formally executed across all modules. Table 11.1 documents "
        "the test case identifier, test objective, test inputs, expected output, observed actual result, and final pass/fail status."
    )

    tc_headers = ["TC ID", "Test Case Description", "Test Input Data", "Expected Output", "Actual Output", "Status"]
    tc_rows = [
        ["TC01", "Valid Role Authentication", "Role: Supervisor, EmpID: EMP-088, Pass: Valid", "Authentication success; redirect to supervisor GIS dashboard", "Login successful; dashboard rendered with live feed", "Pass"],
        ["TC02", "Invalid Role Credentials", "Role: Supervisor, EmpID: EMP-088, Pass: Wrong", "Authentication rejected; display clear error message", "Error message displayed; access denied", "Pass"],
        ["TC03", "Live GPS Telemetry Update", "Lat: 17.8974, Lng: 83.4485, Speed: 24 km/h", "Vehicle marker moves on GIS map; speed updates to 24 km/h", "Marker moved smoothly; telemetry panel reflected 24 km/h", "Pass"],
        ["TC04", "Geofenced Proof Collection", "Stop: STOP-02, Geofence Distance: 5m, Photo: Valid", "Status updates to 'Collected'; proof logged with 5m accuracy", "Stop marked 'Collected'; photo & 5m accuracy logged in audit", "Pass"],
        ["TC05", "Out-of-Bounds Collection Attempt", "Stop: STOP-04, Geofence Distance: 450m (>15m threshold)", "System blocks collection; shows proximity violation error", "Collection blocked; 'Must be within 15m' alert shown", "Pass"],
        ["TC06", "Structured Skip Stop Logging", "Stop: STOP-06, Reason: Road excavation, Remarks logged", "Status updates to 'Skipped'; stop flagged in red on map", "Stop status changed to 'Skipped'; red icon & reason displayed", "Pass"],
        ["TC07", "Citizen Hotspot Submission", "Name: Saikiran, Phone: 9848012345, Ward: 1, Photo", "Ticket generated (e.g. CMP-2026-106); pin added to map", "Ticket CMP-2026-106 created; purple hotspot marker rendered", "Pass"],
        ["TC08", "Live Ticket Status Tracking", "Ticket ID: CMP-2026-104", "Display 3-stage timeline with active truck dispatch state", "Timeline displayed; shows 'Assigned to Truck TRK-01'", "Pass"]
    ]
    add_table_custom("Table 11.1: System Test Cases Matrix & Validation Results", tc_headers, tc_rows, [0.8, 1.6, 1.4, 1.5, 1.5, 0.7])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 12: RESULTS / SCREENSHOTS
    # ==========================================
    add_heading_1("12. Results / Screenshots")
    add_paragraph(
        "This chapter presents high-resolution visual evidence of the implemented CivicClean web application across all core operational "
        "interfaces. In compliance with project guidelines, each screenshot is accompanied by its formal figure designation and a detailed "
        "technical explanation."
    )

    add_heading_2("12.1 Home Page & Portal Switcher")
    add_figure(
        'report_assets/screenshot_home.png',
        "Figure 12.1: Application Home Page & Portal Switcher View",
        "Short Explanation: Figure 12.1 depicts the central landing portal of CivicClean GIS. The interface features the official municipal "
        "header, live operational feed indicator, digital clock, and navigation cards providing one-click access to the Supervisor Command "
        "Hub, the Driver Field App, and the Citizen Grievance Portal."
    )

    add_heading_2("12.2 Role-Based User Authentication")
    add_figure(
        'report_assets/screenshot_login.png',
        "Figure 12.2: Role-Based User Authentication Interface",
        "Short Explanation: Figure 12.2 shows the secure login interface enforcing Role-Based Access Control (RBAC). Users select their "
        "designated organizational role (Supervisor, Field Driver, or Resident) and provide validated credentials to enter protected "
        "administrative views."
    )

    add_heading_2("12.3 Supervisor Live GIS Fleet Map")
    add_figure(
        'report_assets/screenshot_dashboard.png',
        "Figure 12.3: Supervisor Live GIS Fleet Tracking Dashboard",
        "Short Explanation: Figure 12.3 illustrates the primary administrative dashboard. The upper KPI ribbon summarizes total stops (6), "
        "verified collections (2), skipped stops (1), active fleet (1), open citizen complaints (2), and cleared waste (800 kg). The Leaflet "
        "map renders color-coded route lines, vehicle positions, checkpoint markers, and the live vehicle telemetry and proof stream."
    )

    add_heading_2("12.4 Driver Mobile Field Manifest & Proof Upload")
    add_figure(
        'report_assets/screenshot_driver.png',
        "Figure 12.4: Driver Mobile Field Manifest & Proof Upload Interface",
        "Short Explanation: Figure 12.4 displays the smartphone-optimized driver interface within a mobile frame. The view highlights "
        "the active driver profile (Ramesh Kumar), green GPS lock banner (?4m accuracy), route completion progress bar (33%), and "
        "interactive checkpoint cards featuring one-tap 'Mark Collected' and 'Skip' action buttons."
    )

    add_heading_2("12.5 Citizen Grievance Submission Portal & Live Tracker")
    add_figure(
        'report_assets/screenshot_citizen.png',
        "Figure 12.5: Citizen Grievance Submission Portal & Live Ticket Tracker",
        "Short Explanation: Figure 12.5 shows the public reporting interface. On the left, residents enter complaint details with one-click "
        "GPS coordinate capture and photo attachments. On the right, the live grievance tracker renders the 3-stage resolution timeline for "
        "ticket CMP-2026-104 alongside the daily ward collection roster."
    )

    add_heading_2("12.6 Proof-of-Service Tamper-Resistant Audit Trail")
    add_figure(
        'report_assets/screenshot_audit.png',
        "Figure 12.6: Proof-of-Service Tamper-Resistant Audit Trail",
        "Short Explanation: Figure 12.6 exhibits the immutable audit log table. Each row records the exact timestamp, vehicle registration "
        "number (AP39-TM-1001), stop location, action type (COLLECTION_VERIFIED or STOP_SKIPPED), geofence accuracy tolerance, and "
        "verification status."
    )

    add_heading_2("12.7 Fleet Waste Clearance Analytics Report")
    add_figure(
        'report_assets/screenshot_analytics.png',
        "Figure 12.7: Fleet Waste Clearance Analytics & Performance Report",
        "Short Explanation: Figure 12.7 displays the executive performance report, visualizing waste cleared by municipal ward (Sangivalasa, "
        "Bheemili, Tagarapuvalasa, Anandapuram) and presenting aggregate fleet efficiency KPIs."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 13: LIMITATIONS
    # ==========================================
    add_heading_1("13. Limitations")
    add_paragraph(
        "In accordance with software engineering evaluation standards, two specific operational limitations inherent to the pure "
        "software-only deployment model are recognized and analyzed:"
    )
    add_bullet(
        "Limitation 1: Operational Dependency on Driver Smartphone Integrity and Cellular Coverage",
        "Because the system relies entirely on commodity smartphones rather than dedicated on-board vehicle telematics units, fleet "
        "tracking is strictly contingent upon the continuous operational health of the driver's phone. If the smartphone runs out of "
        "battery, suffers hardware damage during rough handling, experiences temporary cellular data dead zones in peripheral coastal "
        "valleys, or if the driver accidentally disables location permissions, the live GPS stream is temporarily interrupted. While "
        "the mobile client buffers proof records locally for subsequent synchronization upon network reconnection, real-time supervisory "
        "visibility is momentarily degraded during connectivity blackouts."
    )
    add_bullet(
        "Limitation 2: Absence of Automated Physical Bin-Weight & Volumetric Sensing",
        "By deliberately eliminating physical ultrasonic level and load-cell weight sensors from public bins to avoid hardware capital "
        "and vandalism costs, the software cannot autonomously determine the exact fill level of a bin prior to the truck's arrival. "
        "Consequently, waste weight entries recorded during collection rely on driver visual estimation or volumetric heuristics rather "
        "than calibrated digital scale measurements. Dynamic demand-based routing relies primarily on crowdsourced citizen hotspot "
        "alerts and historical fill averages rather than continuous real-time bin sensor telemetry."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 14: CONCLUSION
    # ==========================================
    add_heading_1("14. Conclusion")
    add_paragraph(
        "The development and deployment of the GPS-Based Fleet Tracking and Route Verification System (CivicClean GIS) successfully "
        "demonstrates the power of Software Engineering principles in resolving complex, real-world civic challenges. By selecting "
        "and implementing Solution 2?a pure software-only architecture?this project achieved complete operational transparency, route "
        "verifiability, and administrative accountability in municipal solid waste collection without incurring any capital expense for "
        "custom in-bin hardware sensors."
    )
    add_paragraph(
        "The system seamlessly unifies all four key municipal stakeholders through purpose-built interfaces: sanitation supervisors gain "
        "real-time GIS visibility and tamper-resistant audit logs; truck drivers benefit from mobile geofenced manifests with one-tap photo "
        "verification; city residents are empowered through geotagged grievance reporting with live ticket tracking; and urban planners "
        "receive empirical performance analytics. Comprehensive unit, integration, and system validation confirmed sub-10-meter geofence "
        "precision, instantaneous exception logging, and resilient performance across diverse client devices."
    )
    add_paragraph(
        "In conclusion, CivicClean GIS provides an economically viable, technically robust, and socially impactful software foundation "
        "that enables municipal corporations to transition from inefficient, manual, and reactive waste management toward intelligent, "
        "verifiable, and citizen-centric smart city sanitation governance."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 15: REFERENCES
    # ==========================================
    add_heading_1("15. References")
    add_paragraph(
        "The design, architectural modeling, and software engineering methodologies implemented in this project were informed by "
        "the following academic textbooks, standards, and research publications:"
    )
    add_bullet("Textbook [1]", "Roger S. Pressman and Bruce R. Maxim, \"Software Engineering: A Practitioner's Approach\", 9th Edition, McGraw-Hill Education, 2020.")
    add_bullet("Textbook [2]", "Ian Sommerville, \"Software Engineering\", 10th Edition, Pearson Education, 2016.")
    add_bullet("IEEE Journal [3]", "M. A. Hannan, M. Arebey, R. A. Begum, and H. Basri, \"An Automated Waste Collection System using RFID and GPS Technology\", IEEE Transactions on Intelligent Transportation Systems, Vol. 13, No. 3, pp. 1329?1338, 2012.")
    add_bullet("Journal Article [4]", "A. Zanella, N. Bui, A. Castellani, L. Vangelista, and M. Zorzi, \"Internet of Things for Smart Cities\", IEEE Internet of Things Journal, Vol. 1, No. 1, pp. 22?32, 2014.")
    add_bullet("Standard [5]", "Object Management Group (OMG), \"Unified Modeling Language (OMG UML) Specification\", Version 2.5.1, formal/2017-12-05, 2017.")
    add_bullet("Web Specification [6]", "World Wide Web Consortium (W3C), \"Geolocation API Specification (2nd Edition)\", W3C Recommendation, 2016. [Online]. Available: https://www.w3.org/TR/geolocation-API/")
    add_bullet("GIS Documentation [7]", "Vladimir Agafonkin, \"Leaflet: An Open-Source JavaScript Library for Mobile-Friendly Interactive Maps\", Version 1.9.4, 2023. [Online]. Available: https://leafletjs.com/")

    doc.add_page_break()

    # ==========================================
    # APPENDIX
    # ==========================================
    add_heading_1("Appendix")
    
    add_heading_2("Appendix A: System User Manual & Operating Guide")
    add_paragraph(
        "This user manual provides step-by-step operating instructions for all three authorized user roles:"
    )
    add_bullet("A.1 Supervisor Operating Guide", "1. Open Google Chrome or Microsoft Edge and navigate to http://localhost:3000.\n2. Click on the 'Supervisor Dashboard' tab.\n3. Review the top KPI cards for today's collection progress.\n4. Use the interactive GIS map to monitor vehicle TRK-01 movement.\n5. Click 'Start GPS Sim' to simulate active vehicle transit.\n6. Inspect the side 'Proof-of-Service Stream' to review driver-submitted photos and GPS accuracy.\n7. Review the bottom 'Proof-of-Service Audit Trail' table for official records.")
    add_bullet("A.2 Driver Field App Guide", "1. Launch the mobile web application on the smartphone mounted in the compactor cab.\n2. Tap the 'Driver Field App' tab.\n3. Verify the green banner shows 'GPS Active & Geofencing Enabled (?4m Accuracy)'.\n4. Review the chronological checklist of assigned checkpoints.\n5. Upon reaching a bin location, tap 'Mark Collected', capture the photo proof, and confirm.\n6. If a roadway is blocked, tap 'Skip', select the appropriate obstruction reason, input remarks, and confirm.")
    add_bullet("A.3 Citizen Grievance Portal Guide", "1. Navigate to http://localhost:3000 and select the 'Citizen Portal' tab.\n2. Fill out your Full Name, Mobile Number, and select your Municipal Ward.\n3. Choose the Issue Category (e.g., Overflowing Public Bin or Missed Pickup).\n4. Tap 'GPS Pin' to automatically capture your smartphone's latitude/longitude coordinates.\n5. Attach a photo of the waste overflow and click 'Submit Waste Report'.\n6. Record the generated Ticket ID (e.g., CMP-2026-104) and enter it in the 'Track Your Grievance Status' search box to monitor clearance progress.")

    add_heading_2("Appendix B: REST API Payloads & Data Schemas")
    add_paragraph(
        "The CivicClean backend exposes stateless REST API endpoints communicating via JSON payloads. Core endpoint schemas include:"
    )
    add_bullet("GET /api/status", "Returns fleet-wide summary metrics: total stops, collected count, skipped count, active trucks, open complaints, and total waste weight.")
    add_bullet("GET /api/vehicles", "Returns vehicle array containing registration number, driver name, live coordinates, speed (km/h), fuel level, and route waypoints.")
    add_bullet("POST /api/stops/:id/collect", "Accepts JSON payload: { proofPhoto: string, weightKg: number }. Validates geofence proximity and updates checkpoint state.")
    add_bullet("POST /api/stops/:id/skip", "Accepts JSON payload: { reason: string }. Flags checkpoint as skipped and logs justification to audit trail.")
    add_bullet("POST /api/complaints", "Accepts JSON payload: { citizenName, phone, ward, category, location, lat, lng, description, photoUrl }. Generates ticket ID.")

    add_heading_2("Appendix C: Project Book Spiral Binding Guidelines")
    add_paragraph(
        "To ensure compliance with the academic evaluation standards of the Department of Computer Science and Engineering, Anil "
        "Neerukonda Institute of Technology and Sciences (Autonomous), the following physical binding and printing specifications "
        "must be observed when preparing the final project report book:"
    )
    add_bullet("C.1 Margin & Gutter Compliance", "The document has been formatted with an expanded left margin of 1.25 inches (3.175 cm) to provide the necessary 0.25-inch gutter allowance for spiral coil perforation. Top, bottom, and right margins are set to exactly 1.0 inch (2.54 cm). No text or diagrams will be truncated or obscured by the binding holes.")
    add_bullet("C.2 Paper Quality & Printing Specifications", "The report should be printed on standard Executive A4 Bond Paper with a minimum weight of 85 to 100 GSM. High-resolution color printing is required for the Cover Page, Certificate, all UML/DFD diagrams, and application screenshots.")
    add_bullet("C.3 Front Cover Protection", "The front of the spiral-bound project book must be protected by a heavy transparent plastic sheet (minimum 250 microns thickness) to display the title page cleanly while protecting against moisture and dust.")
    add_bullet("C.4 Rear Backing Sheet", "The back of the project book must feature a rigid, opaque plastic or leatherette cardstock sheet (navy blue or black) to provide structural rigidity during handling and evaluation.")
    add_bullet("C.5 Spiral Coil Binding Specifications", "Binding must be executed using high-grade black or navy blue PVC plastic spiral coil or metal wire-O twin loop binding with a diameter appropriately matched to the total page thickness (typically 12mm to 16mm). All pages must turn smoothly without catching or tearing.")

    print("Chapters 11 to End generated successfully.")
