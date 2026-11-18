import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { ActivityItem } from '../../types';
import { format } from 'date-fns';

interface CreditChartProps {
  activities: ActivityItem[];
  initialBalance?: number;
}

export function CreditChart({ activities, initialBalance = 0 }: CreditChartProps) {
  // Build balance history from activities (most recent last)
  const sorted = [...activities].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );

  let balance = initialBalance;
  // Reverse-compute starting balance
  for (const a of sorted) balance -= a.credits_delta;

  const data = sorted.map((a) => {
    balance += a.credits_delta;
    return {
      date: format(new Date(a.created_at), 'MMM d'),
      balance,
    };
  });

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Credit Balance History</h3>
        <div className="h-48 flex items-center justify-center text-gray-400 text-sm">
          No activity yet — purchase credits to see your balance chart.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <h3 className="font-semibold text-slate-900 mb-4">Credit Balance History</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            axisLine={false}
            tickLine={false}
            width={40}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Line
            type="monotone"
            dataKey="balance"
            stroke="#1E3A8A"
            strokeWidth={2}
            dot={{ fill: '#1E3A8A', r: 4 }}
            activeDot={{ r: 6 }}
            name="Credits"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
