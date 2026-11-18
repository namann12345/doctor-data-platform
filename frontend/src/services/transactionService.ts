import api from '../lib/api';

export const transactionService = {
  async getTransactions(params?: { skip?: number; limit?: number; transaction_type?: string }) {
    const response = await api.get('/transactions', { params });
    return response.data;
  },

  async getPayments(params?: { skip?: number; limit?: number }) {
    const response = await api.get('/transactions/payments', { params });
    return response.data;
  },

  async getDashboard() {
    const response = await api.get('/dashboard');
    return response.data;
  },
};
