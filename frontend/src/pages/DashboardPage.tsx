import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { transactionService } from '../services/transactionService';
import { StatsCard } from '../components/dashboard/StatsCard';
import { RecentActivity } from '../components/dashboard/RecentActivity';
import { CreditChart } from '../components/dashboard/CreditChart';
import { CreditCard, TrendingUp, Unlock, ArrowRight, ShoppingCart, Search } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const { data: dashboard, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => transactionService.getDashboard(),
  });

  const stats = dashboard?.stats;
  const activities = dashboard?.recent_activities ?? [];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1,2,3,4].map(i => (
            <div key={i} className="bg-white rounded-xl border border-slate-200 p-6 animate-pulse">
              <div className="h-4 bg-slate-200 rounded w-24 mb-3"></div>
              <div className="h-8 bg-slate-200 rounded w-16"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">
          Welcome back, {user?.full_name?.split(' ')[0] || 'User'} 👋
        </h1>
        <p className="text-slate-500 text-sm mt-1">Here's what's happening with your account</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          label="Credit Balance"
          value={`${stats?.current_balance ?? user?.credit_balance ?? 0} credits`}
          icon={<CreditCard className="w-5 h-5 text-blue-700" />}
          iconBg="bg-blue-100"
        />
        <StatsCard
          label="Credits Purchased"
          value={stats?.total_credits_purchased ?? 0}
          icon={<TrendingUp className="w-5 h-5 text-green-700" />}
          iconBg="bg-green-100"
        />
        <StatsCard
          label="Credits Used"
          value={stats?.total_credits_spent ?? 0}
          icon={<ShoppingCart className="w-5 h-5 text-orange-700" />}
          iconBg="bg-orange-100"
        />
        <StatsCard
          label="Doctors Unlocked"
          value={stats?.total_doctors_unlocked ?? 0}
          icon={<Unlock className="w-5 h-5 text-purple-700" />}
          iconBg="bg-purple-100"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button onClick={() => navigate('/doctors')}
          className="flex items-center gap-4 bg-white rounded-xl border border-slate-200 p-5 hover:border-blue-900 hover:shadow-sm transition-all group text-left">
          <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100">
            <Search className="w-5 h-5 text-blue-900" />
          </div>
          <div className="flex-1">
            <p className="font-medium text-slate-900 text-sm">Find Doctors</p>
            <p className="text-xs text-slate-500">Search & filter</p>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-900" />
        </button>
        <button onClick={() => navigate('/credits')}
          className="flex items-center gap-4 bg-white rounded-xl border border-slate-200 p-5 hover:border-blue-900 hover:shadow-sm transition-all group text-left">
          <div className="w-10 h-10 bg-teal-50 rounded-lg flex items-center justify-center group-hover:bg-teal-100">
            <ShoppingCart className="w-5 h-5 text-teal-700" />
          </div>
          <div className="flex-1">
            <p className="font-medium text-slate-900 text-sm">Buy Credits</p>
            <p className="text-xs text-slate-500">From ₹99</p>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-teal-700" />
        </button>
        <button onClick={() => navigate('/transactions')}
          className="flex items-center gap-4 bg-white rounded-xl border border-slate-200 p-5 hover:border-blue-900 hover:shadow-sm transition-all group text-left">
          <div className="w-10 h-10 bg-slate-50 rounded-lg flex items-center justify-center group-hover:bg-slate-100">
            <CreditCard className="w-5 h-5 text-slate-700" />
          </div>
          <div className="flex-1">
            <p className="font-medium text-slate-900 text-sm">Transactions</p>
            <p className="text-xs text-slate-500">View history</p>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-slate-700" />
        </button>
      </div>

      {/* Chart + Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <CreditChart activities={activities} initialBalance={stats?.current_balance ?? user?.credit_balance ?? 0} />
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Recent Activity</h3>
          <RecentActivity items={activities} />
        </div>
      </div>
    </div>
  );
}
