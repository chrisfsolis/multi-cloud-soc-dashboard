import api from "./client";
import type { Alert, PaginatedResponse } from "@/types";

export interface AlertFilters {
  severity?: string;
  status?: string;
  source?: string;
  search?: string;
}

export async function getAlerts(filters?: AlertFilters): Promise<Alert[]> {
  const params = new URLSearchParams();
  if (filters?.severity) params.append("severity", filters.severity);
  if (filters?.status) params.append("status", filters.status);
  if (filters?.source) params.append("source", filters.source);
  if (filters?.search) params.append("q", filters.search);
  const { data } = await api.get<PaginatedResponse<Alert>>("/alerts", { params });
  return data.items;
}

export async function getAlert(alertId: string): Promise<Alert> {
  const { data } = await api.get<Alert>(`/alerts/${alertId}`);
  return data;
}

export async function ingestAlert(alert: Partial<Alert>): Promise<Alert> {
  const { data } = await api.post<Alert>("/alerts/ingest", alert);
  return data;
}

export async function ingestSampleAlerts(): Promise<{ ok: boolean }> {
  const { data } = await api.post<{ ok: boolean }>("/alerts/ingest/sample");
  return data;
}

export async function updateAlertStatus(
  alertId: string,
  status: string
): Promise<Alert> {
  const { data } = await api.patch<Alert>(`/alerts/${alertId}/status`, {
    status,
  });
  return data;
}

export async function assignAlert(
  alertId: string,
  assignedTo: string
): Promise<Alert> {
  const { data } = await api.patch<Alert>(`/alerts/${alertId}/assign`, {
    assigned_to: assignedTo,
  });
  return data;
}

export async function enrichAlert(alertId: string): Promise<{ ioc_value: string }> {
  const { data } = await api.post<{ ioc_value: string }>(
    `/alerts/${alertId}/enrich`
  );
  return data;
}

export async function searchAlerts(q: string): Promise<Alert[]> {
  const { data } = await api.get<Alert[]>("/alerts/search", { params: { q } });
  return data;
}
