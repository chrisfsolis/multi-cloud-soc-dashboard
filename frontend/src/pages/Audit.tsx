import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getAuditLog } from "@/api/audit";
import DataTable, { type Column } from "@/components/ui/DataTable";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import type { AuditEntry } from "@/types";

export default function Audit() {
  const { data, isLoading } = useQuery({
    queryKey: ["audit"],
    queryFn: getAuditLog,
  });

  const [expanded, setExpanded] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const filtered = (data ?? []).filter(
    (e) => !filter || e.entity_type === filter
  );

  const entityTypes = [
    ...new Set((data ?? []).map((e) => e.entity_type)),
  ];

  const columns: Column<AuditEntry>[] = [
    {
      key: "timestamp",
      header: "Timestamp",
      render: (e) =>
        e.timestamp ? new Date(e.timestamp).toLocaleString() : "",
    },
    { key: "entity_type", header: "Entity Type" },
    { key: "entity_id", header: "Entity ID" },
    { key: "action", header: "Action" },
    { key: "actor", header: "Actor" },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold text-white">Audit Log</h1>

      <div className="flex gap-3">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Entity Types</option>
          {entityTypes.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <DataTable
            columns={columns}
            data={filtered}
            keyExtractor={(e) => e.id}
            onRowClick={(e) =>
              setExpanded(expanded === e.id ? null : e.id)
            }
          />
          {expanded && (
            <ExpandedAudit
              entry={filtered.find((e) => e.id === expanded) ?? null}
            />
          )}
        </div>
      )}
    </div>
  );
}

function ExpandedAudit({ entry }: { entry: AuditEntry | null }) {
  if (!entry) return null;
  return (
    <div className="px-4 py-3 bg-slate-900 border-t border-slate-700">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h4 className="text-xs font-medium text-slate-400 mb-2">Before</h4>
          <pre className="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg overflow-auto max-h-40">
            {entry.before
              ? JSON.stringify(entry.before, null, 2)
              : "N/A"}
          </pre>
        </div>
        <div>
          <h4 className="text-xs font-medium text-slate-400 mb-2">After</h4>
          <pre className="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg overflow-auto max-h-40">
            {entry.after
              ? JSON.stringify(entry.after, null, 2)
              : "N/A"}
          </pre>
        </div>
      </div>
    </div>
  );
}
