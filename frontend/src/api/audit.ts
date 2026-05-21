import api from "./client";
import type { AuditEntry, PaginatedResponse } from "@/types";

export async function getAuditLog(): Promise<AuditEntry[]> {
  const { data } = await api.get<PaginatedResponse<AuditEntry>>("/audit");
  return data.items;
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
