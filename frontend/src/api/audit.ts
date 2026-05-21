import api from "./client";
import type { AuditEntry } from "@/types";

export async function getAuditLog(): Promise<AuditEntry[]> {
  const { data } = await api.get<AuditEntry[]>("/audit");
  return data;
}

export async function getEntityAudit(
  entityType: string,
  entityId: string
): Promise<AuditEntry[]> {
  const { data } = await api.get<AuditEntry[]>(
    `/audit/${entityType}/${entityId}`
  );
  return data;
}
