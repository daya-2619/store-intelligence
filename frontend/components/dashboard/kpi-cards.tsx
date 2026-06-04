"use client";

import { useEffect, useState } from "react";
import { Users, Clock, ShoppingCart, TrendingUp, Activity, BarChart2 } from "lucide-react";

export function KPICards({ live, metrics, health }: { live: any, metrics: any, health: any }) {

  const cards = [
    { title: "Active Visitors", value: live?.active_visitors ?? 0, icon: Users, color: "text-blue-600" },
    { title: "Queue Size", value: live?.queue_size ?? 0, icon: Clock, color: "text-orange-600" },
    { title: "Avg Dwell (sec)", value: ((metrics?.avg_dwell_time || 0) / 1000).toFixed(1), icon: Activity, color: "text-purple-600" },
    { title: "Conversion (%)", value: `${(live?.conversion_rate ?? 0).toFixed(2)}%`, icon: TrendingUp, color: "text-emerald-600" },
    { title: "Revenue (₹)", value: `₹${(live?.revenue ?? 0).toLocaleString()}`, icon: ShoppingCart, color: "text-blue-700" },
    { title: "Health Score", value: health ? `${health.health_score}/100` : "Loading...", icon: BarChart2, color: "text-indigo-600" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
      {cards.map((card, i) => (
        <div key={i} className="glass-panel p-6 flex flex-col items-center justify-center hover-magnet group cursor-pointer group-hover:-translate-y-1 transition-transform border border-neutral-200 shadow-sm bg-white/60">
          <card.icon className={`w-8 h-8 mb-3 ${card.color} group-hover:scale-110 transition-transform`} />
          <h3 className="text-sm font-medium text-neutral-500 mb-1">{card.title}</h3>
          <div className="text-2xl font-bold tracking-tight text-neutral-900">{card.value}</div>
        </div>
      ))}
    </div>
  );
}
