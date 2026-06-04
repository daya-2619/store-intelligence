"use client";

import { useEffect, useState } from "react";
import { Map, Zap } from "lucide-react";

export function VisualHeatmap({ heatmap }: { heatmap: any }) {

  return (
    <div className="glass-panel p-6 hover-magnet relative overflow-hidden group min-h-[400px] flex flex-col">
      <div className="flex justify-between items-center z-20 relative mb-4">
        <h2 className="text-xl font-bold flex items-center gap-2 text-neutral-800">
          <Map className="w-5 h-5 text-indigo-500" /> Spatial Heatmap
        </h2>
        <div className="flex items-center gap-2">
           <span className="flex items-center gap-1 text-xs px-2 py-1 bg-indigo-100 text-indigo-600 rounded-full font-medium border border-indigo-200">
             <Zap className="w-3 h-3" />
             98% Confidence
           </span>
        </div>
      </div>
      
      <div className="relative flex-1 rounded-xl overflow-hidden bg-neutral-100 border border-neutral-200 flex items-center justify-center shadow-inner">
        {heatmap?.image ? (
          <img src={`data:image/png;base64,${heatmap.image}`} alt="Heatmap Overlay" className="w-full h-full object-cover opacity-90 mix-blend-multiply" />
        ) : (
          <>
            <div className="absolute inset-0 opacity-10 bg-[url('https://images.unsplash.com/photo-1555529771-835f59bfc50c?q=80&w=1200&auto=format&fit=crop')] bg-cover bg-center mix-blend-luminosity" />
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-purple-500/10 to-rose-500/10 opacity-50 blur-xl mix-blend-multiply" />
            
            <div className="relative z-10 flex flex-col items-center">
               <p className="text-sm font-medium text-neutral-500">Waiting for live spatial data...</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
