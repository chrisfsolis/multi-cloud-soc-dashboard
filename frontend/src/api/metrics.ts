import api from "./client";
import type {
  MetricsOverview,
  MetricValue,
  AlertVolume,
  MitreBreakdown,
  ProviderRisk,
  Asset,
} from "@/types";

export async function getMetricsOverview(): Promise<MetricsOverview> {
  const { data } = await api.get<MetricsOverview>("/metrics/overview");
  return data;
}

export async function getMttd(): Promise<MetricValue> {
  const { data } = await api.get<MetricValue>("/metrics/mttd");
  return data;
}

export async function getMtta(): Promise<MetricValue> {
  const { data } = await api.get<MetricValue>("/metrics/mtta");
  return data;
}

export async function getMttr(): Promise<MetricValue> {
  const { data } = await api.get<MetricValue>("/metrics/mttr");
  return data;
}

export async function getProviderRisk(): Promise<ProviderRisk[]> {
  const { data } = await api.get<ProviderRisk[]>("/metrics/provider-risk");
  return data;
}

export async function getFalsePositiveRate(): Promise<MetricValue> {
  const { data } = await api.get<MetricValue>("/metrics/false-positive-rate");
  return data;
}

export async function getAlertVolume(): Promise<AlertVolume[]> {
  const { data } = await api.get<AlertVolume[]>("/metrics/alert-volume");
  return data;
}

export async function getIncidentVolume(): Promise<Record<string, number>[]> {
  const { data } = await api.get<Record<string, number>[]>(
    "/metrics/incident-volume"
  );
  return data;
}

export async function getMitreBreakdown(): Promise<MitreBreakdown[]> {
  const { data } = await api.get<MitreBreakdown[]>("/metrics/mitre-breakdown");
  return data;
}

export async function getTopRiskyAssets(): Promise<Asset[]> {
  const { data } = await api.get<Asset[]>("/metrics/top-risky-assets");
  return data;
}
