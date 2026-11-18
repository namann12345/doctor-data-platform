import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { doctorService } from '../services/doctorService';

export interface DoctorSearchParams {
  specialty?: string;
  city?: string;
  state?: string;
  min_experience?: number;
  max_fee?: number;
  search?: string;
  page?: number;
  page_size?: number;
}

export function useDoctors(params: DoctorSearchParams) {
  return useQuery({
    queryKey: ['doctors', params],
    queryFn: () => doctorService.search(params),
    staleTime: 1000 * 60 * 2,
  });
}

export function useDoctor(id: number) {
  return useQuery({
    queryKey: ['doctor', id],
    queryFn: () => doctorService.getDoctor(id),
    enabled: !!id,
  });
}

export function useUnlockDoctor() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => doctorService.unlockDoctor(id),
    onSuccess: (_data, id) => {
      queryClient.invalidateQueries({ queryKey: ['doctor', id] });
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['credit-balance'] });
    },
  });
}
