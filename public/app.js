// CivicClean GIS - Core Application Logic
let currentTab = 'supervisor';
let map = null;
let vehicleMarker = null;
let routeLine = null;
let stopMarkers = [];
let complaintMarkers = [];
let simInterval = null;
let isSimulating = false;
let currentWaypointIndex = 4;
let pendingSkipStopId = null;

let stopsData = [];
let vehiclesData = [];
let complaintsData = [];
let routeWaypoints = [];

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initMap();
  loadData();
  setInterval(loadData, 10000); // Poll updates every 10s
});

// Tab Switcher
function switchTab(tabId) {
  currentTab = tabId;
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.view-pane').forEach(pane => pane.classList.remove('active'));

  const activeBtn = document.getElementById('tab-' + tabId);
  const activePane = document.getElementById('view-' + tabId);
  if (activeBtn) activeBtn.classList.add('active');
  if (activePane) activePane.classList.add('active');

  if (tabId === 'supervisor' && map) {
    setTimeout(() => { map.invalidateSize(); }, 200);
  }
}

// Clock
function initClock() {
  const clockEl = document.getElementById('live-clock');
  function update() {
    const now = new Date();
    clockEl.innerText = now.toLocaleTimeString('en-US', { hour12: false });
  }
  update();
  setInterval(update, 1000);
}

