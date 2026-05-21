import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { Bell, ShieldAlert, Clock, AlertTriangle } from "lucide-react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import StatusBadge from "@/components/ui/StatusBadge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { useMetricsOverview } from "@/hooks/useMetrics";

const PIE_COLORS = ["#3b82f6", "#f59e0b", "#ef4444", "#22c55e", "#64748b"];

export default function Dashboard() {
  const { data: metrics, isLoading } = useMetricsOverview();
  const navigate = useNavigate();

  if (isLoading) return <LoadingSpinner />;

  const alertsByProvider = metrics?.alerts_by_provider
    ? Object.entries(metrics.alerts_by_provider).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  const incidentsByStatus = metrics?.incidents_by_status
    ? Object.entries(metrics.incidents_by_status).map(([name, value]) => ({
        name: name.replace(/_/g, " "),
        value,
      }))
    : [];

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-white">Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          icon={<Bell className="h-5 w-5 text-blue-400" />}
          label="Total Alerts"
          value={metrics?.total_alerts ?? 0}
        />
        <KpiCard
          icon={<ShieldAlert className="h-5 w-5 text-orange-400" />}
          label="Open Incidents"
          value={metrics?.open_incidents ?? 0}
        />
        <KpiCard
          icon={<Clock className="h-5 w-5 text-green-400" />}
          label="MTTR (hours)"
          value={metrics?.mttr_hours?.toFixed(1) ?? "N/A"}
        />
        <KpiCard
          icon={<AlertTriangle className="h-5 w-5 text-yellow-400" />}
          label="False Positive Rate"
          value={
            metrics?.false_positive_rate != null
              ? `${(metrics.false_positive_rate * 100).toFixed(1)}%`
              : "N/A"
          }
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Alerts by Provider">
          {alertsByProvider.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={alertsByProvider}>
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1e293b",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                    color: "#fff",
                  }}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-slate-400">No alert data available</p>
          )}
        </Card>

        <Card title="Incidents by Status">
          {incidentsByStatus.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={incidentsByStatus}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                  labelLine={false}
                >
                  {incidentsByStatus.map((_, index) => (
                    <Cell
                      key={index}
                      fill={PIE_COLORS[index % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Legend
                  wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1e293b",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                    color: "#fff",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-slate-400">No incident data available</p>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Top Risky Assets">
          {metrics?.top_risky_assets && Array.isArray(metrics.top_risky_assets) && metrics.top_risky_assets.length > 0 ? (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-400 border-b border-slate-700">
                  <th className="pb-2">Name</th>
                  <th className="pb-2">Provider</th>
                  <th className="pb-2">Risk Score</th>
                </tr>
              </thead>
              <tbody>
                {metrics.top_risky_assets.slice(0, 5).map((asset) => (
                  <tr
                    key={asset.id}
                    className="border-b border-slate-700/50"
                  >
                    <td className="py-2 text-slate-300">{asset.name}</td>
                    <td className="py-2 text-slate-400">{asset.provider}</td>
                    <td className="py-2">
                      <RiskBar score={asset.risk_score} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-sm text-slate-400">No risky assets</p>
          )}
        </Card>

        <Card title="Recent Alerts">
          {metrics?.recent_alerts && Array.isArray(metrics.recent_alerts) && metrics.recent_alerts.length > 0 ? (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-400 border-b border-slate-700">
                  <th className="pb-2">Severity</th>
                  <th className="pb-2">Title</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {metrics.recent_alerts.slice(0, 5).map((alert) => (
                  <tr
                    key={alert.id}
                    className="border-b border-slate-700/50 cursor-pointer hover:bg-slate-700/30"
                    onClick={() => navigate(`/alerts/${alert.id}`)}
                  >
                    <td className="py-2">
                      <Badge variant={alert.severity}>{alert.severity}</Badge>
                    </td>
                    <td className="py-2 text-slate-300">{alert.title}</td>
                    <td className="py-2">
                      <StatusBadge status={alert.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-sm text-slate-400">No recent alerts</p>
          )}
        </Card>
      </div>
    </div>
  );
}

function KpiCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
      <div className="flex items-center gap-3">
        {icon}
        <div>
          <p className="text-xs text-slate-400">{label}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
        </div>
      </div>
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
      <div className="w-16 h-2 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className="text-xs text-slate-400">{score}</span>
    </div>
  );
}
