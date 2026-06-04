"use client";

import { useEffect, useState } from "react";
import {
  getPOSSummary,
  getMetrics,
  getFunnel,
  getVisualHeatmap,
  getAnomalies,
  getLiveAnalytics,
  getHealth,
  getCameras,
} from "@/lib/dashboard";
import React from 'react';

const BackgroundVideo = React.memo(({ streamUrl }: { streamUrl: string }) => {
  return (
    <video
      key={streamUrl}
      src={streamUrl}
      autoPlay
      loop
      muted
      playsInline
      className="absolute inset-0 w-full h-full object-cover opacity-70 pointer-events-none"
    />
  );
});

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [funnel, setFunnel] = useState<any>(null);
  const [heatmap, setHeatmap] = useState<any>(null);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [live, setLive] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [store, setStore] = useState("");
  const [storesList, setStoresList] = useState<any[]>([]);
  const [cameras, setCameras] = useState<any[]>([]);

  const fetchStores = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/stores');
      const data = await res.json();
      const storesArray = Array.isArray(data) ? data : (data.stores || []);
      setStoresList(storesArray);
      if (storesArray.length > 0 && !store) {
        setStore(storesArray[0].store_id);
      }
    } catch(e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchStores();
  }, []);

  useEffect(() => {
    if (!store) return;

    let isMounted = true;
    
    // Clear state before loading
    setSummary(null);
    setMetrics(null);
    setFunnel(null);
    setHeatmap(null);
    setAnomalies([]);
    setLive(null);
    setHealth(null);
    setCameras([]);

    const loadDashboardData = async () => {
      try {
        const [
          summaryData,
          metricsData,
          funnelData,
          heatmapData,
          anomalyData,
          liveData,
          healthData,
          videosRes,
        ] = await Promise.all([
          getPOSSummary(store),
          getMetrics(store),
          getFunnel(store),
          getVisualHeatmap(store),
          getAnomalies(store),
          getLiveAnalytics(store),
          getHealth(store),
          getCameras(store),
        ]);

        if (isMounted) {
          setSummary(summaryData);
          setMetrics(metricsData);
          setFunnel(funnelData);
          setHeatmap(heatmapData);
          setAnomalies(anomalyData.anomalies || []);
          setLive(liveData);
          setHealth(healthData);
          setCameras(videosRes || []);
        }
      } catch (error) {
        console.error("Dashboard load error:", error);
      }
    };

    loadDashboardData(); // Initial load for all data

    // Establish WebSocket for live data, metrics, anomalies
    const ws = new WebSocket(`ws://127.0.0.1:8000/websocket/live/${store}`);

    ws.onmessage = (event) => {
      if (!isMounted) return;
      try {
        const data = JSON.parse(event.data);
        if (data.live) setLive(data.live);
        if (data.metrics) setMetrics(data.metrics);
        if (data.live?.alerts) setAnomalies(data.live.alerts);
      } catch (e) {
        console.error("WebSocket payload error:", e);
      }
    };

    ws.onerror = (e) => console.error("WebSocket error:", e);

    // Keep POS summary, funnel, heatmap, health on a slower interval or just fetch once
    const interval = setInterval(async () => {
      if (!isMounted) return;
      const [summaryData, funnelData, heatmapData, healthData] = await Promise.all([
        getPOSSummary(store),
        getFunnel(store),
        getVisualHeatmap(store),
        getHealth(store)
      ]);
      if (isMounted) {
        setSummary(summaryData);
        setFunnel(funnelData);
        setHeatmap(heatmapData);
        setHealth(healthData);
      }
    }, 10000);

    return () => {
      isMounted = false;
      ws.close();
      clearInterval(interval);
    };
  }, [store]);

  useEffect(() => {
    // Mouse follower for background glow
    const handleMouseMove = (e: MouseEvent) => {
      document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
      document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
    };
    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Safe access wrappers
  const healthScore = health?.health_score ?? 0;
  const healthStatus = health?.status || "Unknown";
  const activeVisitors = live?.active_visitors || 0;
  const queueSize = live?.queue_size || 0;
  const avgDwell = ((metrics?.avg_dwell_time || 0) / 60000).toFixed(1);
  const convRate = metrics?.conversion_rate?.toFixed(1) || "0.0";
  const hourlyRev = summary?.revenue ? (summary.revenue / 1000).toFixed(1) : "0.0";

  const entryCount = funnel?.entry || 0;
  const browsingCount = funnel?.zone_visit || 0;
  const engagedCount = funnel?.dwell || 0;
  const purchaseCount = funnel?.purchase || 0;

  const getPercent = (value: number, total: number) => {
    if (!total) return 0;
    return Math.round((value / total) * 100);
  };

  return (
    <div className="font-body-md text-body-md selection:bg-primary/20 bg-background min-h-screen text-on-surface">
      <div id="cursor-glow"></div>
      
      {/* SideNavBar */}
      <aside className="hidden lg:flex fixed left-0 top-0 h-full z-40 flex-col w-64 border-r border-outline bg-white shadow-sm">
        <div className="p-6">
          <h1 className="font-display-lg font-bold text-primary mb-1 tracking-tight" style={{fontSize: '24px', lineHeight: '32px'}}>Store-Intelligence</h1>
          <p className="font-label-mono text-[10px] text-on-surface-variant/60 uppercase tracking-widest">Enterprise AI Solution</p>
        </div>
        <nav className="flex-1 px-4 py-6 space-y-1">
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-primary font-bold bg-primary/5 transition-all active:scale-95 duration-150" href="#">
            <span className="material-symbols-outlined">dashboard</span>
            <span>Dashboard</span>
          </a>
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#funnel">
            <span className="material-symbols-outlined text-slate-400">filter_alt</span>
            <span>Funnel</span>
          </a>
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#heatmap">
            <span className="material-symbols-outlined text-slate-400">wb_sunny</span>
            <span>Heatmap</span>
          </a>
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#cctv">
            <span className="material-symbols-outlined text-slate-400">videocam</span>
            <span>CCTV</span>
          </a>
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#ai-insights">
            <span className="material-symbols-outlined text-slate-400">error</span>
            <span>Anomalies</span>
          </a>
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#">
            <span className="material-symbols-outlined text-slate-400">description</span>
            <span>Reports</span>
          </a>
        </nav>
        <div className="px-4 py-6 border-t border-outline space-y-1">
          <a className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all active:scale-95 duration-150" href="#">
            <span className="material-symbols-outlined text-slate-400">settings</span>
            <span>Settings</span>
          </a>
          <div className="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant font-medium hover:bg-slate-50 transition-all cursor-pointer">
            <img alt="Profile" className="w-8 h-8 rounded-full border border-outline" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAC0YhJBeVSINX8b0PjfIl2k7iNvShWmY5_QVPsYCY9teZWPIZyvcCkAO6RsAf_u3oN9c2rH2uuSiahQBVBKJ9uakviurdRliLc_GGmQmDJitDpQnjpCC4UWviGnc0LBfoqE-INa7BavjrEO9DjROAbm361q4FyE_Jnxhed-a72XYyuK2IG3Gox3yRKy-Mu2fKhea4N7zMJtStIxt6ZkiMOyM8lzeD6ZsIJ0nm9HOao9KWS1d7WV4VzqCud0a1T3IKU1DfzOUU7gEkk"/>
            <span>Profile</span>
          </div>
        </div>
      </aside>

      {/* TopNavBar */}
      <header className="fixed top-0 right-0 w-full lg:w-[calc(100%-16rem)] z-50 flex items-center justify-between px-4 lg:px-10 h-16 border-b border-outline bg-white/80 backdrop-blur-md shadow-sm">
        <div className="flex items-center flex-1 pr-4">
          <div className="relative w-full max-w-xs md:max-w-md group">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors">search</span>
            <input className="w-full bg-slate-50 border border-slate-200 rounded-full py-1.5 pl-10 pr-4 text-body-md focus:outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 transition-all text-ellipsis" placeholder="Search analytics, cameras, or reports..." type="text"/>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-4 text-on-surface-variant">
            <button className="material-symbols-outlined hover:text-primary transition-all">notifications</button>
            <button className="material-symbols-outlined hover:text-primary transition-all">settings</button>
            <button className="material-symbols-outlined hover:text-primary transition-all">sensors</button>
          </div>
          <div className="h-6 w-px bg-slate-200"></div>
          <div className="flex items-center gap-3">
            <select
              value={store}
              onChange={(e) => setStore(e.target.value)}
              className="bg-transparent text-label-mono text-on-surface-variant/80 font-bold focus:outline-none appearance-none cursor-pointer hover:text-primary transition-colors pr-2"
            >
              {storesList.length === 0 && (
                <option value="">No stores found/Loading...</option>
              )}
              {storesList.map((s) => (
                <option key={s.store_id} value={s.store_id}>{s.store_name}</option>
              ))}
            </select>
            <div className="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse-subtle shadow-[0_0_8px_rgba(0,180,125,0.4)]"></div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="ml-0 lg:ml-64 pt-20 lg:pt-24 px-4 sm:px-6 lg:px-10 pb-10 min-h-screen relative z-10">
        
        {/* KPI Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
          {/* Store Health Hero */}
          <div className="col-span-1 lg:col-span-4 glass-card p-6 rounded-xl flex items-center gap-6 relative overflow-hidden group">
            <div className="absolute inset-0 glow-secondary -z-10 opacity-30"></div>
            <div className="relative w-32 h-32 shrink-0">
              <svg className="w-full h-full" viewBox="0 0 100 100">
                <circle className="text-slate-100 stroke-current" cx="50" cy="50" fill="transparent" r="42" strokeWidth="8"></circle>
                <circle className={`stroke-current progress-ring__circle ${healthScore < 70 ? 'text-amber-500' : 'text-secondary'}`} cx="50" cy="50" fill="transparent" id="health-progress" r="42" strokeLinecap="round" strokeWidth="8" style={{strokeDashoffset: 264 - (healthScore / 100 * 264)}}></circle>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-headline-md text-[24px] font-bold text-on-surface">{healthScore}</span>
                <span className="text-label-mono text-[10px] text-on-surface-variant/50 uppercase tracking-widest">/100</span>
              </div>
            </div>
            <div>
              <h3 className={`text-label-mono font-bold mb-1 ${healthScore < 70 ? 'text-amber-600' : 'text-secondary'}`}>HEALTH SCORE</h3>
              <p className={`font-headline-md font-bold mb-2 uppercase ${healthStatus.length > 8 ? 'text-[18px]' : 'text-[24px]'} ${healthScore < 70 ? 'text-amber-600' : 'text-on-surface'}`}>
                {healthStatus.replace(/_/g, ' ')}
              </p>
              <p className="text-sm text-on-surface-variant leading-tight">
                {healthScore >= 90 ? "System integrity at peak performance." :
                  healthScore >= 70 ? "Minor issues detected. Operating normally." :
                  "Attention required. System degraded."}
              </p>
            </div>
          </div>
          
          {/* Metric Cards */}
          <div className="col-span-1 lg:col-span-8 grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-4 lg:gap-6">
            <div className="glass-card p-4 rounded-xl flex flex-col justify-between">
              <div className="flex justify-between items-start mb-2">
                <span className="material-symbols-outlined text-primary">groups</span>
              </div>
              <div>
                <p className="text-label-mono text-on-surface-variant/60 text-[11px] mb-1 uppercase tracking-wider">Active Visitors</p>
                <p className="font-headline-md text-[24px] text-on-surface font-bold">{activeVisitors}</p>
              </div>
            </div>

            <div className="glass-card p-4 rounded-xl flex flex-col justify-between">
              <div className="flex justify-between items-start mb-2">
                <span className="material-symbols-outlined text-tertiary">hourglass_empty</span>
              </div>
              <div>
                <p className="text-label-mono text-on-surface-variant/60 text-[11px] mb-1 uppercase tracking-wider">Queue Size</p>
                <p className="font-headline-md text-[24px] text-on-surface font-bold">{queueSize}</p>
              </div>
            </div>

            <div className="glass-card p-4 rounded-xl flex flex-col justify-between">
              <div className="flex justify-between items-start mb-2">
                <span className="material-symbols-outlined text-primary">schedule</span>
              </div>
              <div>
                <p className="text-label-mono text-on-surface-variant/60 text-[11px] mb-1 uppercase tracking-wider">Avg Dwell</p>
                <p className="font-headline-md text-[24px] text-on-surface font-bold">{avgDwell}<span className="text-sm font-normal">m</span></p>
              </div>
            </div>

            <div className="glass-card p-4 rounded-xl flex flex-col justify-between">
              <div className="flex justify-between items-start mb-2">
                <span className="material-symbols-outlined text-secondary">shopping_cart</span>
              </div>
              <div>
                <p className="text-label-mono text-on-surface-variant/60 text-[11px] mb-1 uppercase tracking-wider">Conv Rate</p>
                <p className="font-headline-md text-[24px] text-on-surface font-bold">{convRate}<span className="text-sm font-normal">%</span></p>
              </div>
            </div>

            <div className="glass-card p-4 rounded-xl flex flex-col justify-between overflow-hidden relative">
              <div className="flex justify-between items-start mb-2">
                <span className="material-symbols-outlined text-primary">payments</span>
              </div>
              <div>
                <p className="text-label-mono text-on-surface-variant/60 text-[11px] mb-1 uppercase tracking-wider">Hourly Rev</p>
                <p className="font-headline-md text-[24px] text-on-surface font-bold"><span className="text-sm font-normal">₹</span>{hourlyRev}<span className="text-sm font-normal">k</span></p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-6">
          {/* Funnel Analytics */}
          <div className="col-span-1 xl:col-span-7 glass-card p-6 lg:p-8 rounded-xl" id="funnel">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8 sm:mb-10">
              <h2 className="font-headline-md text-[24px] font-bold text-on-surface leading-tight">Customer Funnel Analytics</h2>
              <div className="flex flex-wrap gap-2">
                <button className="px-3 py-1 bg-slate-100 rounded-full text-label-mono text-xs border border-slate-200 text-on-surface-variant">TODAY</button>
                <button className="px-3 py-1 bg-primary/10 text-primary rounded-full text-label-mono text-xs border border-primary/20 flex items-center gap-2 font-bold shrink-0">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                  LIVE
                </button>
              </div>
            </div>
            <div className="space-y-6 relative">
              <div className="flex items-center gap-6">
                <div className="w-full h-12 min-w-[130px] bg-slate-50 rounded-lg relative overflow-hidden border border-slate-100">
                  <div className="absolute inset-0 bg-primary/10 w-full transition-transform duration-1000 origin-left"></div>
                  <div className="relative z-10 h-full flex items-center px-4 justify-between">
                    <span className="font-label-mono text-xs text-on-surface-variant font-bold">ENTRY</span>
                    <span className="font-bold text-on-surface">{entryCount}</span>
                  </div>
                </div>
                <div className="w-24 text-center">
                  <span className="text-label-mono text-xs text-on-surface-variant font-bold">100%</span>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="h-12 min-w-[130px] bg-slate-50 rounded-lg relative overflow-hidden border border-slate-100" style={{width: `${Math.max(20, getPercent(browsingCount, entryCount) || 78)}%`}}>
                  <div className="absolute inset-0 bg-primary/10 w-full transition-transform duration-1000 origin-left"></div>
                  <div className="relative z-10 h-full flex items-center px-4 justify-between">
                    <span className="font-label-mono text-xs text-on-surface-variant font-bold">BROWSING</span>
                    <span className="font-bold text-on-surface">{browsingCount}</span>
                  </div>
                </div>
                <div className="w-24 text-center">
                  <span className="text-label-mono text-xs text-on-surface-variant font-bold">{getPercent(browsingCount, entryCount)}%</span>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="h-12 min-w-[130px] bg-slate-50 rounded-lg relative overflow-hidden border border-slate-100" style={{width: `${Math.max(20, getPercent(engagedCount, entryCount) || 52)}%`}}>
                  <div className="absolute inset-0 bg-primary/10 w-full transition-transform duration-1000 origin-left"></div>
                  <div className="relative z-10 h-full flex items-center px-4 justify-between">
                    <span className="font-label-mono text-xs text-on-surface-variant font-bold">ENGAGED</span>
                    <span className="font-bold text-on-surface">{engagedCount}</span>
                  </div>
                </div>
                <div className="w-24 text-center">
                  <span className="text-label-mono text-xs text-on-surface-variant font-bold">{getPercent(engagedCount, entryCount)}%</span>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="h-12 min-w-[130px] bg-secondary/5 rounded-lg relative overflow-hidden border border-secondary/10" style={{width: `${Math.max(20, getPercent(purchaseCount, entryCount) || 34)}%`}}>
                  <div className="absolute inset-0 bg-secondary/10 w-full transition-transform duration-1000 origin-left"></div>
                  <div className="relative z-10 h-full flex items-center px-4 justify-between">
                    <span className="font-label-mono text-xs text-secondary font-bold">PURCHASE</span>
                    <span className="font-bold text-on-surface">{purchaseCount}</span>
                  </div>
                </div>
                <div className="w-24 text-center">
                  <span className="text-label-mono text-xs text-on-surface-variant font-bold">{getPercent(purchaseCount, entryCount)}%</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* AI Insights */}
          <div className="col-span-1 xl:col-span-5 flex flex-col gap-6" id="ai-insights">
            <div className="flex justify-between items-center px-2">
              <h2 className="font-headline-md text-[24px] font-bold text-on-surface flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary" style={{fontVariationSettings: '"FILL" 1'}}>auto_awesome</span>
                AI Detections
              </h2>
              <span className="text-label-mono text-xs text-on-surface-variant/60 flex items-center gap-2 font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                REAL-TIME
              </span>
            </div>
            
            {anomalies && anomalies.slice(0, 3).map((anomaly, idx) => (
              <div key={idx} className="glass-card p-5 rounded-xl flex gap-4 border-l-4 border-l-primary hover:border-primary transition-all cursor-pointer group">
                <div className="w-12 h-12 rounded-lg bg-primary/5 flex items-center justify-center text-primary shrink-0 group-hover:scale-110 transition-transform">
                  <span className="material-symbols-outlined">group_work</span>
                </div>
                <div className="flex-1">
                  <div className="flex justify-between mb-1">
                    <span className="text-label-mono text-[11px] text-primary font-bold uppercase">{anomaly.type}</span>
                    <span className="text-label-mono text-[10px] text-on-surface-variant/40">NOW</span>
                  </div>
                  <h4 className="font-bold mb-1 text-on-surface">{anomaly.severity} Insight</h4>
                  <p className="text-xs text-on-surface-variant leading-relaxed">{anomaly.suggested_action}</p>
                </div>
              </div>
            ))}
            {(!anomalies || anomalies.length === 0) && (
              <div className="glass-card p-5 rounded-xl flex gap-4 border-l-4 border-l-primary transition-all group">
                <div className="flex-1">
                  <p className="text-xs text-on-surface-variant leading-relaxed">No anomalies detected.</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          {/* Heatmap View */}
          <div className="col-span-1 xl:col-span-8 glass-card p-6 lg:p-8 rounded-xl overflow-hidden flex flex-col" id="heatmap">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 className="font-headline-md text-[24px] font-bold text-on-surface">Floorplan Heatmap</h2>
              <div className="flex flex-wrap items-center gap-3 sm:gap-6">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 shrink-0 rounded-full bg-red-500 animate-pulse"></div>
                  <span className="text-label-mono text-[10px] text-on-surface-variant/60 font-bold">HIGH</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 shrink-0 rounded-full bg-amber-400"></div>
                  <span className="text-label-mono text-[10px] text-on-surface-variant/60 font-bold">MED</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 shrink-0 rounded-full bg-blue-400"></div>
                  <span className="text-label-mono text-[10px] text-on-surface-variant/60 font-bold">LOW</span>
                </div>
              </div>
            </div>
            <div className="flex-1 relative rounded-lg bg-white overflow-hidden border border-slate-200 min-h-[400px] shadow-inner flex items-center justify-center">
              {heatmap?.image_url ? (
                <img alt="Store Heatmap" className="w-full h-full object-contain" src={`http://127.0.0.1:8000${heatmap.image_url}?t=${new Date().getTime()}`} />
              ) : (
                <span className="text-on-surface-variant font-medium">Processing CV Pipeline Heatmap...</span>
              )}
              
              {heatmap?.image_url && (
                <div className="absolute top-4 right-4 px-3 py-1.5 bg-green-500/90 backdrop-blur-md rounded-full shadow-sm z-20 flex items-center gap-2 border border-green-400">
                  <span className="material-symbols-outlined text-white text-[14px]">verified_user</span>
                  <span className="text-label-mono text-[10px] font-bold text-white tracking-wider">95% CONFIDENCE</span>
                </div>
              )}
            </div>
          </div>

          {/* Live CCTV & Alerts */}
          <div className="col-span-1 xl:col-span-4 flex flex-col gap-6" id="cctv">
            <div className="glass-card p-4 rounded-xl">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-label-mono text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Live Streams</h3>
                <div className="flex gap-1.5 items-center bg-red-50 px-2 py-0.5 rounded text-red-600">
                  <div className="w-1.5 h-1.5 rounded-full bg-red-600 animate-pulse"></div>
                  <span className="text-[10px] font-bold uppercase">REC</span>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {cameras.map((cam: any) => {
                  const streamUrl = cam.stream_url || "";
                  
                  // Match up live stats from websocket
                  const liveStats = (live?.camera_status || []).find((c: any) => c.camera_id === cam.camera_id) || {
                     active_visitors: 0,
                     queue_size: 0
                  };
                  
                  return (
                  <div key={`${cam.store_id}_${cam.camera_id}`} className="aspect-video relative bg-slate-900 rounded-lg overflow-hidden group border border-slate-200">
                    <BackgroundVideo streamUrl={streamUrl} />
                    <div className="absolute top-2 left-2 right-2 flex justify-between items-center z-10">
                      <div className="flex gap-1.5 items-center">
                        <div className="px-1.5 py-0.5 bg-black/60 backdrop-blur-md rounded text-[9px] font-mono text-white">
                          {cam.camera_name || cam.camera_id}
                        </div>
                        {cam.camera_type && (
                          <div className="px-1.5 py-0.5 bg-indigo-500/90 backdrop-blur-md rounded text-[9px] font-bold text-white">
                            [{cam.camera_type}]
                          </div>
                        )}
                      </div>
                      <div className="w-2 h-2 rounded-full bg-secondary animate-pulse shadow-[0_0_8px_rgba(0,180,125,0.8)]"></div>
                    </div>
                    <div className="absolute bottom-2 left-2 right-2 z-10 grid grid-cols-2 gap-2">
                        <div className="bg-black/40 p-1.5 rounded text-white backdrop-blur-sm flex flex-col justify-center">
                          <p className="text-[8px] text-white/70 uppercase leading-none mb-1">Visitors</p>
                          <p className="text-xs font-bold leading-none">{liveStats.active_visitors}</p>
                        </div>
                        <div className="bg-black/40 p-1.5 rounded text-white backdrop-blur-sm flex flex-col justify-center">
                          <p className="text-[8px] text-white/70 uppercase leading-none mb-1">Queue</p>
                          <p className="text-xs font-bold leading-none">{liveStats.queue_size}</p>
                        </div>
                    </div>
                  </div>
                  )
                })}
              </div>
            </div>
            
            <div className="glass-card flex-1 p-5 rounded-xl flex flex-col h-full overflow-hidden">
              <h3 className="text-label-mono text-[10px] font-bold uppercase tracking-widest mb-4 text-on-surface-variant">Security Feed</h3>
              <div className="space-y-4 overflow-y-auto pr-2">
                
                {anomalies && anomalies.slice(0, 5).map((anomaly, idx) => (
                  <div key={idx} className="flex gap-3 items-start border-l-4 border-error/50 bg-red-50/50 p-2 rounded-r-lg">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-label-mono text-[10px] text-error font-bold px-1.5 py-0.5 bg-white rounded border border-error/20">ALERT</span>
                        <span className="text-[10px] text-on-surface-variant/60 font-bold">LIVE</span>
                      </div>
                      <p className="text-[11px] leading-tight text-on-surface font-medium">
                        {anomaly.type ? anomaly.type.replace(/_/g, ' ') : 'ALERT'}
                        {anomaly.zone ? ` in ${anomaly.zone}` : ''}
                      </p>
                      {anomaly.suggested_action && (
                        <p className="text-[9px] text-on-surface-variant mt-0.5">{anomaly.suggested_action}</p>
                      )}
                    </div>
                  </div>
                ))}

                {(!anomalies || anomalies.length === 0) && (
                  <div className="flex gap-3 items-start border-l-4 border-green-500/50 bg-green-50/50 p-2 rounded-r-lg">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-label-mono text-[10px] text-green-700 font-bold px-1.5 py-0.5 bg-white rounded border border-green-500/20">SECURE</span>
                      </div>
                      <p className="text-[11px] leading-tight text-on-surface font-medium">All zones clear. No anomalies.</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}