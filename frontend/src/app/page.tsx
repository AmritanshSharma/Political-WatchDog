"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Disclaimer from '@/components/Disclaimer';
import MapDashboard from '@/components/MapDashboard';
import { Search, MapPin, AlertTriangle } from 'lucide-react';

export default function Home() {
  const [politicians, setPoliticians] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    // Fetch from our Python backend (dummy fetch for now)
    fetch("http://localhost:8000/api/politicians")
      .then(res => res.json())
      .then(data => setPoliticians(data))
      .catch(err => console.error("Error fetching politicians", err));
  }, []);

  // Use the fetched data directly
  const displayData = politicians;

  const filteredData = displayData.filter((p: any) => p.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="min-h-screen flex flex-col items-center justify-between font-[family-name:var(--font-geist-sans)]">
      <main className="flex-grow w-full max-w-7xl mx-auto p-4 md:p-8">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4 tracking-tight">Public Official Transparency Dashboard</h1>
          <p className="text-slate-400 text-lg">Neutral, data-driven insights into public fund utilization and asset growth.</p>
        </header>

        <MapDashboard politicians={politicians} />

        <div className="mb-8 relative max-w-2xl mx-auto mt-12">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-slate-500" />
          </div>
          <input 
            type="text" 
            placeholder="Search by official name or constituency..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="block w-full pl-10 pr-3 py-3 border border-slate-700 rounded-lg leading-5 bg-slate-800 text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
          />
        </div>

        <h2 className="text-2xl font-bold text-slate-200 mb-6 text-center">All Leaders Directory</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredData.slice(0, 50).map((official: any) => (
            <Link href={`/official/${official.unique_id}`} key={official.id}>
              <div className="glassmorphism rounded-xl p-6 hover:scale-105 transition-transform duration-200 cursor-pointer h-full flex flex-col justify-between group">
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <h2 className="text-xl font-semibold group-hover:text-blue-400 transition-colors truncate max-w-[200px]">{official.name}</h2>
                    <div className="flex space-x-2">
                      <span className="text-xs bg-slate-800 border border-slate-700 px-2 py-1 rounded text-slate-300">{official.role || "MP"}</span>
                      {official.scrape_status === "Data Scraped" && (
                        <span className="text-xs bg-emerald-900/40 border border-emerald-700 px-2 py-1 rounded text-emerald-400">Scraped</span>
                      )}
                      {official.scrape_status === "In Progress" && (
                        <span className="text-xs bg-amber-900/40 border border-amber-700 px-2 py-1 rounded text-amber-400 animate-pulse">Scraping...</span>
                      )}
                      {official.scrape_status === "Not Scraped" && (
                        <span className="text-xs bg-red-900/40 border border-red-700 px-2 py-1 rounded text-red-400">Pending</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center text-slate-400 mb-1 text-sm">
                    <MapPin className="h-4 w-4 mr-1" />
                    <span>{official.state} | {official.constituency}</span>
                  </div>
                  <div className="text-slate-400 text-sm font-medium">
                    {official.party}
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-slate-700/50 flex justify-between items-center text-sm">
                  <span className="text-slate-300">View Profile</span>
                  <span className="text-blue-500 flex items-center">
                    Metrics &rarr;
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
        {filteredData.length > 50 && (
          <p className="text-center text-slate-500 mt-8">Showing 50 of {filteredData.length} records. Use the search to find specific officials.</p>
        )}
      </main>
      <Disclaimer />
    </div>
  );
}
