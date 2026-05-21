export interface Alert {
  id: string;
  source: "aws" | "azure" | "gcp";
  provider_alert_id: string;
  title: string;
  severity: "critical" | "high" | "medium" | "low";
  status: "new" | "investigating" | "resolved" | "closed" | "false_positive";
  mitre_tactic: string;
  mitre_technique: string;
  asset_id: string | null;
  ioc_values: string[];
  assigned_to: string | null;
  created_at: string;
  updated_at: string;
}

export interface Incident {
  id: string;
  title: string;
  severity: "critical" | "high" | "medium" | "low";
  status: "new" | "investigating" | "contained" | "remediated" | "closed";
  assigned_to: string | null;
  source_providers: string[];
  mitre_tactics: string[];
  detection_rule: string | null;
  correlated_alerts: Alert[];
  affected_assets: Asset[];
  created_at: string;
  updated_at: string;
}

export interface IncidentNote {
  id: string;
  incident_id: string;
  author: string;
  content: string;
  created_at: string;
}

export interface Asset {
  id: string;
  name: string;
  type: string;
  provider: "aws" | "azure" | "gcp";
  environment: string;
  risk_score: number;
  tags: Record<string, string>;
  alert_count: number;
  created_at: string;
  updated_at: string;
}

export interface DetectionRule {
  id: string;
  name: string;
  description: string;
  mitre_technique: string;
  mitre_tactic: string;
  severity: "critical" | "high" | "medium" | "low";
  enabled: boolean;
  query: string;
  source_providers: string[];
  created_at: string;
  updated_at: string;
}

export interface Playbook {
  id: string;
  name: string;
  description: string;
  steps: PlaybookStep[];
  last_run: string | null;
  run_count: number;
  created_at: string;
  updated_at: string;
}

export interface PlaybookStep {
  order: number;
  action: string;
  description: string;
  requires_approval: boolean;
}

export interface PlaybookRun {
  id: string;
  playbook_id: string;
  playbook_name: string;
  incident_id: string | null;
  status: "pending_approval" | "running" | "completed" | "failed" | "cancelled";
  started_at: string;
  completed_at: string | null;
  triggered_by: string;
  results: Record<string, unknown>;
}

export interface MetricsOverview {
  total_alerts: number;
  open_incidents: number;
  mttr_hours: number;
  false_positive_rate: number;
  alerts_by_severity: Record<string, number>;
  alerts_by_provider: Record<string, number>;
  incidents_by_status: Record<string, number>;
  top_risky_assets: Asset[];
  recent_alerts: Alert[];
}

export interface AuditEntry {
  id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  actor: string;
  timestamp: string;
  before: Record<string, unknown> | null;
  after: Record<string, unknown> | null;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface TimelineEntry {
  id: string;
  incident_id: string;
  event_type: string;
  description: string;
  actor: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface HealthStatus {
  status: string;
  dependencies?: Record<string, string>;
}

export interface MetricValue {
  value: number;
  unit: string;
  period_start?: string;
  period_end?: string;
}

export interface AlertVolume {
  date: string;
  aws: number;
  azure: number;
  gcp: number;
  total: number;
}

export interface MitreBreakdown {
  technique: string;
  tactic: string;
  count: number;
}

export interface ProviderRisk {
  provider: string;
  risk_score: number;
  alert_count: number;
}
