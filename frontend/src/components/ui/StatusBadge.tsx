const statusColors: Record<string, string> = {
  new: "text-blue-400",
  investigating: "text-yellow-400",
  contained: "text-orange-400",
  resolved: "text-green-400",
  remediated: "text-green-400",
  closed: "text-slate-400",
  false_positive: "text-slate-500",
  running: "text-blue-400",
  completed: "text-green-400",
  failed: "text-red-400",
  cancelled: "text-slate-400",
  pending_approval: "text-yellow-400",
};

const dotColors: Record<string, string> = {
  new: "bg-blue-400",
  investigating: "bg-yellow-400",
  contained: "bg-orange-400",
  resolved: "bg-green-400",
  remediated: "bg-green-400",
  closed: "bg-slate-400",
  false_positive: "bg-slate-500",
  running: "bg-blue-400",
  completed: "bg-green-400",
  failed: "bg-red-400",
  cancelled: "bg-slate-400",
  pending_approval: "bg-yellow-400",
};

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export default function StatusBadge({ status, className = "" }: StatusBadgeProps) {
  const textColor = statusColors[status] ?? "text-slate-400";
  const dot = dotColors[status] ?? "bg-slate-400";
  const label = status.replace(/_/g, " ");

  return (
    <span className={`inline-flex items-center gap-1.5 text-xs font-medium capitalize ${textColor} ${className}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${dot}`} />
      {label}
    </span>
  );
}
