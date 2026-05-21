import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Bell,
  ShieldAlert,
  Server,
  Search,
  BookOpen,
  BarChart3,
  FileText,
  ClipboardList,
} from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/alerts", label: "Alerts", icon: Bell },
  { to: "/incidents", label: "Incidents", icon: ShieldAlert },
  { to: "/assets", label: "Assets", icon: Server },
  { to: "/detections", label: "Detections", icon: Search },
  { to: "/playbooks", label: "Playbooks", icon: BookOpen },
  { to: "/metrics", label: "Metrics", icon: BarChart3 },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/audit", label: "Audit Log", icon: ClipboardList },
];

export default function Sidebar() {
  return (
    <aside className="w-60 min-h-screen bg-slate-900 border-r border-slate-700 flex flex-col">
      <div className="p-4 border-b border-slate-700">
        <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
          <ShieldAlert className="h-5 w-5 text-blue-400" />
          SOC Dashboard
        </h1>
      </div>
      <nav className="flex-1 p-2 space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-600/20 text-blue-400"
                  : "text-slate-400 hover:text-white hover:bg-slate-800"
              }`
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
