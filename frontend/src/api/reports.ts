import api from "./client";

export interface ReportResponse {
  markdown: string;
}

export async function getIncidentReport(
  incidentId: string
): Promise<ReportResponse> {
  const { data } = await api.get<ReportResponse>(
    `/reports/incidents/${incidentId}`
  );
  return data;
}

export async function getExecutiveSummary(): Promise<ReportResponse> {
  const { data } = await api.get<ReportResponse>("/reports/executive-summary");
  return data;
}

export async function getMonthlySoc(): Promise<ReportResponse> {
  const { data } = await api.get<ReportResponse>("/reports/monthly-soc");
  return data;
}
