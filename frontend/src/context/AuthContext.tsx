import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import { login as apiLogin, register as apiRegister, getCurrentUser } from "@/api/auth";
import type { User } from "@/types";

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem("token")
  );
  const [isLoading, setIsLoading] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      getCurrentUser()
        .then(setUser)
        .catch(() => {
          localStorage.removeItem("token");
          setToken(null);
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = useCallback(async (username: string, password: string) => {
    const result = await apiLogin(username, password);
    localStorage.setItem("token", result.access_token);
    setToken(result.access_token);
    const me = await getCurrentUser();
    setUser(me);
  }, []);

  const register = useCallback(
    async (username: string, email: string, password: string) => {
      await apiRegister(username, email, password);
      await login(username, password);
    },
    [login]
  );

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
