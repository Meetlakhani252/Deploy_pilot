import React from 'react';
import { Activity, AlertTriangle, CheckSquare, Clock, ArrowUpRight } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">System Overview</h1>
        <p className="text-sm text-slate-400 mt-1">Live status of managed projects, deployments, and autonomous actions.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Projects</p>
            <p className="text-2xl font-bold text-white mt-1">3</p>
          </div>
          <div className="h-10 w-10 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-400 flex items-center justify-center">
            <Activity className="h-5 w-5" />
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Incidents</p>
            <p className="text-2xl font-bold text-amber-400 mt-1">1</p>
          </div>
          <div className="h-10 w-10 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center">
            <AlertTriangle className="h-5 w-5" />
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Pending Approvals</p>
            <p className="text-2xl font-bold text-emerald-400 mt-1">1</p>
          </div>
          <div className="h-10 w-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <CheckSquare className="h-5 w-5" />
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Deployments (24h)</p>
            <p className="text-2xl font-bold text-white mt-1">12</p>
          </div>
          <div className="h-10 w-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center">
            <Clock className="h-5 w-5" />
          </div>
        </div>
      </div>

      {/* Quick Status Wireframe Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-6 rounded-xl bg-slate-900/50 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-white">Recent Deployments</h2>
            <button className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1">
              View all <ArrowUpRight className="h-3 w-3" />
            </button>
          </div>
          <div className="divide-y divide-slate-800/60">
            <div className="py-3 flex items-center justify-between text-sm">
              <div>
                <p className="font-medium text-slate-200">sample-target-app</p>
                <p className="text-xs text-slate-400">commit 75e2f92 &bull; 5m ago</p>
              </div>
              <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">SUCCESS</span>
            </div>
            <div className="py-3 flex items-center justify-between text-sm">
              <div>
                <p className="font-medium text-slate-200">api-gateway</p>
                <p className="text-xs text-slate-400">commit a12e841 &bull; 42m ago</p>
              </div>
              <span className="px-2 py-0.5 text-xs rounded bg-red-500/10 text-red-400 border border-red-500/20">FAILED</span>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900/50 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-white">AI Incident Diagnostics</h2>
            <span className="px-2 py-0.5 text-xs rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">LangGraph Active</span>
          </div>
          <div className="p-4 rounded-lg bg-slate-950/70 border border-slate-800/80">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-amber-400">INC-109: Port Conflict Detected</span>
              <span className="text-[11px] text-slate-500">2m ago</span>
            </div>
            <p className="text-xs text-slate-300 mt-2">
              Container failed to bind port 8080. Proposed action: rollback to previous release image.
            </p>
            <div className="mt-3 flex items-center gap-2">
              <span className="text-[11px] text-slate-400">Confidence: 94%</span>
              <span className="text-[11px] text-slate-500">&bull;</span>
              <span className="text-[11px] text-amber-400 font-medium">Approval Required</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
