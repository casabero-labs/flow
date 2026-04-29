import api from './client';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export const login = async (email: string, password: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', { email, password });
  if (response.data.token) {
    localStorage.setItem('flow_token', response.data.token);
    localStorage.setItem('flow_user', JSON.stringify(response.data.user));
  }
  return response.data;
};

export const register = async (email: string, password: string, name: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/register', { email, password, name });
  if (response.data.token) {
    localStorage.setItem('flow_token', response.data.token);
    localStorage.setItem('flow_user', JSON.stringify(response.data.user));
  }
  return response.data;
};

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>('/auth/me');
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('flow_token');
  localStorage.removeItem('flow_user');
};
