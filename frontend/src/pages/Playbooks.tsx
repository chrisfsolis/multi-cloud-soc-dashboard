import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPlaybooks, runPlaybook, getPlaybookRuns } from "@/api/playbooks";
import Card from "@/components/ui/Card";
import StatusBadge from "@/components/ui/StatusBadge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import EmptyState from "@/components/ui/EmptyState";
import { Play, History } from "lucide-react";
import { useState } from "react";

export default function Playbooks() {
  const { data: playbooks, isLoading } = useQuery({
    queryKey: ["playbooks"],
    queryFn: getPlaybooks,
  });
  const { data: runs } = useQuery({
    queryKey: ["playbook-runs"],
    queryFn: getPlaybookRuns,
  });
  const qc = useQueryClient();
  const run = useMutation({
    mutationFn: (playbookId: string) => runPlaybook(playbookId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["playbooks"] });
      qc.invalidateQueries({ queryKey: ["playbook-runs"] });
    },
  });
  const [showRuns, setShowRuns] = useState(false);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">Playbooks</h1>
        <button
          onClick={() => setShowRuns(!showRuns)}
          className="flex items-center gap-1 px-3 py-1.5 text-sm bg-slate-700 text-slate-300 rounded-lg hover:bg-slate-600"
        >
          <History className="h-4 w-4" /> {showRuns ? "Hide Runs" : "View Runs"}
        </button>
      </div>

      {!playbooks || playbooks.length === 0 ? (
        <EmptyState message="No playbooks configured" />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {playbooks.map((pb) => (
            <Card key={pb.id}>
              <div className="space-y-3">
                <h3 className="font-semibold text-white">{pb.name}</h3>
                <p className="text-sm text-slate-400">{pb.description}</p>
                <div className="flex items-center justify-between text-xs text-slate-500">
                  <span>
                    Runs: {pb.run_count ?? 0}
                  </span>
                  <span>
                    Last:{" "}
                    {pb.last_run
                      ? new Date(pb.last_run).toLocaleDateString()
                      : "Never"}
                  </span>
                </div>
                <button
                  onClick={() => run.mutate(pb.id)}
                  className="flex items-center gap-1 w-full justify-center px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  <Play className="h-4 w-4" /> Run Playbook
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {showRuns && (
        <Card title="Recent Runs">
          {runs && Array.isArray(runs) && runs.length > 0 ? (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-400 border-b border-slate-700">
                  <th className="pb-2">Playbook</th>
                  <th className="pb-2">Status</th>
                  <th className="pb-2">Triggered By</th>
                  <th className="pb-2">Started</th>
                </tr>
              </thead>
              <tbody>
                {runs.map((r) => (
                  <tr key={r.id} className="border-b border-slate-700/50">
                    <td className="py-2 text-slate-300">
                      {r.playbook_name}
                    </td>
                    <td className="py-2">
                      <StatusBadge status={r.status} />
                    </td>
                    <td className="py-2 text-slate-400">
                      {r.triggered_by}
                    </td>
                    <td className="py-2 text-slate-400">
                      {r.started_at
                        ? new Date(r.started_at).toLocaleString()
                        : ""}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-sm text-slate-400">No runs yet</p>
          )}
        </Card>
      )}
    </div>
  );
}
