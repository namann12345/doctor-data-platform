import api from '../lib/api';
import { Doctor, DoctorListResponse, UnlockResponse } from '../types';

export const doctorService = {
  async search(params: {
    specialty?: string;
    city?: string;
    state?: string;
    min_experience?: number;
    max_fee?: number;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<DoctorListResponse> {
    // Remove undefined values
    const cleanParams: Record<string, string | number> = {};
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') cleanParams[k] = v;
    });
    const response = await api.get<DoctorListResponse>('/doctors', { params: cleanParams });
    return response.data;
  },

  async getDoctor(id: number): Promise<Doctor> {
    const response = await api.get<Doctor>(`/doctors/${id}`);
    return response.data;
  },

  async unlockDoctor(doctorId: number): Promise<UnlockResponse> {
    const response = await api.post<UnlockResponse>('/credits/unlock', { doctor_id: doctorId });
    return response.data;
  },

  async getSpecialties(): Promise<string[]> {
    // Extract from search results
    return [];
  },
};
