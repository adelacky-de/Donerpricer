from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import Qt # Import Qt for alignment
import json
import pandas as pd # Import pandas for DataFrame type hinting
import requests
from time import sleep

class VintageMap(QWidget):
    # Cache for geocoded locations to avoid repeated API calls
    _geocode_cache = {}
    
    @staticmethod
    def geocode_location(supermarket, location):
        """
        Geocode a location using Nominatim API (OpenStreetMap).
        Returns (latitude, longitude) tuple or None if geocoding fails.
        Caches results to avoid repeated API calls.
        """
        # Check cache first
        cache_key = (supermarket, location)
        if cache_key in VintageMap._geocode_cache:
            return VintageMap._geocode_cache[cache_key]
        
        # Construct search query: "Supermarket Location, Münster, Germany"
        query = f"{supermarket} {location}, Münster, Germany"
        
        try:
            # Use Nominatim API (free, no API key required)
            # User-Agent is required by Nominatim's usage policy
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': query,
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'Donerpricer/1.0 (Educational Project)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    result = (lat, lon)
                    
                    # Cache the result
                    VintageMap._geocode_cache[cache_key] = result
                    
                    # Be respectful to the API - wait 1 second between requests
                    sleep(1)
                    
                    return result
        except Exception as e:
            print(f"Geocoding error for {query}: {e}")
        
        # If geocoding fails, return Münster city center as fallback
        fallback = (51.9607, 7.6261)
        VintageMap._geocode_cache[cache_key] = fallback
        return fallback
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background: #fdfbf7;")
        
        # Leaflet HTML with monochrome filter
        self.map_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                body, html, #map { height: 100%; margin: 0; background: #fdfbf7; }
                .leaflet-tile-pane {
                    filter: grayscale(100%) contrast(1.2) brightness(1.05) sepia(0.2);
                }
                .custom-div-icon {
                    background-color: #1a1a1a;
                    color: #fdfbf7;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Courier Prime', monospace;
                    font-size: 10px;
                    font-weight: bold;
                    border: 1px solid #fff;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map', {
                    center: [51.9607, 7.6261], // Center of Münster
                    zoom: 12,
                    zoomControl: false,
                    attributionControl: false
                });
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19
                }).addTo(map);
                
                var markers = [];
                function updateMarkers(data) {
                    markers.forEach(m => m.remove());
                    markers = [];
                    if (!data || data.length === 0) return;
                    
                    var bounds = L.latLngBounds([]);
                    data.forEach(r => {
                        if (r.lat && r.lng) {
                            var icon = L.divIcon({
                                className: 'custom-div-icon',
                                html: '€',
                                iconSize: [24, 24],
                                iconAnchor: [12, 12]
                            });
                            var marker = L.marker([r.lat, r.lng], {icon: icon}).addTo(map);
                            marker.bindPopup("<b>" + r.supermarket + "</b><br>" + r.location + "<br>Price: €" + r.price.toFixed(2));
                            markers.push(marker);
                            bounds.extend([r.lat, r.lng]);
                        }
                    });
                    if (markers.length > 0) {
                        map.fitBounds(bounds, {padding: [30, 30]});
                    }
                }
            </script>
        </body>
        </html>
        """
        self.web_view.setHtml(self.map_html)
        layout.addWidget(self.web_view)
        self.setMinimumHeight(300)

    def update_map(self, df: pd.DataFrame):
        """Update map with markers from DataFrame using API-based geocoding."""
        print(f"VintageMap.update_map called with {len(df)} records")
        
        data = []
        for _, row in df.iterrows():
            # Use API-based geocoding for each location
            coords = self.geocode_location(row['supermarket'], row['location'])
            if coords:
                lat, lng = coords
                data.append({
                    'lat': lat,
                    'lng': lng,
                    'supermarket': row['supermarket'],
                    'location': row['location'],
                    'price': row['price']
                })
        
        print(f"Mapped {len(data)} markers")
        js_code = f"updateMarkers({json.dumps(data)});"
        self.web_view.page().runJavaScript(js_code)
