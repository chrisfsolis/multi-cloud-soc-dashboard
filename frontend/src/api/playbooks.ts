import api from "./client";
import type { Playbook, PlaybookRun } from "@/types";

export async function getPlaybooks(): Promise<Playbook[]> {
  const { data } = await api.get<Playbook[]>("/playbooks");
  return data;
}

export async function getPlaybook(playbookId: string): Promise<Playbook> {
  const { data } = await api.get<Playbook>(`/playbooks/${playbookId}`);
  return data;
}

export async function runPlaybook(
  playbookId: string,
  incidentId?: string
): Promise<{ status: string }> {
  const { data } = await api.post<{ status: string }>(
    `/playbooks/${playbookId}/run`,
    { incident_id: incidentId }
  );
  return data;
}

export async function approveRun(
  runId: string
): Promise<{ status: string }> {
  const { data } = await api.post<{ status: string }>(
    `/playbooks/runs/${runId}/approve`,
    {}
  );
  return data;
}

export async function cancelRun(
  runId: string
): Promise<{ status: string }> {
  const { data } = await api.post<{ status: string }>(
    `/playbooks/runs/${runId}/cancel`
  );
  return data;
}

export async function getPlaybookRuns(): Promise<PlaybookRun[]> {
  const { data } = await api.get<PlaybookRun[]>("/playbooks/runs");
  return data;
}

export async function getPlaybookRun(runId: string): Promise<PlaybookRun> {
  const { data } = await api.get<PlaybookRun>(`/playbooks/runs/${runId}`);
  return data;
}
