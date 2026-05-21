import api from "./client";
import type { Token, User } from "@/types";

export async function login(username: string, password: string): Promise<Token> {
  const { data } = await api.post<Token>("/auth/login", {
    username,
    password,
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
