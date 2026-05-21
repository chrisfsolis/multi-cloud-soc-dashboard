import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { getExecutiveSummary, getMonthlySoc } from "@/api/reports";
import Card from "@/components/ui/Card";
import { FileText, BarChart3, Calendar } from "lucide-react";

type ReportType = "executive" | "monthly" | null;

export default function Reports() {
  const [activeReport, setActiveReport] = useState<ReportType>(null);
  const [markdown, setMarkdown] = useState("");

  const executive = useMutation({
    mutationFn: getExecutiveSummary,
    onSuccess: (data) => {
      setMarkdown(data.markdown);
      setActiveReport("executive");
    },
  });

  const monthly = useMutation({
    mutationFn: getMonthlySoc,
    onSuccess: (data) => {
      setMarkdown(data.markdown);
      setActiveReport("monthly");
    },
  });

  const reports = [
    {
      key: "executive" as const,
      icon: <BarChart3 className="h-6 w-6 text-blue-400" />,
      title: "Executive Summary",
      description: "High-level overview for leadership",
      action: () => executive.mutate(),
      loading: executive.isPending,
    },
    {
      key: "monthly" as const,
      icon: <Calendar className="h-6 w-6 text-green-400" />,
      title: "Monthly SOC Report",
      description: "Comprehensive monthly security operations report",
      action: () => monthly.mutate(),
      loading: monthly.isPending,
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-white">Reports</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {reports.map((r) => (
          <Card key={r.key}>
            <div className="space-y-3 text-center">
              <div className="flex justify-center">{r.icon}</div>
              <h3 className="font-semibold text-white">{r.title}</h3>
              <p className="text-sm text-slate-400">{r.description}</p>
              <button
                onClick={r.action}
                disabled={r.loading}
                className="w-full px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50"
              >
                {r.loading ? "Generating..." : "Generate Report"}
              </button>
            </div>
          </Card>
        ))}

        <Card>
          <div className="space-y-3 text-center">
            <div className="flex justify-center">
              <FileText className="h-6 w-6 text-orange-400" />
            </div>
            <h3 className="font-semibold text-white">Incident Report</h3>
            <p className="text-sm text-slate-400">
              Generate from the Incident Detail page
            </p>
          </div>
        </Card>
      </div>

      {activeReport && markdown && (
        <Card
          title={
            activeReport === "executive"
              ? "Executive Summary"
              : "Monthly SOC Report"
          }
        >
          <div className="prose prose-invert prose-sm max-w-none whitespace-pre-wrap text-slate-300">
            {markdown}
          </div>
        </Card>
      )}
    </div>
  );
}
