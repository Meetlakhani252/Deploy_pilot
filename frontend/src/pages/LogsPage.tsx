import React from 'react';
import { Terminal, Download } from 'lucide-react';

export const LogsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Logs Explorer</h1>
          <p className="text-sm text-slate-400 mt-1">Live streaming container and deployment logs with level filtering.</p>
        </div>
        <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors">
          <Download className="h-3.5 w-3.5" />
          <span>Export Logs</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-950 font-mono text-xs overflow-hidden shadow-2xl">
        <div className="bg-slate-900/90 px-4 py-2.5 border-b border-slate-800 flex items-center justify-between text-slate-400">
          <div className="flex items-center gap-2">
            <Terminal className="h-4 w-4 text-sky-400" />
            <span>sample-target-app &bull; stdout / stderr</span>
          </div>
          <span className="flex items-center gap-1.5 text-[11px] text-emerald-400">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            Streaming
          </span>
        </div>
        <div className="p-4 space-y-1 text-slate-300 max-h-96 overflow-y-auto">
          <p className="text-slate-500">[2026-11-21 16:50:01] <span className="text-sky-400">[INFO]</span> Starting uvicorn application server...</p>
          <p className="text-slate-500">[2026-11-21 16:50:02] <span className="text-sky-400">[INFO]</span> Application startup complete on 0.0.0.0:8080</p>
          <p className="text-slate-500">[2026-11-21 16:50:10] <span className="text-emerald-400">[INFO]</span> GET /health HTTP/1.1 200 OK</p>
          <p className="text-slate-500">[2026-11-21 16:50:20] <span className="text-emerald-400">[INFO]</span> GET /health HTTP/1.1 200 OK</p>
        </div>
      </div>
    </div>
  );
};
