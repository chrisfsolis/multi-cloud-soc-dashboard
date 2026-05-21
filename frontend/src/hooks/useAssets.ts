import { useQuery } from "@tanstack/react-query";
import { getAssets, getAsset, getHighRiskAssets } from "@/api/assets";

export function useAssets() {
  return useQuery({
    queryKey: ["assets"],
    queryFn: getAssets,
  });
}

export function useAsset(assetId: string) {
  return useQuery({
    queryKey: ["assets", assetId],
    queryFn: () => getAsset(assetId),
    enabled: !!assetId,
  });
}

export function useHighRiskAssets() {
  return useQuery({
    queryKey: ["assets", "high-risk"],
    queryFn: getHighRiskAssets,
  });
}
