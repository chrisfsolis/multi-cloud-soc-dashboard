import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import {
  useMttd,
  useMtta,
  useMttr,
  useAlertVolume,
  useProviderRisk,
  useMitreBreakdown,
} from "@/hooks/useMetrics";

export default function Metrics() {
  const { data: mttd, isLoading: l1 } = useMttd();
  const { data: mtta, isLoading: l2 } = useMtta();
  const { data: mttr, isLoading: l3 } = useMttr();
  const { data: alertVolume, isLoading: l4 } = useAlertVolume();
  const { data: providerRisk, isLoading: l5 } = useProviderRisk();
  const { data: mitreData, isLoading: l6 } = useMitreBreakdown();

  const isLoading = l1 || l2 || l3 || l4 || l5 || l6;

  if (isLoading) return <LoadingSpinner />;

  const tooltipStyle = {
    backgroundColor: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "8px",
    color: "#fff",
  };

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-white">Metrics</h1>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          label="MTTD"
          value={mttd?.value != null ? `${mttd.value}` : "N/A"}
          unit={mttd?.unit ?? "hours"}
        />
        <MetricCard
          label="MTTA"
          value={mtta?.value != null ? `${mtta.value}` : "N/A"}
          unit={mtta?.unit ?? "hours"}
        />
        <MetricCard
          label="MTTR"
          value={mttr?.value != null ? `${mttr.value}` : "N/A"}
          unit={mttr?.unit ?? "hours"}
        />
      </div>

      <Card title="Alert Volume Over Time">
        {Array.isArray(alertVolume) && alertVolume.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={alertVolume}>
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend />
              <Line type="monotone" dataKey="aws" stroke="#f59e0b" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="azure" stroke="#3b82f6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="gcp" stroke="#22c55e" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-sm text-slate-400">No data available</p>
        )}
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Provider Risk Comparison">
          {Array.isArray(providerRisk) && providerRisk.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={providerRisk}>
                <XAxis dataKey="provider" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="risk_score" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-slate-400">No data available</p>
          )}
        </Card>

        <Card title="MITRE Technique Breakdown">
          {Array.isArray(mitreData) && mitreData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={mitreData} layout="vertical">
                <XAxis type="number" stroke="#94a3b8" fontSize={12} />
                <YAxis type="category" dataKey="technique" stroke="#94a3b8" fontSize={11} width={120} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-slate-400">No data available</p>
          )}
        </Card>
      </div>
    </div>
  );
}

function MetricCard({
  label,
  value,
  unit,
}: {
  label: string;
  value: string;
  unit: string;
}) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className="text-3xl font-bold text-white">
        {value}
        <span className="text-sm font-normal text-slate-400 ml-1">{unit}</span>
      </p>
    </div>
  );
}
