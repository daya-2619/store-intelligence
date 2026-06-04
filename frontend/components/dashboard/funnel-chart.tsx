"use client";

import { useEffect, useState } from "react";
import { Filter } from "lucide-react";

export function FunnelChart({ funnel }: { funnel: any }) {
  const entries = funnel?.entries || 0;
  const zones = funnel?.zone_interactions || 0;
  const queues = funnel?.queue_entries || 0;
  const purchases = funnel?.purchases || 0;

  const funnelData = [
    { stage: "Store Entries", count: entries, percentage: 100, color: "bg-blue-600" },
    { stage: "Zone Interactions", count: zones, percentage: entries ? ((zones/entries)*100).toFixed(1) : 0, color: "bg-indigo-600" },
    { stage: "Queue Entries", count: queues, percentage: entries ? ((queues/entries)*100).toFixed(1) : 0, color: "bg-purple-600" },
    { stage: "Purchases", count: purchases, percentage: entries ? ((purchases/entries)*100).toFixed(1) : 0, color: "bg-rose-600" },
  ];

  return (
    <div className="glass-panel p-6 hover-magnet h-full flex flex-col">
      <h2 className="text-xl font-bold flex items-center gap-2 mb-8 text-neutral-800">
        <Filter className="w-5 h-5 text-purple-500" /> Conversion Funnel
      </h2>
      
      <div className="flex-1 flex flex-col justify-center space-y-4 relative">
        {funnelData.map((step, index) => {
          const width = `${Math.max(step.percentage, 10)}%`;
          return (
            <div key={index} className="relative group">
              {/* Drop-off line to next step */}
              {index < funnelData.length - 1 && (
                <div className="absolute left-1/2 -bottom-4 w-px h-4 bg-neutral-300 -translate-x-1/2 z-0" />
              )}
              
              <div 
                className={`h-16 rounded-xl ${step.color} relative z-10 flex items-center justify-between px-6 transition-all duration-500 hover:scale-[1.02] mx-auto shadow-md border border-black/10`}
                style={{ width, minWidth: '200px' }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl" />
                <span className="font-semibold text-white relative z-20 whitespace-nowrap drop-shadow-md">
                  {step.stage}
                </span>
                <div className="text-right relative z-20">
                  <div className="font-bold text-white text-lg drop-shadow-md">{step.count}</div>
                  <div className="text-white/80 text-xs font-medium">{step.percentage}%</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
