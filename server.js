const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;

// In-Memory Database for Municipal Waste Collection (Solution 2: Software-Only GPS Tracking)
let state = {
  vehicles: [
    {
      id: 'TRK-01',
      regNo: 'AP39-TM-1001',
      driverName: 'Ramesh Kumar',
      phone: '+91 98480 12345',
      type: 'Compactor (4-Ton)',
      status: 'En Route',
      speedKmh: 24,
      fuelLevel: '78%',
      currentLat: 17.8974,
      currentLng: 83.4485,
      routeId: 'ROUTE-NORTH-01',
      currentStopIndex: 2,
      lastUpdated: new Date().toLocaleTimeString()
    },
    {
      id: 'TRK-02',
      regNo: 'AP39-TM-1002',
      driverName: 'Suresh Varma',
      phone: '+91 98480 54321',
      type: 'Tipper Truck (2.5-Ton)',
      status: 'At Depot',
      speedKmh: 0,
      fuelLevel: '92%',
      currentLat: 17.8860,
      currentLng: 83.4350,
      routeId: 'ROUTE-SOUTH-02',
      currentStopIndex: 0,
      lastUpdated: new Date().toLocaleTimeString()
    }
  ],
  stops: [
    {
      id: 'STOP-01',
      routeId: 'ROUTE-NORTH-01',
      sequence: 1,
      name: 'Sangivalasa Junction Main Market',
      zone: 'Ward 1 - North',
      lat: 17.9015,
      lng: 83.4420,
      targetTime: '06:30 AM',
      status: 'Collected',
      completedTime: '06:38 AM',
      driverId: 'TRK-01',
      proofPhoto: 'https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=400&q=80',
      proofTimestamp: '2026-10-04 06:38:12',
      verificationStatus: 'Geo-Verified (Within 8m)',
      weightKg: 420
    },
    {
      id: 'STOP-02',
      routeId: 'ROUTE-NORTH-01',
      sequence: 2,
      name: 'ANITS Campus North Gate & Hostels',
      zone: 'Ward 1 - North',
      lat: 17.8995,
      lng: 83.4452,
      targetTime: '07:15 AM',
      status: 'Collected',
      completedTime: '07:22 AM',
      driverId: 'TRK-01',
      proofPhoto: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80',
      proofTimestamp: '2026-10-04 07:22:45',
      verificationStatus: 'Geo-Verified (Within 5m)',
      weightKg: 380
    },
    {
      id: 'STOP-03',
      routeId: 'ROUTE-NORTH-01',
      sequence: 3,
      name: 'Bheemili Beach Road Commercial Complex',
      zone: 'Ward 2 - Coastal',
      lat: 17.8942,
      lng: 83.4510,
      targetTime: '08:00 AM',
      status: 'Pending',
      completedTime: null,
      driverId: 'TRK-01',
      proofPhoto: null,
      proofTimestamp: null,
      verificationStatus: 'Awaiting Truck Arrival',
      weightKg: 0
    },
    {
      id: 'STOP-04',
      routeId: 'ROUTE-NORTH-01',
      sequence: 4,
      name: 'Tagarapuvalasa Weekly Market Yard',
      zone: 'Ward 3 - East',
      lat: 17.8910,
      lng: 83.4580,
      targetTime: '08:45 AM',
      status: 'Pending',
      completedTime: null,
      driverId: 'TRK-01',
      proofPhoto: null,
      proofTimestamp: null,
      verificationStatus: 'Scheduled',
      weightKg: 0
    },
    {
      id: 'STOP-05',
      routeId: 'ROUTE-NORTH-01',
      sequence: 5,
      name: 'RTC Bus Stand Civic Waste Depot',
      zone: 'Ward 3 - East',
      lat: 17.8875,
      lng: 83.4625,
      targetTime: '09:30 AM',
      status: 'Pending',
      completedTime: null,
      driverId: 'TRK-01',
      proofPhoto: null,
      proofTimestamp: null,
      verificationStatus: 'Scheduled',
      weightKg: 0
    },
    {
      id: 'STOP-06',
      routeId: 'ROUTE-NORTH-01',
      sequence: 6,
      name: 'Anandapuram Bypass Crossroad',
      zone: 'Ward 4 - West',
      lat: 17.8830,
      lng: 83.4530,
      targetTime: '10:15 AM',
      status: 'Skipped',
      completedTime: '10:20 AM',
      driverId: 'TRK-01',
      proofPhoto: null,
      proofTimestamp: '2026-10-04 10:20:05',
      verificationStatus: 'Flagged: Road Excavation Blockage',
      skippedReason: 'Access road blocked due to underground drainage work',
      weightKg: 0
    }
  ],
  complaints: [
    {
      id: 'CMP-2026-104',
      citizenName: 'M. Venkat Rao',
      phone: '+91 94401 88231',
      ward: 'Ward 2 - Coastal',
      location: 'Near Bheemili Lighthouse Old Fish Market',
      lat: 17.8935,
      lng: 83.4522,
      category: 'Overflowing Public Bin',
      description: 'Garbage bin overflowing onto the pedestrian lane since yesterday evening.',
      photoUrl: 'https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&w=400&q=80',
      status: 'Open',
      assignedTruck: 'TRK-01',
      reportedAt: 'Today, 07:45 AM'
    },
    {
      id: 'CMP-2026-105',
      citizenName: 'K. Lakshmi Devi',
      phone: '+91 98492 44109',
      ward: 'Ward 1 - North',
      location: 'Opposite Community Hall, Sangivalasa',
      lat: 17.9008,
      lng: 83.4435,
      category: 'Missed Scheduled Pickup',
      description: 'Secondary collection truck did not visit street 4 this morning.',
      photoUrl: 'https://images.unsplash.com/photo-1530587191325-3db32d826c18?auto=format&fit=crop&w=400&q=80',
      status: 'Assigned',
      assignedTruck: 'TRK-01',
      reportedAt: 'Today, 08:10 AM'
    }
  ],
  auditLogs: [
    {
      id: 'LOG-01',
      timestamp: '06:38:12',
      vehicleId: 'AP39-TM-1001',
      stopName: 'Sangivalasa Junction Main Market',
      action: 'COLLECTION_VERIFIED',
      driver: 'Ramesh Kumar',
      geoAccuracy: '8 meters',
      status: 'SUCCESS'
    },
    {
      id: 'LOG-02',
      timestamp: '07:22:45',
      vehicleId: 'AP39-TM-1001',
      stopName: 'ANITS Campus North Gate & Hostels',
      action: 'COLLECTION_VERIFIED',
      driver: 'Ramesh Kumar',
      geoAccuracy: '5 meters',
      status: 'SUCCESS'
    },
    {
      id: 'LOG-03',
      timestamp: '10:20:05',
      vehicleId: 'AP39-TM-1001',
      stopName: 'Anandapuram Bypass Crossroad',
      action: 'STOP_SKIPPED',
      driver: 'Ramesh Kumar',
      reason: 'Access road blocked due to underground drainage work',
      status: 'WARNING'
    }
  ]
};

