import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getIncidents,
  getIncident,
  createIncident,
  updateIncidentStatus,
  assignIncident,
  addIncidentNote,
  getIncidentTimeline,
  exportIncident,
  runPlaybookOnIncident,
} from "@/api/incidents";
import type { Incident } from "@/types";

export function useIncidents() {
  return useQuery({
    queryKey: ["incidents"],
    queryFn: getIncidents,
  });
}

export function useIncident(incidentId: string) {
  return useQuery({
    queryKey: ["incidents", incidentId],
    queryFn: () => getIncident(incidentId),
    enabled: !!incidentId,
  });
}

export function useCreateIncident() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (incident: Partial<Incident>) => createIncident(incident),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["incidents"] }),
  });
}

export function useUpdateIncidentStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      incidentId,
      status,
    }: {
      incidentId: string;
      status: string;
    }) => updateIncidentStatus(incidentId, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["incidents"] }),
  });
}

export function useAssignIncident() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      incidentId,
      assignedTo,
    }: {
      incidentId: string;
      assignedTo: string;
    }) => assignIncident(incidentId, assignedTo),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["incidents"] }),
  });
}

export function useAddIncidentNote() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      incidentId,
      content,
    }: {
      incidentId: string;
      content: string;
    }) => addIncidentNote(incidentId, content),
    onSuccess: (_, { incidentId }) =>
      qc.invalidateQueries({ queryKey: ["incidents", incidentId] }),
  });
}

export function useIncidentTimeline(incidentId: string) {
  return useQuery({
    queryKey: ["incidents", incidentId, "timeline"],
    queryFn: () => getIncidentTimeline(incidentId),
    enabled: !!incidentId,
  });
}

export function useExportIncident() {
  return useMutation({
    mutationFn: (incidentId: string) => exportIncident(incidentId),
  });
}

export function useRunPlaybookOnIncident() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      incidentId,
      playbookId,
    }: {
      incidentId: string;
      playbookId: string;
    }) => runPlaybookOnIncident(incidentId, playbookId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["incidents"] }),
  });
}
