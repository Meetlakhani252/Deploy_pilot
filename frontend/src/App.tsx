import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from './components/layout/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { DeploymentsPage } from './pages/DeploymentsPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { ApprovalsPage } from './pages/ApprovalsPage';
import { LogsPage } from './pages/LogsPage';
import { MetricsPage } from './pages/MetricsPage';
import { SettingsPage } from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 1000 * 30, // 30 seconds
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="projects" element={<ProjectsPage />} />
            <Route path="deployments" element={<DeploymentsPage />} />
            <Route path="incidents" element={<IncidentsPage />} />
            <Route path="approvals" element={<ApprovalsPage />} />
            <Route path="logs" element={<LogsPage />} />
            <Route path="metrics" element={<MetricsPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