// Map Initialization
function initMap() {
  map = L.map('fleet-map').setView([17.8960, 83.4500], 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
}

// Fetch Initial Data
async function loadData() {
  try {
    const [statusRes, vehRes, stopsRes, compRes, auditRes] = await Promise.all([
      fetch('/api/status').then(r => r.json()),
      fetch('/api/vehicles').then(r => r.json()),
      fetch('/api/stops').then(r => r.json()),
      fetch('/api/complaints').then(r => r.json()),
      fetch('/api/audit').then(r => r.json())
    ]);

    stopsData = stopsRes.stops || [];
    vehiclesData = vehRes.vehicles || [];
    routeWaypoints = vehRes.routeCoordinates || [];
    complaintsData = compRes.complaints || [];

    updateKPIs(statusRes);
    renderMapElements();
    renderVerificationFeed();
    renderAuditTable(auditRes.logs || []);
    renderComplaintsTable(complaintsData);
    renderDriverManifest();
  } catch (err) {
    console.error('Error fetching data:', err);
  }
}

// Update KPI Header Cards
function updateKPIs(status) {
  document.getElementById('kpi-total-stops').innerText = status.totalStops;
  document.getElementById('kpi-collected').innerText = status.collected;
  document.getElementById('kpi-rate').innerText = `(${status.completionRate}%)`;
  document.getElementById('kpi-skipped').innerText = status.skipped;
  document.getElementById('kpi-trucks').innerText = `${status.activeTrucks} Active`;
  document.getElementById('kpi-complaints').innerText = `${status.openComplaints} Open`;
  document.getElementById('kpi-waste').innerText = `${status.totalWasteKg} kg`;
}

// Render Map Markers & Routes
function renderMapElements() {
  if (!map) return;

  // Clear existing markers
  stopMarkers.forEach(m => map.removeLayer(m));
  stopMarkers = [];
  complaintMarkers.forEach(m => map.removeLayer(m));
  complaintMarkers = [];

  // Draw Route Polyline
  if (routeWaypoints.length > 0 && !routeLine) {
    routeLine = L.polyline(routeWaypoints, {
      color: '#2563eb',
      weight: 5,
      opacity: 0.7,
      dashArray: '8, 8'
    }).addTo(map);
  }

  // Draw Stops
  stopsData.forEach(stop => {
    let color = '#f59e0b'; // pending
    let iconClass = 'fa-clock';
    if (stop.status === 'Collected') {
      color = '#10b981';
      iconClass = 'fa-check';
    } else if (stop.status === 'Skipped') {
      color = '#ef4444';
      iconClass = 'fa-ban';
    }

    const customIcon = L.divIcon({
      className: 'custom-stop-marker',
      html: `<div style="background-color: ${color}; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 11px;">
               <i class="fa-solid ${iconClass}"></i>
             </div>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    const marker = L.marker([stop.lat, stop.lng], { icon: customIcon }).addTo(map);
    marker.bindPopup(`
      <div style="font-family: Inter, sans-serif; font-size: 12px; min-width: 180px;">
        <strong style="display:block; font-size: 13px; color:#0f172a; margin-bottom: 3px;">${stop.name}</strong>
        <span style="color: #64748b;">${stop.zone}</span><br>
        <span style="display:inline-block; margin-top:5px; padding: 2px 6px; border-radius: 4px; font-weight:600; font-size:11px; color:white; background:${color};">
          ${stop.status.toUpperCase()}
        </span>
        ${stop.completedTime ? `<div style="margin-top:6px; color:#10b981;"><b>Time:</b> ${stop.completedTime}</div>` : ''}
        ${stop.verificationStatus ? `<div style="margin-top:2px; color:#3b82f6;"><small>${stop.verificationStatus}</small></div>` : ''}
        ${stop.skippedReason ? `<div style="margin-top:4px; color:#ef4444;"><small><b>Reason:</b> ${stop.skippedReason}</small></div>` : ''}
      </div>
    `);
    stopMarkers.push(marker);
  });

  // Draw Citizen Hotspots
  complaintsData.forEach(comp => {
    if (comp.lat && comp.lng && comp.status !== 'Resolved') {
      const compIcon = L.divIcon({
        className: 'comp-marker',
        html: `<div style="background-color: #8b5cf6; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 10px;">
                 <i class="fa-solid fa-bullhorn"></i>
               </div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const m = L.marker([comp.lat, comp.lng], { icon: compIcon }).addTo(map);
      m.bindPopup(`
        <div style="font-family: Inter, sans-serif; font-size: 12px; min-width: 160px;">
          <strong style="color: #8b5cf6;">[Citizen Alert] ${comp.id}</strong><br>
          <b>Location:</b> ${comp.location}<br>
          <b>Issue:</b> ${comp.category}<br>
          <small style="color:#64748b;">${comp.description}</small>
        </div>
      `);
      complaintMarkers.push(m);
    }
  });

  // Draw Vehicle Marker
  if (vehiclesData.length > 0) {
    const v = vehiclesData[0];
    const truckIcon = L.divIcon({
      className: 'truck-marker',
      html: `<div style="background-color: #2563eb; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 3px solid #ffffff; box-shadow: 0 3px 8px rgba(37,99,235,0.4); font-size: 14px;">
               <i class="fa-solid fa-truck"></i>
             </div>`,
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });

    if (!vehicleMarker) {
      vehicleMarker = L.marker([v.currentLat, v.currentLng], { icon: truckIcon }).addTo(map);
      vehicleMarker.bindPopup(`
        <div style="font-family: Inter, sans-serif; font-size: 12px;">
          <strong style="font-size: 13px;">${v.regNo} (${v.id})</strong><br>
          <b>Driver:</b> ${v.driverName}<br>
          <b>Speed:</b> ${v.speedKmh} km/h | <b>Fuel:</b> ${v.fuelLevel}<br>
          <span style="color:#10b981; font-weight:600;">Status: ${v.status}</span>
        </div>
      `);
    } else {
      vehicleMarker.setLatLng([v.currentLat, v.currentLng]);
    }
  }
}

// Side Verification Stream
function renderVerificationFeed() {
  const container = document.getElementById('verification-stream');
  if (!container) return;

  const verifiedStops = stopsData.filter(s => s.status === 'Collected');
  if (verifiedStops.length === 0) {
    container.innerHTML = '<p class="text-muted" style="font-size:12px;">No verifications yet.</p>';
    return;
  }

  container.innerHTML = verifiedStops.map(s => `
    <div class="stream-card">
      <img src="${s.proofPhoto || 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80'}" class="stream-thumb" alt="Proof">
      <div class="stream-info">
        <strong>${s.name}</strong>
        <p class="stream-meta"><i class="fa-regular fa-clock"></i> ${s.completedTime || '07:22 AM'} | <b>${s.weightKg} kg</b></p>
        <span class="badge-success"><i class="fa-solid fa-check"></i> ${s.verificationStatus}</span>
      </div>
    </div>
  `).join('');
}

// Audit Table
function renderAuditTable(logs) {
  const tbody = document.getElementById('audit-tbody');
  if (!tbody) return;

  tbody.innerHTML = logs.map(l => `
    <tr>
      <td><code>${l.timestamp}</code></td>
      <td><strong>${l.vehicleId}</strong></td>
      <td>${l.stopName}</td>
      <td><span class="${l.action === 'COLLECTION_VERIFIED' ? 'text-success' : 'text-danger'}"><b>${l.action}</b></span></td>
      <td>${l.geoAccuracy ? `<span class="badge-info">${l.geoAccuracy}</span>` : `<span class="text-muted">${l.reason || 'N/A'}</span>`}</td>
      <td><span class="${l.status === 'SUCCESS' ? 'badge-success' : 'badge-warning'}">${l.status}</span></td>
    </tr>
  `).join('');
}

// Complaints Table
function renderComplaintsTable(complaints) {
  const tbody = document.getElementById('complaints-tbody');
  if (!tbody) return;

  tbody.innerHTML = complaints.map(c => `
    <tr>
      <td><strong>${c.id}</strong></td>
      <td>${c.citizenName}<br><small class="text-muted">${c.ward}</small></td>
      <td>${c.category}</td>
      <td><span class="${c.status === 'Resolved' ? 'badge-success' : 'badge-warning'}">${c.status}</span></td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="locateComplaint(${c.lat}, ${c.lng})">
          <i class="fa-solid fa-location-crosshairs"></i> View
        </button>
      </td>
    </tr>
  `).join('');
}

function locateComplaint(lat, lng) {
  if (map && lat && lng) {
    switchTab('supervisor');
    map.setView([lat, lng], 16);
    showToast(`Focused on complaint location (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
  }
}

// Driver Field Portal Manifest
function renderDriverManifest() {
  const container = document.getElementById('driver-stops-list');
  const progText = document.getElementById('driver-progress-text');
  const progBar = document.getElementById('driver-progress-bar');
  if (!container) return;

  const total = stopsData.length;
  const collected = stopsData.filter(s => s.status === 'Collected').length;
  const pct = Math.round((collected / total) * 100);

  if (progText) progText.innerText = `${collected} / ${total} Stops (${pct}%)`;
  if (progBar) progBar.style.width = `${pct}%`;

  container.innerHTML = stopsData.map((s, idx) => {
    let statusClass = 'pending';
    let statusBadge = '<span class="badge-warning">Pending</span>';

    if (s.status === 'Collected') {
      statusClass = 'collected';
      statusBadge = '<span class="badge-success"><i class="fa-solid fa-check"></i> Collected</span>';
    } else if (s.status === 'Skipped') {
      statusClass = 'skipped';
      statusBadge = '<span class="badge-danger"><i class="fa-solid fa-ban"></i> Skipped</span>';
    }

    return `
      <div class="manifest-card ${statusClass}">
        <div class="manifest-header">
          <div>
            <span class="manifest-name">#${s.sequence}. ${s.name}</span>
            <div class="manifest-zone">${s.zone}</div>
          </div>
          ${statusBadge}
        </div>
        <div class="manifest-meta">
          <i class="fa-regular fa-clock"></i> Target: ${s.targetTime}
          ${s.completedTime ? ` | <b>Finished: ${s.completedTime}</b>` : ''}
        </div>
        ${s.status === 'Pending' ? `
          <div class="manifest-actions">
            <button class="btn btn-sm btn-primary" onclick="markCollected('${s.id}')">
              <i class="fa-solid fa-camera"></i> Mark Collected
            </button>
            <button class="btn btn-sm btn-outline text-danger" onclick="openSkipModal('${s.id}', '${s.name}')">
              <i class="fa-solid fa-forward"></i> Skip
            </button>
          </div>
        ` : ''}
        ${s.skippedReason ? `<div style="font-size:11px; color:#ef4444; margin-top:4px;"><b>Reason:</b> ${s.skippedReason}</div>` : ''}
      </div>
    `;
  }).join('');
}

// Driver Actions
async function markCollected(stopId) {
  try {
    const res = await fetch(`/api/stops/${stopId}/collect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        proofPhoto: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80',
        weightKg: Math.floor(Math.random() * 150 + 300)
      })
    });
    const result = await res.json();
    if (result.success) {
      showToast(`Stop ${result.stop.name} marked as Collected with GPS lock!`);
      loadData();
    }
  } catch (err) {
    showToast('Failed to mark collected.');
  }
}

