import api from "./client";
import type { DetectionRule } from "@/types";

export async function getDetections(): Promise<DetectionRule[]> {
  const { data } = await api.get<DetectionRule[]>("/detections");
  return data;
}

export async function getDetection(ruleId: string): Promise<DetectionRule> {
  const { data } = await api.get<DetectionRule>(`/detections/${ruleId}`);
  return data;
}

export async function testDetection(
  rule: Partial<DetectionRule>
): Promise<{ matched: boolean }> {
  const { data } = await api.post<{ matched: boolean }>(
    "/detections/test",
    rule
  );
  return data;
}

export async function reloadDetections(): Promise<{ reloaded: boolean }> {
  const { data } = await api.post<{ reloaded: boolean }>("/detections/reload");
  return data;
}
