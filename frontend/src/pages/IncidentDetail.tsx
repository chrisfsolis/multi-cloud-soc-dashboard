import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Clock } from "lucide-react";
import {
  useIncident,
  useUpdateIncidentStatus,
  useAddIncidentNote,
  useIncidentTimeline,
  useExportIncident,
} from "@/hooks/useIncidents";
import Badge from "@/components/ui/Badge";
import StatusBadge from "@/components/ui/StatusBadge";
import Card from "@/components/ui/Card";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

const STATUSES = ["new", "investigating", "contained", "remediated", "closed"];

type Tab = "overview" | "timeline" | "alerts" | "notes";

export default function IncidentDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: incident, isLoading } = useIncident(id ?? "");
  const updateStatus = useUpdateIncidentStatus();
  const addNote = useAddIncidentNote();
  const exportIncident = useExportIncident();
  const { data: timeline } = useIncidentTimeline(id ?? "");
  const [tab, setTab] = useState<Tab>("overview");
  const [noteText, setNoteText] = useState("");

  if (isLoading) return <LoadingSpinner />;
  if (!incident) return <p className="text-slate-400">Incident not found</p>;

  const handleAddNote = () => {
    if (!noteText.trim() || !id) return;
    addNote.mutate({ incidentId: id, content: noteText });
    setNoteText("");
  };

  const tabs: { key: Tab; label: string }[] = [
    { key: "overview", label: "Overview" },
    { key: "timeline", label: "Timeline" },
    { key: "alerts", label: "Alerts" },
    { key: "notes", label: "Notes" },
  ];

  return (
    <div className="space-y-4">
      <button
        onClick={() => navigate("/incidents")}
        className="flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="h-4 w-4" /> Back to Incidents
      </button>

      <div className="flex items-center gap-3 flex-wrap">
        <Badge variant={incident.severity}>{incident.severity}</Badge>
        <h1 className="text-xl font-bold text-white">{incident.title}</h1>
        <StatusBadge status={incident.status} />
      </div>

      <div className="flex items-center gap-2">
        {STATUSES.map((s) => (
          <button
            key={s}
            onClick={() =>
              updateStatus.mutate({ incidentId: incident.id, status: s })
            }
            disabled={incident.status === s}
            className="px-2 py-1 text-xs rounded bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-30 capitalize"
          >
            {s}
          </button>
        ))}
        <button
          onClick={() => exportIncident.mutate(incident.id)}
          className="px-2 py-1 text-xs rounded bg-blue-600 text-white hover:bg-blue-700 ml-2"
        >
          Export
        </button>
      </div>

      <div className="flex gap-1 border-b border-slate-700">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 ${
              tab === t.key
                ? "border-blue-500 text-blue-400"
                : "border-transparent text-slate-400 hover:text-white"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <Card>
          <dl className="space-y-3 text-sm">
            <Row label="ID" value={incident.id} />
            <Row label="Assigned To" value={incident.assigned_to ?? "Unassigned"} />
            <Row
              label="Detection Rule"
              value={incident.detection_rule ?? "N/A"}
            />
            <Row
              label="Providers"
              value={incident.source_providers?.join(", ") ?? ""}
            />
            <Row
              label="MITRE Tactics"
              value={incident.mitre_tactics?.join(", ") ?? ""}
            />
            <Row
              label="Created"
              value={
                incident.created_at
                  ? new Date(incident.created_at).toLocaleString()
                  : ""
              }
            />
          </dl>
        </Card>
      )}

      {tab === "timeline" && (
        <Card>
          {timeline && Array.isArray(timeline) && timeline.length > 0 ? (
            <div className="space-y-4">
              {timeline.map((entry) => (
                <div key={entry.id} className="flex gap-3">
                  <div className="flex flex-col items-center">
                    <Clock className="h-4 w-4 text-blue-400" />
                    <div className="w-px flex-1 bg-slate-700" />
                  </div>
                  <div className="pb-4">
                    <p className="text-sm text-white">{entry.description}</p>
                    <p className="text-xs text-slate-400">
                      {entry.actor} &middot;{" "}
                      {new Date(entry.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400">No timeline events</p>
          )}
        </Card>
      )}

      {tab === "alerts" && (
        <Card>
          {incident.correlated_alerts?.length > 0 ? (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-400 border-b border-slate-700">
                  <th className="pb-2">Severity</th>
                  <th className="pb-2">Title</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {incident.correlated_alerts.map((a) => (
                  <tr key={a.id} className="border-b border-slate-700/50">
                    <td className="py-2">
                      <Badge variant={a.severity}>{a.severity}</Badge>
                    </td>
                    <td className="py-2 text-slate-300">{a.title}</td>
                    <td className="py-2">
                      <StatusBadge status={a.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-sm text-slate-400">No correlated alerts</p>
          )}
        </Card>
      )}

      {tab === "notes" && (
        <Card>
          <div className="space-y-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Add a note..."
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                className="flex-1 px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-sm text-white focus:outline-none focus:border-blue-500"
              />
              <button
                onClick={handleAddNote}
                className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-sm text-white rounded-lg"
              >
                Add
              </button>
            </div>
            <p className="text-sm text-slate-400">
              Notes will appear here when the backend supports persisted notes.
            </p>
          </div>
        </Card>
      )}
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
