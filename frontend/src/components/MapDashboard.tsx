"use client";

import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';

const INDIA_TOPO_JSON = "https://raw.githubusercontent.com/udit-001/india-maps-data/main/topojson/india.json";

interface MapDashboardProps {
  politicians: any[];
}

export default function MapDashboard({ politicians }: MapDashboardProps) {
  const [selectedState, setSelectedState] = useState<string | null>(null);

  // Normalize state names to match Map Data or simple matching
  // MyNeta usually lists states, but we might need fuzzy matching
  const handleStateClick = (geo: any) => {
    // Deldersveld topojson properties usually have NAME_1, udit uses st_nm
    const stateName = geo.properties.st_nm;
    if (selectedState === stateName) {
        setSelectedState(null);
    } else {
        setSelectedState(stateName);
    }
  };

  const displayedPoliticians = selectedState 
    ? politicians.filter(p => p.state.toLowerCase() === selectedState.toLowerCase() || p.state === "India") // "India" fallback for now
    : politicians;

  return (
    <div className="flex flex-col lg:flex-row gap-8 mb-12">
      {/* Map Section */}
      <div className="w-full lg:w-1/2 glassmorphism rounded-xl p-4">
        <h2 className="text-xl font-semibold text-slate-200 mb-4 text-center">Electoral Map (State View)</h2>
        <div className="w-full" style={{ height: "450px" }}>
          <ComposableMap
            projection="geoMercator"
            projectionConfig={{
              scale: 800,
              center: [80, 22] // Center of India
            }}
            width={800}
            height={600}
            style={{ width: "100%", height: "100%" }}
          >
            <Geographies geography={INDIA_TOPO_JSON}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  const stateName = geo.properties.st_nm;
                  const isSelected = selectedState === stateName;
                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      onClick={() => handleStateClick(geo)}
                      style={{
                        default: {
                          fill: isSelected ? "#3b82f6" : "#334155",
                          outline: "none",
                          stroke: "#0f172a",
                          strokeWidth: 0.5
                        },
                        hover: {
                          fill: "#60a5fa",
                          outline: "none",
                          cursor: "pointer"
                        },
                        pressed: {
                          fill: "#2563eb",
                          outline: "none"
                        }
                      }}
                    />
                  );
                })
              }
            </Geographies>
          </ComposableMap>
        </div>
        {selectedState && (
          <p className="text-center text-blue-400 font-medium mt-2">
            Selected: {selectedState}
          </p>
        )}
      </div>

      {/* Projects/Leaders Section */}
      <div className="w-full lg:w-1/2 glassmorphism rounded-xl p-6 h-[500px] overflow-y-auto">
        <h2 className="text-xl font-semibold text-slate-200 mb-4">
          {selectedState ? `Projects in ${selectedState}` : "All Nationwide Projects"}
        </h2>
        {displayedPoliticians.length === 0 ? (
          <p className="text-slate-400">No leaders found for this region.</p>
        ) : (
          <div className="space-y-4">
            {displayedPoliticians.slice(0, 20).map(p => (
              <div key={p.id} className="bg-slate-800/50 p-4 rounded-lg border border-slate-700">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-medium text-white">{p.name}</h3>
                    <span className="text-xs text-blue-400 border border-blue-400/30 bg-blue-400/10 px-2 py-0.5 rounded-full">
                      {p.role || "MP"}
                    </span>
                    <span className="text-xs text-slate-400 ml-2">{p.party} | {p.constituency}</span>
                  </div>
                </div>
                <div className="mt-3">
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Projects Overview</h4>
                  <ul className="space-y-2">
                    {p.tenders && p.tenders.length > 0 ? p.tenders.map((t: any) => (
                      <li key={t.id} className="text-sm flex justify-between items-center bg-slate-900/50 p-2 rounded">
                        <span className="text-slate-300 truncate max-w-[60%]">{t.project_name}</span>
                        <span className={`text-xs px-2 py-1 rounded ${t.status === 'Completed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                          {t.status}
                        </span>
                      </li>
                    )) : (
                      <li className="text-sm text-slate-500 italic">No projects found.</li>
                    )}
                  </ul>
                </div>
              </div>
            ))}
            {displayedPoliticians.length > 20 && (
              <p className="text-center text-xs text-slate-500 mt-4">Showing 20 of {displayedPoliticians.length} leaders.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
