// Core domain types aligned with backend responses

export interface User {
  id: number;
  full_name: string;
  email: string;
  phone?: string;
  credit_balance: number;
  is_active: boolean;
  is_admin: boolean;
}

export interface Doctor {
  id: number;
  name: string;
  specialty: string;
  qualification?: string;
  experience_years: number;
  hospital?: string;
  city?: string;
  state?: string;
  consultation_fee?: number;
  rating: number;
  total_reviews: number;
  bio?: string;
  is_unlocked: boolean;
  // Only present when unlocked
  phone?: string;
  email?: string;
  unlocked_at?: string;
}

export interface CreditPackage {
  id: number;
  name: string;
  description?: string;
  credits: number;
  bonus_credits: number;
  total_credits: number;
  price: number;
  price_per_credit: number;
  is_active: boolean;
  is_featured: boolean;
}

export interface Transaction {
  id: number;
  transaction_type: string;
  credits_delta: number;
  balance_after: number;
  description?: string;
  created_at: string;
}

export interface Payment {
  id: number;
  credit_package_id: number;
  amount: number;
  credits_purchased: number;
  bonus_credits: number;
  status: string; // pending | success | failed
  payment_mode: string;
  gateway_reference?: string;
  failure_reason?: string;
  created_at: string;
}

export interface DashboardStats {
  total_credits_purchased: number;
  total_credits_spent: number;
  current_balance: number;
  total_doctors_unlocked: number;
  total_payments: number;
  successful_payments: number;
  failed_payments: number;
  total_spent_amount: number;
}

export interface ActivityItem {
  id: number;
  activity_type: string;
  description: string;
  credits_delta: number;
  created_at: string;
}

export interface DashboardResponse {
  stats: DashboardStats;
  recent_activities: ActivityItem[];
  unlocked_doctor_ids: number[];
}

// Auth types — backend returns flat token response
export interface TokenResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  email: string;
  full_name: string;
  is_admin: boolean;
  credit_balance: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  phone?: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

export interface PurchaseRequest {
  package_id: number;
  payment_mode: 'success' | 'fail' | 'pending';
  idempotency_key: string;
}

export interface PurchaseResponse {
  payment_id: number;
  status: string;
  credits_added: number;
  bonus_credits: number;
  new_balance: number;
  message: string;
}

export interface UnlockResponse {
  doctor_id: number;
  already_unlocked: boolean;
  credits_spent: number;
  new_balance: number;
  message: string;
}

export interface DoctorListResponse {
  doctors: Doctor[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface CreditBalance {
  user_id: number;
  credit_balance: number;
}
