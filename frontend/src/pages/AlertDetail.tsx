import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { useAlert, useUpdateAlertStatus, useEnrichAlert } from "@/hooks/useAlerts";
import Badge from "@/components/ui/Badge";
import StatusBadge from "@/components/ui/StatusBadge";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

const STATUSES = ["new", "investigating", "resolved", "closed", "false_positive"];

export default function AlertDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: alert, isLoading } = useAlert(id ?? "");
  const updateStatus = useUpdateAlertStatus();
  const enrich = useEnrichAlert();

  if (isLoading) return <LoadingSpinner />;
  if (!alert) return <p className="text-slate-400">Alert not found</p>;

  return (
    <div className="space-y-4">
      <button
        onClick={() => navigate("/alerts")}
        className="flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="h-4 w-4" /> Back to Alerts
      </button>

      <div className="flex items-center gap-3">
        <Badge variant={alert.severity}>{alert.severity}</Badge>
        <h1 className="text-xl font-bold text-white">{alert.title}</h1>
        <StatusBadge status={alert.status} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Details">
          <dl className="space-y-3 text-sm">
            <Row label="ID" value={alert.id} />
            <Row label="Source" value={alert.source} />
            <Row label="Provider Alert ID" value={alert.provider_alert_id} />
            <Row label="MITRE Tactic" value={alert.mitre_tactic} />
            <Row label="MITRE Technique" value={alert.mitre_technique} />
            <Row label="Asset ID" value={alert.asset_id ?? "N/A"} />
            <Row label="Assigned To" value={alert.assigned_to ?? "Unassigned"} />
            <Row
              label="Created"
              value={
                alert.created_at
                  ? new Date(alert.created_at).toLocaleString()
                  : ""
              }
            />
            <Row
              label="Updated"
              value={
                alert.updated_at
                  ? new Date(alert.updated_at).toLocaleString()
                  : ""
              }
            />
          </dl>
        </Card>

        <div className="space-y-4">
          <Card title="Actions">
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">
                  Change Status
                </label>
                <div className="flex flex-wrap gap-2">
                  {STATUSES.map((s) => (
                    <button
                      key={s}
                      onClick={() =>
                        updateStatus.mutate({ alertId: alert.id, status: s })
                      }
                      disabled={alert.status === s}
                      className="px-2 py-1 text-xs rounded bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-30 disabled:cursor-not-allowed capitalize"
                    >
                      {s.replace(/_/g, " ")}
                    </button>
                  ))}
                </div>
              </div>
              <button
                onClick={() => enrich.mutate(alert.id)}
                className="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                Enrich Alert
              </button>
            </div>
          </Card>

          <Card title="IOC Values">
            {alert.ioc_values && alert.ioc_values.length > 0 ? (
              <ul className="space-y-1">
                {alert.ioc_values.map((ioc, i) => (
                  <li
                    key={i}
                    className="text-sm font-mono text-slate-300 bg-slate-900 px-3 py-1.5 rounded"
                  >
                    {ioc}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-400">No IOC values</p>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between">
      <dt className="text-slate-400">{label}</dt>
      <dd className="text-slate-200 font-mono text-xs">{value}</dd>
    </div>
  );
}
