import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getDetections, testDetection, reloadDetections } from "@/api/detections";
import DataTable, { type Column } from "@/components/ui/DataTable";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import type { DetectionRule } from "@/types";
import { RefreshCw, Zap } from "lucide-react";

export default function Detections() {
  const { data, isLoading } = useQuery({
    queryKey: ["detections"],
    queryFn: getDetections,
  });

  const qc = useQueryClient();
  const reload = useMutation({
    mutationFn: reloadDetections,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["detections"] }),
  });
  const test = useMutation({ mutationFn: testDetection });

  const columns: Column<DetectionRule>[] = [
    { key: "name", header: "Name" },
    { key: "mitre_technique", header: "MITRE Technique" },
    {
      key: "severity",
      header: "Severity",
      render: (r) => <Badge variant={r.severity}>{r.severity}</Badge>,
    },
    {
      key: "enabled",
      header: "Enabled",
      render: (r) => (
        <span
          className={`text-xs font-medium ${r.enabled ? "text-green-400" : "text-slate-500"}`}
        >
          {r.enabled ? "Yes" : "No"}
        </span>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      sortable: false,
      render: (r) => (
        <button
          onClick={(e) => {
            e.stopPropagation();
            test.mutate(r);
          }}
          className="flex items-center gap-1 px-2 py-1 text-xs bg-slate-700 text-slate-300 rounded hover:bg-slate-600"
        >
          <Zap className="h-3 w-3" /> Test
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">Detection Rules</h1>
        <button
          onClick={() => reload.mutate()}
          className="flex items-center gap-1 px-3 py-1.5 text-sm bg-slate-700 text-slate-300 rounded-lg hover:bg-slate-600"
        >
          <RefreshCw className="h-4 w-4" /> Reload
        </button>
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <DataTable
            columns={columns}
            data={data ?? []}
            keyExtractor={(r) => r.id}
          />
        </div>
      )}
    </div>
  );
}
