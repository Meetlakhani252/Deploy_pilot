import React from 'react';
import { Rocket, RefreshCw } from 'lucide-react';

export const DeploymentsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Deployments</h1>
          <p className="text-sm text-slate-400 mt-1">Deployment history, container lifecycles, and health check results.</p>
        </div>
        <button className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium transition-colors border border-slate-700">
          <RefreshCw className="h-4 w-4" />
          <span>Refresh</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/50 overflow-hidden">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-900 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800">
            <tr>
              <th className="px-6 py-3.5 font-medium">Project</th>
              <th className="px-6 py-3.5 font-medium">Commit</th>
              <th className="px-6 py-3.5 font-medium">Trigger</th>
              <th className="px-6 py-3.5 font-medium">Status</th>
              <th className="px-6 py-3.5 font-medium">Started</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            <tr>
              <td className="px-6 py-4 font-medium text-white flex items-center gap-2">
                <Rocket className="h-4 w-4 text-sky-400" />
                sample-target-app
              </td>
              <td className="px-6 py-4 font-mono text-xs text-slate-400">75e2f92 (v1.0.0)</td>
              <td className="px-6 py-4 text-xs">push</td>
              <td className="px-6 py-4">
                <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  SUCCESS
                </span>
              </td>
              <td className="px-6 py-4 text-xs text-slate-400">10m ago</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
