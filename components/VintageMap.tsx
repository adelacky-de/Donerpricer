import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { HistoryRecord } from '../types';

interface Props {
  data: HistoryRecord[];
  loading: boolean;
}

const VintageMap: React.FC<Props> = ({ data, loading }) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersRef = useRef<L.Marker[]>([]);

  // Initialize Map
  useEffect(() => {
    if (mapContainerRef.current && !mapInstanceRef.current) {
      const berlinCenter: [number, number] = [52.5200, 13.4050];
      
      const map = L.map(mapContainerRef.current, {
        center: berlinCenter,
        zoom: 11,
        zoomControl: false,
        attributionControl: false
      });

      // Use Standard OSM tiles but apply CSS filter in index.html for B&W look
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        className: 'vintage-map-tiles'
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update Markers
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    // Clear existing markers
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    if (loading || data.length === 0) return;

    // Create a custom div icon for a "printed" look
    const createVintageIcon = (price: number) => {
      return L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="
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
          box-shadow: 2px 2px 0px rgba(0,0,0,0.3);
        ">€</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
    };

    const bounds = L.latLngBounds([]);

    data.forEach(record => {
      if (record.lat && record.lng) {
        const marker = L.marker([record.lat, record.lng], {
          icon: createVintageIcon(record.price)
        })
        .bindPopup(`
          <div style="font-family: 'Lora', serif; text-align: center;">
            <strong style="text-transform: uppercase; font-size: 11px;">${record.supermarket}</strong><br/>
            <span style="font-family: 'Courier Prime';">€${record.price.toFixed(2)}</span><br/>
            <span style="font-size: 10px; color: #666;">${record.date}</span>
          </div>
        `)
        .addTo(map);

        markersRef.current.push(marker);
        bounds.extend([record.lat, record.lng]);
      }
    });

    if (markersRef.current.length > 0) {
      map.fitBounds(bounds, { padding: [30, 30] });
    }

  }, [data, loading]);

  return (
    <div className="border-2 border-ink bg-white p-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] relative">
      <div className="border border-ink h-[250px] relative overflow-hidden vintage-map-filter">
         <div ref={mapContainerRef} className="w-full h-full bg-slate-100 z-0" />
         
         {loading && (
             <div className="absolute inset-0 z-10 bg-white/50 flex items-center justify-center backdrop-blur-sm">
                 <span className="font-mono text-xs uppercase text-ink bg-white px-2 py-1 border border-ink">Locating Vendors...</span>
             </div>
         )}

         {/* Vintage Map Label */}
         <div className="absolute top-2 right-2 z-[400] bg-white border border-ink px-2 py-1">
            <span className="font-serif text-xs font-bold uppercase tracking-widest">Zone Map</span>
         </div>
      </div>
    </div>
  );
};

export default VintageMap;