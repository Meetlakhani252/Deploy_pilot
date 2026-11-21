/**
 * Authentication API client.
 * Calls DeployPilot backend endpoints with credentials: 'include'
 * for httpOnly cookie management.
 */

export interface User {
  id: string;
  email: string;
  created_at: string;
  last_login_at: string | null;
  failed_logins?: number;
  locked_until?: string | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface ApiError {
  code: string;
  message: string;
  details?: {
    minutes_remaining?: number;
    attempts_remaining?: number;
    locked_until?: string;
    [key: string]: unknown;
  };
}

const API_BASE = '/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const error: ApiError = {
      code: data?.code || 'UNKNOWN_ERROR',
      message: data?.message || response.statusText || 'An unexpected error occurred',
      details: data?.details,
    };
    throw error;
  }

  return data as T;
}

export async function apiSignup(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });
  return handleResponse<AuthResponse>(response);
}

export async function apiLogin(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });
  return handleResponse<AuthResponse>(response);
}

export async function apiRefreshToken(): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
  return handleResponse<AuthResponse>(response);
}

export async function apiLogout(): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
  return handleResponse<{ message: string }>(response);
}

export async function apiGetMe(token: string): Promise<User> {
  const response = await fetch(`${API_BASE}/auth/me`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  });
  return handleResponse<User>(response);
}
