import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { creditService } from '../services/creditService';
import { PurchaseRequest } from '../types';

export function useCreditBalance() {
  return useQuery({
    queryKey: ['credit-balance'],
    queryFn: () => creditService.getBalance(),
    staleTime: 1000 * 30,
  });
}

export function useCreditPackages() {
  return useQuery({
    queryKey: ['credit-packages'],
    queryFn: () => creditService.getPackages(),
    staleTime: 1000 * 60 * 10,
  });
}

export function useCreditHistory(page = 1, perPage = 10) {
  return useQuery({
    queryKey: ['credit-history', page, perPage],
    queryFn: () => creditService.getHistory(page, perPage),
  });
}

export function usePurchaseCredits() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PurchaseRequest) => creditService.purchase(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['credit-balance'] });
      queryClient.invalidateQueries({ queryKey: ['credit-history'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
    },
  });
}
