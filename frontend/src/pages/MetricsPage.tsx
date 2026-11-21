import React from 'react';
import { Activity } from 'lucide-react';

export const MetricsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Metrics & Health</h1>
        <p className="text-sm text-slate-400 mt-1">cAdvisor, node_exporter, and Prometheus telemetry.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>CPU Usage</span>
            <Activity className="h-4 w-4 text-sky-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">12.4%</p>
          <p className="text-[11px] text-slate-500 mt-1">Threshold: 80%</p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Memory Usage</span>
            <Activity className="h-4 w-4 text-emerald-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">248 MB</p>
          <p className="text-[11px] text-slate-500 mt-1">Limit: 1024 MB</p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Disk Usage</span>
            <Activity className="h-4 w-4 text-indigo-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">1.8 GB</p>
          <p className="text-[11px] text-slate-500 mt-1">Host root /dev/sda1</p>
        </div>
      </div>
    </div>
  );
};
