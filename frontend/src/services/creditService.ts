import api from '../lib/api';
import { CreditPackage, CreditBalance, PurchaseRequest, PurchaseResponse } from '../types';

export const creditService = {
  async getPackages(): Promise<CreditPackage[]> {
    const response = await api.get<CreditPackage[]>('/credits/packages');
    return response.data;
  },

  async getBalance(): Promise<CreditBalance> {
    const response = await api.get<CreditBalance>('/credits/balance');
    return response.data;
  },

  async purchase(data: PurchaseRequest): Promise<PurchaseResponse> {
    const response = await api.post<PurchaseResponse>('/credits/purchase', data);
    return response.data;
  },

  async getLedger(params?: { skip?: number; limit?: number }) {
    const response = await api.get('/credits/ledger', { params });
    return response.data;
  },

  async getHistory(page = 1, perPage = 10) {
    const skip = (page - 1) * perPage;
    const response = await api.get('/credits/ledger', { params: { skip, limit: perPage } });
    return response.data;
  },
};
