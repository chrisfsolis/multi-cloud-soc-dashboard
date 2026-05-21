import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAlerts, useIngestSampleAlerts } from "@/hooks/useAlerts";
import DataTable, { type Column } from "@/components/ui/DataTable";
import Badge from "@/components/ui/Badge";
import StatusBadge from "@/components/ui/StatusBadge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import type { Alert } from "@/types";

export default function Alerts() {
  const [severity, setSeverity] = useState("");
  const [status, setStatus] = useState("");
  const [source, setSource] = useState("");
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const { data, isLoading } = useAlerts({
    severity: severity || undefined,
    status: status || undefined,
    source: source || undefined,
    search: search || undefined,
  });

  const ingestSample = useIngestSampleAlerts();

  const columns: Column<Alert>[] = [
    {
      key: "severity",
      header: "Severity",
      render: (a) => <Badge variant={a.severity}>{a.severity}</Badge>,
    },
    { key: "title", header: "Title" },
    { key: "source", header: "Source" },
    {
      key: "status",
      header: "Status",
      render: (a) => <StatusBadge status={a.status} />,
    },
    {
      key: "assigned_to",
      header: "Assigned To",
      render: (a) => (
        <span className="text-slate-400">{a.assigned_to ?? "Unassigned"}</span>
      ),
    },
    {
      key: "created_at",
      header: "Created",
      render: (a) =>
        a.created_at ? new Date(a.created_at).toLocaleDateString() : "",
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">Alerts</h1>
        <button
          onClick={() => ingestSample.mutate()}
          className="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Ingest Sample Alerts
        </button>
      </div>

      <div className="flex flex-wrap gap-3">
        <select
          value={severity}
          onChange={(e) => setSeverity(e.target.value)}
          className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Statuses</option>
          <option value="new">New</option>
          <option value="investigating">Investigating</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
          <option value="false_positive">False Positive</option>
        </select>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Sources</option>
          <option value="aws">AWS</option>
          <option value="azure">Azure</option>
          <option value="gcp">GCP</option>
        </select>
        <input
          type="text"
          placeholder="Search alerts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 placeholder:text-slate-500 focus:outline-none focus:border-blue-500 flex-1 min-w-[200px]"
        />
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <DataTable
            columns={columns}
            data={data ?? []}
            keyExtractor={(a) => a.id}
            onRowClick={(a) => navigate(`/alerts/${a.id}`)}
          />
        </div>
      )}
    </div>
  );
}
