"use client";

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Disclaimer from '@/components/Disclaimer';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';
import { TrendingUp, AlertCircle, Briefcase, MapPin } from 'lucide-react';

export default function OfficialProfile() {
  const params = useParams();
  const { id } = params;
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Dummy fetch for prototyping
    fetch(`http://localhost:8000/api/politicians/${id}`)
      .then(res => {
        if (!res.ok) throw new Error("API response not ok");
        return res.json();
      })
      .then(data => {
        setProfile(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        // Fallback dummy data for visualization
        setProfile({
          name: id.toString().replace(/_/g, ' ').toUpperCase(),
          state: "Demo State",
          party: "Demo Party",
          anomaly_score: 12.5,
          unspent_funds_percentage: 23.4,
          financials: [
            { year: 2014, declared_assets: 5000000, declared_income: 1200000 },
            { year: 2019, declared_assets: 15000000, declared_income: 1800000 },
            { year: 2024, declared_assets: 85000000, declared_income: 2500000 },
          ],
          tenders: [
            { project_name: "Road Dev", sanctioned_amount: 100000, spent_amount: 80000 },
            { project_name: "Water Supply", sanctioned_amount: 50000, spent_amount: 20000 },
          ]
        });
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-slate-300">Loading profile data...</div>;
  if (!profile) return <div className="min-h-screen flex items-center justify-center text-red-400">Profile not found.</div>;

  return (
    <div className="min-h-screen flex flex-col bg-[#0f172a]">
      <main className="flex-grow w-full max-w-7xl mx-auto p-4 md:p-8">
        <header className="mb-8">
          <div className="flex items-center space-x-4 mb-2">
            <h1 className="text-4xl font-bold tracking-tight text-white">{profile.name}</h1>
          </div>
          <div className="flex items-center space-x-6 text-slate-400">
            <span className="flex items-center"><MapPin className="h-4 w-4 mr-1"/> {profile.state}</span>
            <span className="flex items-center"><Briefcase className="h-4 w-4 mr-1"/> {profile.party}</span>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Risk Card */}
          <div className="glassmorphism p-6 rounded-xl border-l-4 border-l-blue-500">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-slate-300 font-medium">Financial Growth Anomaly Score</h3>
              <TrendingUp className="text-blue-500 h-5 w-5" />
            </div>
            <div className="text-4xl font-bold text-white mb-2">
              {profile.anomaly_score.toFixed(1)}<span className="text-lg text-slate-500">/100</span>
            </div>
            <p className="text-xs text-slate-400">Based on historical asset vs income growth ratio.</p>
          </div>

          {/* Unspent Funds Card */}
          <div className="glassmorphism p-6 rounded-xl border-l-4 border-l-emerald-500">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-slate-300 font-medium">Unspent Public Funds</h3>
              <AlertCircle className="text-emerald-500 h-5 w-5" />
            </div>
            <div className="text-4xl font-bold text-white mb-2">
              {profile.unspent_funds_percentage.toFixed(1)}%
            </div>
            <p className="text-xs text-slate-400">Percentage of sanctioned scheme funds unutilized.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Financial Growth Chart */}
          <div className="glassmorphism p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-6 text-slate-200">Asset Velocity vs Declared Income</h3>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={profile.financials} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorAssets" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                  <XAxis dataKey="year" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" tickFormatter={(value) => `₹${(value/10000000).toFixed(1)}Cr`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                    itemStyle={{ color: '#e2e8f0' }}
                  />
                  <Legend />
                  <Area type="monotone" dataKey="declared_assets" name="Declared Assets" stroke="#3b82f6" fillOpacity={1} fill="url(#colorAssets)" />
                  <Area type="monotone" dataKey="declared_income" name="Declared Income" stroke="#10b981" fillOpacity={0} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Scheme Utilization Chart */}
          <div className="glassmorphism p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-6 text-slate-200">Public Scheme Utilization</h3>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={profile.tenders} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                  <XAxis dataKey="project_name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  />
                  <Legend />
                  <Bar dataKey="sanctioned_amount" name="Sanctioned" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="spent_amount" name="Spent" fill="#10b981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main>
      <Disclaimer />
    </div>
  );
}
