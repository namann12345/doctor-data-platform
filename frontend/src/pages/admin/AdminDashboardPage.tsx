import { useQuery } from '@tanstack/react-query';
import { transactionService } from '../../services/transactionService';
import { Users, CreditCard, TrendingUp, Stethoscope } from 'lucide-react';

export default function AdminDashboardPage() {
  const { data: dashboard, isLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const { default: api } = await import('../../lib/api');
      const r = await api.get('/admin/stats');
      return r.data;
    },
  });

  if (isLoading) {
    return <div className="animate-pulse space-y-4">
      <div className="h-8 bg-slate-200 rounded w-48"></div>
      <div className="grid grid-cols-4 gap-4">
        {[1,2,3,4].map(i => <div key={i} className="h-24 bg-slate-200 rounded-xl"></div>)}
      </div>
    </div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Admin Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">Platform-wide statistics and management</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Users', value: dashboard?.total_users ?? 0, icon: <Users className="w-5 h-5 text-blue-900" />, bg: 'bg-blue-50' },
          { label: 'Total Doctors', value: dashboard?.total_doctors ?? 0, icon: <Stethoscope className="w-5 h-5 text-teal-700" />, bg: 'bg-teal-50' },
          { label: 'Credits Sold', value: dashboard?.total_credits_sold ?? 0, icon: <CreditCard className="w-5 h-5 text-purple-700" />, bg: 'bg-purple-50' },
          { label: 'Total Revenue', value: `₹${(dashboard?.total_revenue ?? 0).toFixed(0)}`, icon: <TrendingUp className="w-5 h-5 text-emerald-700" />, bg: 'bg-emerald-50' },
        ].map(s => (
          <div key={s.label} className="bg-white rounded-xl border border-slate-200 p-5">
            <div className={`w-10 h-10 ${s.bg} rounded-lg flex items-center justify-center mb-3`}>
              {s.icon}
            </div>
            <p className="text-2xl font-bold text-slate-900">{s.value}</p>
            <p className="text-sm text-slate-500 mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {dashboard?.top_specialties?.length > 0 && (
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="font-medium text-slate-900 mb-3">Top Specialties</h3>
            <div className="space-y-2">
              {dashboard.top_specialties.map((s: { specialty: string; count: number }) => (
                <div key={s.specialty} className="flex items-center justify-between text-sm">
                  <span className="text-slate-600">{s.specialty}</span>
                  <span className="font-medium text-slate-900">{s.count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        {dashboard?.top_cities?.length > 0 && (
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="font-medium text-slate-900 mb-3">Top Cities</h3>
            <div className="space-y-2">
              {dashboard.top_cities.map((c: { city: string; count: number }) => (
                <div key={c.city} className="flex items-center justify-between text-sm">
                  <span className="text-slate-600">{c.city}</span>
                  <span className="font-medium text-slate-900">{c.count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
