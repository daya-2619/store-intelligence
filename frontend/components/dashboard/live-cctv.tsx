"use client";

import { useEffect, useState } from "react";
import { Camera, Users, Clock, AlertTriangle } from "lucide-react";

export function LiveCCTV({ live }: { live: any }) {
  const feeds = live?.camera_status || [];

  return (
    <div className="glass-panel p-6 mb-8 hover-magnet">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold flex items-center gap-2 text-neutral-800">
          <Camera className="w-5 h-5 text-neutral-500" /> Live Camera Feeds
        </h2>
        <div className="flex gap-2">
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-green-500/20 text-green-500 rounded-full">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            LIVE
          </span>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {feeds.map((feed: any) => (
          <div key={feed.camera_id} className="relative group overflow-hidden rounded-xl bg-neutral-100 border border-neutral-200 aspect-video flex flex-col justify-between p-4 shadow-sm">
            <div className="absolute inset-0 bg-gradient-to-t from-white/90 via-white/40 to-transparent z-10" />
            {/* Mock Camera Feed Background */}
            <div className="absolute inset-0 bg-white flex items-center justify-center opacity-70">
               <Camera className="w-10 h-10 text-neutral-300" />
            </div>
            
            <div className="relative z-20 flex justify-between items-start">
              <span className="font-mono text-sm font-semibold bg-white/80 text-neutral-700 px-2 py-1 rounded backdrop-blur-md shadow-sm border border-neutral-200">
                {feed.camera_id}
              </span>
              {feed.anomalies?.map((alert: string, i: number) => (
                <span key={i} className="flex items-center gap-1 text-xs bg-red-100 text-red-600 border border-red-200 px-2 py-1 rounded backdrop-blur-md shadow-sm">
                  <AlertTriangle className="w-3 h-3" />
                  {alert}
                </span>
              ))}
            </div>

            <div className="relative z-20 flex gap-4 text-sm font-medium text-neutral-700">
              <div className="flex items-center gap-1">
                <Users className="w-4 h-4 text-blue-500" />
                <span>{feed.active_visitors}</span>
              </div>
              <div className="flex items-center gap-1">
                <Clock className="w-4 h-4 text-orange-500" />
                <span>{feed.queue_size}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
