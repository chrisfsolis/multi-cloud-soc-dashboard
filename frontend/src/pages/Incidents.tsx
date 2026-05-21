import { useNavigate } from "react-router-dom";
import { Plus } from "lucide-react";
import { useIncidents } from "@/hooks/useIncidents";
import DataTable, { type Column } from "@/components/ui/DataTable";
import Badge from "@/components/ui/Badge";
import StatusBadge from "@/components/ui/StatusBadge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import type { Incident } from "@/types";

export default function Incidents() {
  const { data, isLoading } = useIncidents();
  const navigate = useNavigate();

  const columns: Column<Incident>[] = [
    {
      key: "severity",
      header: "Severity",
      render: (inc) => <Badge variant={inc.severity}>{inc.severity}</Badge>,
    },
    { key: "title", header: "Title" },
    {
      key: "status",
      header: "Status",
      render: (inc) => <StatusBadge status={inc.status} />,
    },
    {
      key: "assigned_to",
      header: "Assigned",
      render: (inc) => (
        <span className="text-slate-400">
          {inc.assigned_to ?? "Unassigned"}
        </span>
      ),
    },
    {
      key: "source_providers",
      header: "Providers",
      render: (inc) => (
        <span className="text-slate-400">
          {inc.source_providers?.join(", ") ?? ""}
        </span>
      ),
    },
    {
      key: "created_at",
      header: "Created",
      render: (inc) =>
        inc.created_at ? new Date(inc.created_at).toLocaleDateString() : "",
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">Incidents</h1>
        <button
          onClick={() => navigate("/incidents/new")}
          className="flex items-center gap-1 px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          <Plus className="h-4 w-4" /> Create Incident
        </button>
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <DataTable
            columns={columns}
            data={data ?? []}
            keyExtractor={(inc) => inc.id}
            onRowClick={(inc) => navigate(`/incidents/${inc.id}`)}
          />
        </div>
      )}
    </div>
  );
}
