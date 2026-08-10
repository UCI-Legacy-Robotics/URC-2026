// GNSS map — driven entirely from Python via page().runJavaScript(...).
// Pins are added by manual coordinate entry in the GUI, not by clicking
// the map, so there is no click -> Python event wiring here by design.

// Default center: UCI campus. Swap this once real competition-area
// (MDRS, Utah) tiles are downloaded — see scripts/download_tiles.py.
const DEFAULT_CENTER = [33.6405, -117.8443];
const DEFAULT_ZOOM = 16;
const MIN_ZOOM = 15;
const MAX_ZOOM = 17;

const map = L.map('map', {
  zoomControl: true,
  attributionControl: true,
}).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

// Local offline tiles only — no CDN/live tile fetching, competition site
// has no internet access. Run scripts/download_tiles.py to populate
// tiles/{z}/{x}/{y}.png before this will show anything but blanks.
L.tileLayer('tiles/{z}/{x}/{y}.png', {
  minZoom: MIN_ZOOM,
  maxZoom: MAX_ZOOM,
  noWrap: true,
  attribution: '&copy; OpenStreetMap contributors',
  errorTileUrl: '', // missing tiles just render blank, not broken-image icons
}).addTo(map);

// -- Rover position marker (with heading rotation) -------------------

const roverIcon = L.divIcon({
  className: '',
  html: '<div class="rover-marker-icon"></div>',
  iconSize: [18, 22],
  iconAnchor: [9, 11],
});

let roverMarker = null;

function setRoverPosition(lat, lon, headingDegrees) {
  const latLng = [lat, lon];
  if (roverMarker === null) {
    roverMarker = L.marker(latLng, {
      icon: roverIcon,
      rotationAngle: headingDegrees,
      rotationOrigin: 'center center',
    }).addTo(map);
  } else {
    roverMarker.setLatLng(latLng);
    roverMarker.setRotationAngle(headingDegrees);
  }
}

function setRoverStale(isStale) {
  if (roverMarker === null) return;
  const el = roverMarker.getElement();
  if (el) {
    el.style.opacity = isStale ? '0.35' : '1.0';
  }
}

function centerOnRover() {
  if (roverMarker !== null) {
    map.panTo(roverMarker.getLatLng());
  }
}

// -- Manually-entered waypoint pins -----------------------------------

const pins = {}; // id -> L.Marker

function addPin(id, lat, lon, label) {
  if (pins[id]) {
    map.removeLayer(pins[id]);
  }
  const marker = L.marker([lat, lon]).addTo(map);
  if (label) {
    marker.bindTooltip(label, {
      permanent: true,
      direction: 'top',
      className: 'pin-label',
      offset: [0, -8],
    });
  }
  pins[id] = marker;
}

function removePin(id) {
  if (pins[id]) {
    map.removeLayer(pins[id]);
    delete pins[id];
  }
}

function clearPins() {
  Object.keys(pins).forEach(removePin);
}

// -- Zoom control from Python (e.g. GUI zoom in/out buttons) ----------

function setZoom(zoomLevel) {
  map.setZoom(zoomLevel);
}

function zoomIn() {
  map.zoomIn();
}

function zoomOut() {
  map.zoomOut();
}
