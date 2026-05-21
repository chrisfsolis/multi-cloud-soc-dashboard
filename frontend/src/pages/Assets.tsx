import { useState } from "react";
import { useAssets, useHighRiskAssets } from "@/hooks/useAssets";
import DataTable, { type Column } from "@/components/ui/DataTable";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import type { Asset } from "@/types";

export default function Assets() {
  const [tab, setTab] = useState<"all" | "high-risk">("all");
  const { data: allAssets, isLoading: loadingAll } = useAssets();
  const { data: highRisk, isLoading: loadingHigh } = useHighRiskAssets();

  const data = tab === "all" ? allAssets : highRisk;
  const isLoading = tab === "all" ? loadingAll : loadingHigh;

  const columns: Column<Asset>[] = [
    { key: "name", header: "Name" },
    { key: "type", header: "Type" },
    { key: "provider", header: "Provider" },
    { key: "environment", header: "Environment" },
    {
      key: "risk_score",
      header: "Risk Score",
      render: (a) => <RiskBar score={a.risk_score} />,
    },
    {
      key: "alert_count",
      header: "Alerts",
      render: (a) => (
        <span
          className={`text-sm font-medium ${a.alert_count > 0 ? "text-orange-400" : "text-slate-500"}`}
        >
          {a.alert_count}
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold text-white">Assets</h1>

      <div className="flex gap-1 border-b border-slate-700">
        {(["all", "high-risk"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors capitalize ${
              tab === t
                ? "border-blue-500 text-blue-400"
                : "border-transparent text-slate-400 hover:text-white"
            }`}
          >
            {t === "high-risk" ? "High Risk" : "All"}
          </button>
        ))}
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <DataTable
            columns={columns}
            data={data ?? []}
            keyExtractor={(a) => a.id}
          />
        </div>
      )}
    </div>
  );
}

function RiskBar({ score }: { score: number }) {
  const color =
    score >= 80
      ? "bg-red-500"
      : score >= 60
        ? "bg-orange-500"
        : score >= 40
          ? "bg-yellow-500"
          : "bg-green-500";
  return (
    <div className="flex items-center gap-2">
      <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
      <span className="text-xs text-slate-400 w-6">{score}</span>
    </div>
  );
}
