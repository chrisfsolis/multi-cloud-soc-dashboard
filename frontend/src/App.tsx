import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

type Alert = { id: string; title: string; provider: string; severity: string; status: string; owner: string; timestamp: string; mitre_tactic: string; mitre_technique: string };
type Incident = { id: string; title: string; severity: string; status: string; owner: string; providers: string[]; alert_ids: string[] };
type Asset = { id: string; name: string; provider: string; type: string; risk_level: string; region: string; owner: string };
type Detection = { id: string; name: string; coverage: string; mitre_tactic: string; enabled: boolean };
type Playbook = { id: string; name: string; trigger: string; approval_required: boolean; steps: string[] };
type Metrics = { open_alerts: number; critical_alerts: number; active_incidents: number; cloud_assets: number; mean_time_to_triage_minutes: number; severity_counts: Record<string, number>; alerts_by_provider: Record<string, number>; incidents_by_provider: Record<string, number> };
type Summary = { title: string; summary: string; business_risk: string; recommended_actions: string[] };

type DashboardData = { health: { status: string; service: string }; alerts: Alert[]; incidents: Incident[]; assets: Asset[]; detections: Detection[]; playbooks: Playbook[]; metrics: Metrics; summary: Summary };

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) throw new Error(`${path} returned ${response.status}`);
  return response.json();
}

export default function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [health, alerts, incidents, assets, detections, playbooks, metrics, summary] = await Promise.all([
          getJson<DashboardData["health"]>("/health"),
          getJson<{ items: Alert[] }>("/alerts"),
          getJson<{ items: Incident[] }>("/incidents"),
          getJson<{ items: Asset[] }>("/assets"),
          getJson<{ items: Detection[] }>("/detections"),
          getJson<{ items: Playbook[] }>("/playbooks"),
          getJson<Metrics>("/metrics"),
          getJson<Summary>("/reports/executive-summary"),
        ]);
        setData({ health, alerts: alerts.items, incidents: incidents.items, assets: assets.items, detections: detections.items, playbooks: playbooks.items, metrics, summary });
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to reach the backend API");
      }
    }
    loadDashboard();
  }, []);

  if (error) {
    return <main className="shell"><Hero /><section className="warning"><h2>Backend connection warning</h2><p>The dashboard could not load API data from <code>{API_BASE_URL}</code>.</p><p>Start the backend with: <code>cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000</code></p><p>Details: {error}</p></section></main>;
  }

  if (!data) return <main className="shell"><Hero /><section className="card">Loading synthetic SOC telemetry...</section></main>;

  const kpis = [
    ["Open Alerts", data.metrics.open_alerts], ["Critical Alerts", data.metrics.critical_alerts], ["Active Incidents", data.metrics.active_incidents], ["Cloud Assets", data.metrics.cloud_assets], ["Mean Time to Triage", `${data.metrics.mean_time_to_triage_minutes}m`],
  ];

  return <main className="shell"><Hero />
    <section className="status card"><span className="pulse" /> Backend health: <strong>{data.health.status}</strong> · {data.health.service}</section>
    <section className="kpi-grid">{kpis.map(([label, value]) => <article className="card kpi" key={label}><span>{label}</span><strong>{value}</strong></article>)}</section>
    <section className="grid two"><Breakdown title="Severity Breakdown" values={data.metrics.severity_counts} /><Breakdown title="Provider Breakdown" values={data.metrics.alerts_by_provider} /></section>
    <section className="card"><h2>Recent Alerts</h2><table><thead><tr><th>Alert</th><th>Provider</th><th>Severity</th><th>Status</th><th>Owner</th><th>MITRE</th></tr></thead><tbody>{data.alerts.map(a => <tr key={a.id}><td><strong>{a.id}</strong><br />{a.title}</td><td><Badge text={a.provider} /></td><td><Badge text={a.severity} /></td><td>{a.status}</td><td>{a.owner}</td><td>{a.mitre_tactic}<br /><small>{a.mitre_technique}</small></td></tr>)}</tbody></table></section>
    <section className="grid two"><TableCard title="Active Incidents" rows={data.incidents.map(i => [i.id, i.title, i.severity, i.status, i.providers.join(", ")])} headers={["ID", "Title", "Severity", "Status", "Providers"]} /><TableCard title="Cloud Asset Risk" rows={data.assets.map(a => [a.name, a.provider, a.type, a.risk_level, a.owner])} headers={["Asset", "Provider", "Type", "Risk", "Owner"]} /></section>
    <section className="grid two"><section className="card"><h2>Detections & Playbooks</h2>{data.detections.map(d => <p key={d.id}><strong>{d.name}</strong> — {d.coverage} · {d.mitre_tactic}</p>)}{data.playbooks.map(p => <p key={p.id}><strong>{p.name}</strong> playbook: {p.steps.join(" → ")}</p>)}</section><section className="card"><h2>{data.summary.title}</h2><p>{data.summary.summary}</p><p>{data.summary.business_risk}</p><ul>{data.summary.recommended_actions.map(action => <li key={action}>{action}</li>)}</ul></section></section>
  </main>;
}

function Hero() { return <header className="hero"><p className="eyebrow">Demo-ready cloud security operations</p><h1>Multi-Cloud SOC Dashboard</h1><p>Synthetic demo data for AWS, Azure, and GCP security operations</p></header>; }
function Badge({ text }: { text: string }) { return <span className={`badge ${text.toLowerCase()}`}>{text}</span>; }
function Breakdown({ title, values }: { title: string; values: Record<string, number> }) { return <section className="card"><h2>{title}</h2>{Object.entries(values).map(([key, value]) => <div className="bar-row" key={key}><span>{key}</span><div><i style={{ width: `${Math.max(value * 25, 8)}%` }} /></div><strong>{value}</strong></div>)}</section>; }
function TableCard({ title, headers, rows }: { title: string; headers: string[]; rows: string[][] }) { return <section className="card"><h2>{title}</h2><table><thead><tr>{headers.map(h => <th key={h}>{h}</th>)}</tr></thead><tbody>{rows.map((row, i) => <tr key={i}>{row.map(cell => <td key={cell}>{cell}</td>)}</tr>)}</tbody></table></section>; }
