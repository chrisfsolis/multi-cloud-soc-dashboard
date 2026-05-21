import { useState } from "react";
import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";
import EmptyState from "./EmptyState";

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string;
  onRowClick?: (item: T) => void;
  pageSize?: number;
}

export default function DataTable<T>({
  columns,
  data,
  keyExtractor,
  onRowClick,
  pageSize = 10,
}: DataTableProps<T>) {
  const [page, setPage] = useState(0);
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const sorted = [...data];
  if (sortKey) {
    sorted.sort((a, b) => {
      const aVal = (a as Record<string, unknown>)[sortKey];
      const bVal = (b as Record<string, unknown>)[sortKey];
      if (aVal == null) return 1;
      if (bVal == null) return -1;
      const cmp = String(aVal).localeCompare(String(bVal));
      return sortDir === "asc" ? cmp : -cmp;
    });
  }

  const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const paged = sorted.slice(page * pageSize, (page + 1) * pageSize);

  if (data.length === 0) return <EmptyState />;

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700">
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer select-none"
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                >
                  <span className="flex items-center gap-1">
                    {col.header}
                    {col.sortable !== false &&
                      (sortKey === col.key ? (
                        sortDir === "asc" ? (
                          <ChevronUp className="h-3 w-3" />
                        ) : (
                          <ChevronDown className="h-3 w-3" />
                        )
                      ) : (
                        <ChevronsUpDown className="h-3 w-3 opacity-30" />
                      ))}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((item, i) => (
              <tr
                key={keyExtractor(item)}
                className={`border-b border-slate-700/50 transition-colors ${
                  onRowClick ? "cursor-pointer hover:bg-slate-700/30" : ""
                } ${i % 2 === 0 ? "bg-slate-800/30" : ""}`}
                onClick={() => onRowClick?.(item)}
              >
                {columns.map((col) => (
                  <td key={col.key} className="px-4 py-3 text-slate-300">
                    {col.render
                      ? col.render(item)
                      : String(
                          (item as Record<string, unknown>)[col.key] ?? ""
                        )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 border-t border-slate-700">
          <span className="text-xs text-slate-400">
            Showing {page * pageSize + 1}-
            {Math.min((page + 1) * pageSize, sorted.length)} of {sorted.length}
          </span>
          <div className="flex gap-2">
            <button
              disabled={page === 0}
              onClick={() => setPage((p) => p - 1)}
              className="px-3 py-1 text-xs rounded bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Prev
            </button>
            <button
              disabled={page >= totalPages - 1}
              onClick={() => setPage((p) => p + 1)}
              className="px-3 py-1 text-xs rounded bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
