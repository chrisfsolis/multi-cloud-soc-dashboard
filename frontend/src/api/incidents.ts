import api from "./client";
import type { Incident, IncidentNote, TimelineEntry } from "@/types";

export async function getIncidents(): Promise<Incident[]> {
  const { data } = await api.get<Incident[]>("/incidents");
  return data;
}

export async function getIncident(incidentId: string): Promise<Incident> {
  const { data } = await api.get<Incident>(`/incidents/${incidentId}`);
  return data;
}

export async function createIncident(
  incident: Partial<Incident>
): Promise<Incident> {
  const { data } = await api.post<Incident>("/incidents", incident);
  return data;
}

export async function updateIncidentStatus(
  incidentId: string,
  status: string
): Promise<Incident> {
  const { data } = await api.patch<Incident>(
    `/incidents/${incidentId}/status`,
    { status }
  );
  return data;
}

export async function assignIncident(
  incidentId: string,
  assignedTo: string
): Promise<Incident> {
  const { data } = await api.patch<Incident>(
    `/incidents/${incidentId}/assign`,
    { assigned_to: assignedTo }
  );
  return data;
}

export async function addIncidentNote(
  incidentId: string,
  content: string
): Promise<IncidentNote> {
  const { data } = await api.post<IncidentNote>(
    `/incidents/${incidentId}/notes`,
    { content }
  );
  return data;
}

export async function getIncidentTimeline(
  incidentId: string
): Promise<TimelineEntry[]> {
  const { data } = await api.get<TimelineEntry[]>(
    `/incidents/${incidentId}/timeline`
  );
  return data;
}

export async function exportIncident(
  incidentId: string
): Promise<{ format: string; markdown?: string }> {
  const { data } = await api.post<{ format: string; markdown?: string }>(
    `/incidents/${incidentId}/export`
  );
  return data;
}

export async function runPlaybookOnIncident(
  incidentId: string,
  playbookId: string
): Promise<{ status: string }> {
  const { data } = await api.post<{ status: string }>(
    `/incidents/${incidentId}/run-playbook`,
    { playbook_id: playbookId }
  );
  return data;
}
