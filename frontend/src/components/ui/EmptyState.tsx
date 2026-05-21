import { Inbox } from "lucide-react";

interface EmptyStateProps {
  message?: string;
  icon?: React.ReactNode;
}

export default function EmptyState({
  message = "No data available",
  icon,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-slate-500">
      {icon ?? <Inbox className="h-10 w-10 mb-3" />}
      <p className="text-sm">{message}</p>
    </div>
  );
}
