import api from "./client";
import type { Alert, Asset, PaginatedResponse } from "@/types";

export async function getAssets(): Promise<Asset[]> {
  const { data } = await api.get<PaginatedResponse<Asset>>("/assets");
  return data.items;
}

export async function getHighRiskAssets(): Promise<Asset[]> {
  const { data } = await api.get<Asset[]>("/assets/high-risk");
  return data;
}

export async function getAsset(assetId: string): Promise<Asset> {
  const { data } = await api.get<Asset>(`/assets/${assetId}`);
  return data;
}

export async function updateAsset(
  assetId: string,
  updates: Partial<Asset>
): Promise<Asset> {
  const { data } = await api.patch<Asset>(`/assets/${assetId}`, updates);
  return data;
}

export async function getAssetAlerts(assetId: string): Promise<Alert[]> {
  const { data } = await api.get<Alert[]>(`/assets/${assetId}/alerts`);
  return data;
}

export async function getAssetRisk(
  assetId: string
): Promise<{ risk: number }> {
  const { data } = await api.get<{ risk: number }>(
    `/assets/${assetId}/risk`
  );
  return data;
}
