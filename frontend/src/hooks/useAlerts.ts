import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getAlerts,
  getAlert,
  ingestAlert,
  ingestSampleAlerts,
  updateAlertStatus,
  assignAlert,
  enrichAlert,
  type AlertFilters,
} from "@/api/alerts";
import type { Alert } from "@/types";

export function useAlerts(filters?: AlertFilters) {
  return useQuery({
    queryKey: ["alerts", filters],
    queryFn: () => getAlerts(filters),
  });
}

export function useAlert(alertId: string) {
  return useQuery({
    queryKey: ["alerts", alertId],
    queryFn: () => getAlert(alertId),
    enabled: !!alertId,
  });
}

export function useIngestAlert() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (alert: Partial<Alert>) => ingestAlert(alert),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}

export function useIngestSampleAlerts() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ingestSampleAlerts,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}

export function useUpdateAlertStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ alertId, status }: { alertId: string; status: string }) =>
      updateAlertStatus(alertId, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}

export function useAssignAlert() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      alertId,
      assignedTo,
    }: {
      alertId: string;
      assignedTo: string;
    }) => assignAlert(alertId, assignedTo),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}

export function useEnrichAlert() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (alertId: string) => enrichAlert(alertId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}