// Route waypoints for vehicle GPS simulation
const routeCoordinates = [
  [17.9020, 83.4410],
  [17.9015, 83.4420], // Stop 1
  [17.9002, 83.4438],
  [17.8995, 83.4452], // Stop 2
  [17.8974, 83.4485], // Current truck pos
  [17.8955, 83.4498],
  [17.8942, 83.4510], // Stop 3
  [17.8925, 83.4545],
  [17.8910, 83.4580], // Stop 4
  [17.8890, 83.4600],
  [17.8875, 83.4625], // Stop 5
  [17.8850, 83.4570],
  [17.8830, 83.4530]  // Stop 6
];

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    return res.end();
  }

  // --- API Endpoints ---
  if (pathname === '/api/status' && req.method === 'GET') {
    const totalStops = state.stops.length;
    const collected = state.stops.filter(s => s.status === 'Collected').length;
    const skipped = state.stops.filter(s => s.status === 'Skipped').length;
    const pending = state.stops.filter(s => s.status === 'Pending').length;
    const totalWasteKg = state.stops.reduce((acc, s) => acc + (s.weightKg || 0), 0);

    return sendJSON(res, 200, {
      totalStops,
      collected,
      skipped,
      pending,
      completionRate: Math.round((collected / totalStops) * 100),
      totalWasteKg,
      activeTrucks: state.vehicles.filter(v => v.status !== 'At Depot').length,
      openComplaints: state.complaints.filter(c => c.status !== 'Resolved').length
    });
  }

  if (pathname === '/api/vehicles' && req.method === 'GET') {
    return sendJSON(res, 200, { vehicles: state.vehicles, routeCoordinates });
  }

  if (pathname === '/api/stops' && req.method === 'GET') {
    return sendJSON(res, 200, { stops: state.stops });
  }

  if (pathname.startsWith('/api/stops/') && pathname.endsWith('/collect') && req.method === 'POST') {
    const stopId = pathname.split('/')[3];
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      const data = body ? JSON.parse(body) : {};
      const stop = state.stops.find(s => s.id === stopId);
      if (!stop) return sendJSON(res, 404, { error: 'Stop not found' });

      stop.status = 'Collected';
      stop.completedTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      stop.proofTimestamp = new Date().toLocaleString();
      stop.proofPhoto = data.proofPhoto || 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=400&q=80';
      stop.verificationStatus = 'Geo-Verified (GPS Matched: 4m)';
      stop.weightKg = data.weightKg || Math.floor(Math.random() * 200 + 250);

      state.auditLogs.unshift({
        id: 'LOG-' + Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        vehicleId: 'AP39-TM-1001',
        stopName: stop.name,
        action: 'COLLECTION_VERIFIED',
        driver: 'Ramesh Kumar',
        geoAccuracy: '4 meters',
        status: 'SUCCESS'
      });

      return sendJSON(res, 200, { success: true, stop });
    });
    return;
  }

  if (pathname.startsWith('/api/stops/') && pathname.endsWith('/skip') && req.method === 'POST') {
    const stopId = pathname.split('/')[3];
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      const data = body ? JSON.parse(body) : {};
      const stop = state.stops.find(s => s.id === stopId);
      if (!stop) return sendJSON(res, 404, { error: 'Stop not found' });

      stop.status = 'Skipped';
      stop.completedTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      stop.skippedReason = data.reason || 'Blocked access or road under construction';
      stop.verificationStatus = 'Flagged: ' + stop.skippedReason;

      state.auditLogs.unshift({
        id: 'LOG-' + Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        vehicleId: 'AP39-TM-1001',
        stopName: stop.name,
        action: 'STOP_SKIPPED',
        driver: 'Ramesh Kumar',
        reason: stop.skippedReason,
        status: 'WARNING'
      });

      return sendJSON(res, 200, { success: true, stop });
    });
    return;
  }

  if (pathname === '/api/complaints' && req.method === 'GET') {
    return sendJSON(res, 200, { complaints: state.complaints });
  }

  if (pathname === '/api/complaints' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const newComplaint = {
          id: 'CMP-2026-' + (100 + state.complaints.length + 1),
          citizenName: data.citizenName || 'Resident',
          phone: data.phone || '+91 99999 00000',
          ward: data.ward || 'Ward 1 - North',
          location: data.location || 'Reported Location',
          lat: data.lat || 17.8960,
          lng: data.lng || 83.4490,
          category: data.category || 'Overflowing Public Bin',
          description: data.description || 'Public bin overflowing.',
          photoUrl: data.photoUrl || 'https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&w=400&q=80',
          status: 'Open',
          assignedTruck: 'TRK-01',
          reportedAt: 'Just now'
        };
        state.complaints.unshift(newComplaint);
        return sendJSON(res, 201, { success: true, complaint: newComplaint });
      } catch (err) {
        return sendJSON(res, 400, { error: 'Invalid JSON payload' });
      }
    });
    return;
  }

  if (pathname === '/api/audit' && req.method === 'GET') {
    return sendJSON(res, 200, { logs: state.auditLogs });
  }

  // --- Static Files Serving ---
  let filePath = path.join(__dirname, 'public', pathname === '/' ? 'index.html' : pathname);
  const ext = path.extname(filePath).toLowerCase();

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      filePath = path.join(__dirname, 'public', 'index.html');
    }
    fs.readFile(filePath, (readErr, content) => {
      if (readErr) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        return res.end('500 Server Error: ' + readErr.message);
      }
      res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'text/html' });
      res.end(content);
    });
  });
});

server.listen(PORT, () => {
  console.log('CivicClean Server running on http://localhost:' + PORT);
});
