import {
  LayoutDashboard,
  Activity,
  AlertTriangle,
  Camera,
} from "lucide-react";

export default function Sidebar() {

  return (

    <aside className="w-64 border-r bg-card">

      <div className="p-6">

        <h2 className="font-bold text-xl">
          Store Intelligence
        </h2>

      </div>

      <nav className="space-y-2 p-4">

        <a href="#dashboard" className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer transition-colors text-inherit no-underline">

          <LayoutDashboard size={18} />

          Dashboard

        </a>

        <a href="#funnel" className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer transition-colors text-inherit no-underline">

          <Activity size={18} />

          Funnel

        </a>

        <a href="#anomalies" className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer transition-colors text-inherit no-underline">

          <AlertTriangle size={18} />

          Anomalies

        </a>

        <a href="#cctv" className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer transition-colors text-inherit no-underline">

          <Camera size={18} />

          CCTV

        </a>

      </nav>

    </aside>
  );
}