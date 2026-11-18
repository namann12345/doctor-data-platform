import api from '../lib/api';
import { TokenResponse, LoginRequest, RegisterRequest, User, ChangePasswordRequest } from '../types';

// Maps the flat token response from backend into a usable object
function tokenToUser(data: TokenResponse): User {
  return {
    id: data.user_id,
    full_name: data.full_name,
    email: data.email,
    credit_balance: data.credit_balance,
    is_active: true,
    is_admin: data.is_admin,
  };
}

export const authService = {
  async login(data: LoginRequest): Promise<{ access_token: string; user: User }> {
    // Backend expects form data for /login
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);
    const response = await api.post<TokenResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return { access_token: response.data.access_token, user: tokenToUser(response.data) };
  },

  async register(data: RegisterRequest): Promise<{ access_token: string; user: User }> {
    const response = await api.post<TokenResponse>('/auth/register', data);
    return { access_token: response.data.access_token, user: tokenToUser(response.data) };
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  async changePassword(data: ChangePasswordRequest): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/change-password', data);
    return response.data;
  },

  async forgotPassword(email: string): Promise<{ message: string }> {
    // Demo flow
    return { message: `Demo: Password reset email sent to ${email}` };
  },
};
