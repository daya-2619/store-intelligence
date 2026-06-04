"use client";

import { AlertTriangle, Info, BellRing } from "lucide-react";
import { useEffect, useState } from "react";

export function AlertsPanel({ anomalies }: { anomalies: any[] }) {
  const alerts = anomalies || [];

  return (
    <div className="glass-panel p-6 hover-magnet h-full flex flex-col">
      <h2 className="text-xl font-bold flex items-center gap-2 mb-6 text-neutral-800">
        <BellRing className="w-5 h-5 text-rose-500" /> Real-Time Alerts
      </h2>
      
      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {alerts.map((alert) => (
          <div 
            key={alert.id || alert.anomaly_id || Math.random()} 
            className={`p-4 rounded-xl border flex gap-4 transition-transform hover:scale-[1.02] cursor-pointer shadow-sm
              ${alert.severity === 'CRITICAL' ? 'bg-red-50 border-red-200' : 
                alert.severity === 'WARN' ? 'bg-orange-50 border-orange-200' : 
                'bg-blue-50 border-blue-200'}
            `}
          >
            <div className="mt-0.5">
              {alert.severity === 'CRITICAL' ? <AlertTriangle className="w-5 h-5 text-red-600" /> : 
               alert.severity === 'WARN' ? <AlertTriangle className="w-5 h-5 text-orange-600" /> : 
               <Info className="w-5 h-5 text-blue-600" />}
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-xs font-bold px-2 py-0.5 rounded uppercase border
                  ${alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-700 border-red-200' : 
                    alert.severity === 'WARN' ? 'bg-orange-100 text-orange-700 border-orange-200' : 
                    'bg-blue-100 text-blue-700 border-blue-200'}
                `}>
                  {(alert.type || alert.anomaly_type || "UNKNOWN").replace('_', ' ')}
                </span>
                <span className="text-xs text-neutral-500">{alert.time || new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="text-sm font-medium text-neutral-800">{alert.message || alert.description}</p>
            </div>
          </div>
        ))}
        {alerts.length === 0 && (
          <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
            No active alerts
          </div>
        )}
      </div>
    </div>
  );
}
