import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { login, register, getCurrentUser } from "@/api/auth";

export function useLogin() {
  return useMutation({
    mutationFn: ({ username, password }: { username: string; password: string }) =>
      login(username, password),
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: ({
      username,
      email,
      password,
    }: {
      username: string;
      email: string;
      password: string;
    }) => register(username, email, password),
  });
}

export function useCurrentUser() {
  const qc = useQueryClient();
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: getCurrentUser,
    retry: false,
    enabled: !!localStorage.getItem("token"),
    meta: { qc },
  });
}
