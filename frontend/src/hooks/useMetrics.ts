import { useQuery } from "@tanstack/react-query";
import {
  getMetricsOverview,
  getMttd,
  getMtta,
  getMttr,
  getProviderRisk,
  getFalsePositiveRate,
  getAlertVolume,
  getMitreBreakdown,
} from "@/api/metrics";

export function useMetricsOverview() {
  return useQuery({
    queryKey: ["metrics", "overview"],
    queryFn: getMetricsOverview,
  });
}

export function useMttd() {
  return useQuery({ queryKey: ["metrics", "mttd"], queryFn: getMttd });
}

export function useMtta() {
  return useQuery({ queryKey: ["metrics", "mtta"], queryFn: getMtta });
}

export function useMttr() {
  return useQuery({ queryKey: ["metrics", "mttr"], queryFn: getMttr });
}

export function useProviderRisk() {
  return useQuery({
    queryKey: ["metrics", "provider-risk"],
    queryFn: getProviderRisk,
  });
}

export function useFalsePositiveRate() {
  return useQuery({
    queryKey: ["metrics", "false-positive-rate"],
    queryFn: getFalsePositiveRate,
  });
}

export function useAlertVolume() {
  return useQuery({
    queryKey: ["metrics", "alert-volume"],
    queryFn: getAlertVolume,
  });
}

export function useMitreBreakdown() {
  return useQuery({
    queryKey: ["metrics", "mitre-breakdown"],
    queryFn: getMitreBreakdown,
  });
}
