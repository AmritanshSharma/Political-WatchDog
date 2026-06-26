import React from 'react';

export default function Disclaimer() {
  return (
    <div className="bg-slate-900 text-slate-400 p-4 text-xs font-medium border-t border-slate-800 text-center w-full">
      <p className="max-w-4xl mx-auto">
        <strong>DISCLAIMER:</strong> The data presented on this dashboard is derived entirely from public government declarations, election affidavits, and official portals. We do not endorse any political figures nor make subjective claims regarding their performance. Metrics are calculated using standardized formulas and are for informational purposes only.
      </p>
    </div>
  );
}