function openSkipModal(stopId, stopName) {
  pendingSkipStopId = stopId;
  document.getElementById('skip-stop-name').innerText = stopName;
  document.getElementById('skip-modal').classList.remove('hidden');
}

function closeSkipModal() {
  pendingSkipStopId = null;
  document.getElementById('skip-modal').classList.add('hidden');
}

async function confirmSkipStop() {
  if (!pendingSkipStopId) return;
  const reasonCategory = document.getElementById('skip-reason-select').value;
  const remarks = document.getElementById('skip-remarks').value;
  const fullReason = remarks ? `${reasonCategory} (${remarks})` : reasonCategory;

  try {
    const res = await fetch(`/api/stops/${pendingSkipStopId}/skip`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: fullReason })
    });
    const result = await res.json();
    if (result.success) {
      showToast(`Stop skipped: ${result.stop.name}`);
      closeSkipModal();
      loadData();
    }
  } catch (err) {
    showToast('Failed to log skip reason.');
  }
}

// GPS Simulation Controls
function toggleSimulation() {
  if (isSimulating) {
    clearInterval(simInterval);
    isSimulating = false;
    document.getElementById('sim-icon').className = 'fa-solid fa-play';
    document.getElementById('sim-text').innerText = 'Resume GPS Sim';
    showToast('GPS Fleet Simulation Paused');
  } else {
    isSimulating = true;
    document.getElementById('sim-icon').className = 'fa-solid fa-pause';
    document.getElementById('sim-text').innerText = 'Pause GPS Sim';
    showToast('Live Vehicle GPS Tracking Simulation Started');

    simInterval = setInterval(() => {
      stepSimulationNext();
    }, 3000);
  }
}

