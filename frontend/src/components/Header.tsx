import { LogOut, User } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export default function Header() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="h-14 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">
      <h2 className="text-sm font-semibold text-slate-300">
        Multi-Cloud Security Operations Center
      </h2>
      {isAuthenticated && (
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-2 text-sm text-slate-300">
            <User className="h-4 w-4" />
            {user?.username ?? "User"}
          </span>
          <button
            onClick={logout}
            className="flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
          >
            <LogOut className="h-4 w-4" />
            Logout
          </button>
        </div>
      )}
    </header>
  );
}
