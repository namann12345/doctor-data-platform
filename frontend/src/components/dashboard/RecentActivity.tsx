import { ActivityItem } from '../../types';
import { format } from 'date-fns';
import { Coins, Lock, RefreshCw } from 'lucide-react';

interface RecentActivityProps {
  items: ActivityItem[];
}

function ActivityIcon({ type }: { type: string }) {
  if (type === 'credit_purchase' || type === 'purchase') return <Coins className="w-4 h-4 text-green-600" />;
  if (type === 'doctor_unlock' || type === 'unlock') return <Lock className="w-4 h-4 text-blue-600" />;
  return <RefreshCw className="w-4 h-4 text-gray-600" />;
}

function ActivityIconBg(type: string) {
  if (type === 'credit_purchase' || type === 'purchase') return 'bg-green-50';
  if (type === 'doctor_unlock' || type === 'unlock') return 'bg-blue-50';
  return 'bg-gray-50';
}

export function RecentActivity({ items }: RecentActivityProps) {
  if (!items || items.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">
        No recent activity
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <div key={item.id} className="flex items-center gap-3">
          <div className={`w-9 h-9 rounded-lg ${ActivityIconBg(item.activity_type)} flex items-center justify-center flex-shrink-0`}>
            <ActivityIcon type={item.activity_type} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {item.description || item.activity_type.replace(/_/g, ' ')}
            </p>
            <p className="text-xs text-gray-500">
              {format(new Date(item.created_at), 'MMM d, yyyy')}
            </p>
          </div>
          <div className="flex flex-col items-end gap-1">
            {item.credits_delta !== 0 && (
              <span className={`text-sm font-semibold ${item.credits_delta > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {item.credits_delta > 0 ? '+' : ''}{item.credits_delta} cr
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