function stepSimulationNext() {
  if (routeWaypoints.length === 0) return;
  currentWaypointIndex = (currentWaypointIndex + 1) % routeWaypoints.length;
  const pt = routeWaypoints[currentWaypointIndex];

  if (vehicleMarker) {
    vehicleMarker.setLatLng(pt);
  }

  // Update telemetry speed
  const speed = Math.floor(Math.random() * 15 + 20);
  const teleSpeed = document.getElementById('tele-speed');
  if (teleSpeed) teleSpeed.innerText = `${speed} km/h`;
}

function resetSimulation() {
  if (isSimulating) toggleSimulation();
  currentWaypointIndex = 0;
  if (routeWaypoints.length > 0 && vehicleMarker) {
    vehicleMarker.setLatLng(routeWaypoints[0]);
  }
  showToast('Simulation reset to depot.');
}

// Citizen Complaint Functions
function useCurrentLocation() {
  const locInput = document.getElementById('cit-location');
  const hint = document.getElementById('cit-coords-hint');
  locInput.value = 'Sangivalasa Junction Main Market Road';
  hint.innerText = 'Coordinates: Lat 17.8970, Lng 83.4475 (High Precision GPS)';
  showToast('GPS Coordinates Captured from Device');
}

function handlePhotoUpload(input) {
  if (input.files && input.files[0]) {
    document.getElementById('cit-file-label').innerText = `Photo selected: ${input.files[0].name}`;
  }
}

async function submitCitizenComplaint(e) {
  e.preventDefault();
  const name = document.getElementById('cit-name').value;
  const phone = document.getElementById('cit-phone').value;
  const ward = document.getElementById('cit-ward').value;
  const category = document.getElementById('cit-category').value;
  const location = document.getElementById('cit-location').value;
  const desc = document.getElementById('cit-desc').value;

  try {
    const res = await fetch('/api/complaints', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        citizenName: name,
        phone,
        ward,
        category,
        location,
        description: desc
      })
    });
    const result = await res.json();
    if (result.success) {
      showToast(`Complaint submitted! Ticket: ${result.complaint.id}`);
      document.getElementById('citizen-report-form').reset();
      document.getElementById('cit-file-label').innerText = 'Tap to upload photo or take picture';

      // Auto update track box
      document.getElementById('track-ticket-num').innerText = result.complaint.id;
      document.getElementById('track-ticket-desc').innerText = result.complaint.location;
      document.getElementById('track-ticket-status').innerText = 'OPEN / ASSIGNED';

      loadData();
    }
  } catch (err) {
    showToast('Error submitting complaint.');
  }
}

function trackComplaint() {
  const ticketId = document.getElementById('track-ticket-id').value.trim();
  if (!ticketId) {
    showToast('Please enter a Ticket ID');
    return;
  }
  const match = complaintsData.find(c => c.id.toLowerCase() === ticketId.toLowerCase());
  if (match) {
    document.getElementById('track-ticket-num').innerText = match.id;
    document.getElementById('track-ticket-desc').innerText = `${match.location} - ${match.category}`;
    document.getElementById('track-ticket-status').innerText = match.status.toUpperCase();
    showToast(`Found Ticket ${match.id}`);
  } else {
    showToast(`Ticket ${ticketId} not found.`);
  }
}

// Toast helper
function showToast(msg) {
  const toast = document.getElementById('notification-toast');
  if (!toast) return;
  toast.innerText = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 3500);
}
