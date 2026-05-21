import api from "./client";
import type { Token, User } from "@/types";

export async function login(username: string, password: string): Promise<Token> {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  const { data } = await api.post<Token>("/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

export async function register(
  username: string,
  email: string,
  password: string
): Promise<User> {
  const { data } = await api.post<User>("/auth/register", {
    username,
    email,
    password,
  });
  return data;
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}
