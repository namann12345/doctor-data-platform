import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Search,
  CreditCard,
  Receipt,
  User,
  Settings,
  Coins,
  ChevronRight,
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/doctors', icon: Search, label: 'Find Doctors' },
  { to: '/credits', icon: CreditCard, label: 'Buy Credits' },
  { to: '/transactions', icon: Receipt, label: 'Transactions' },
  { to: '/profile', icon: User, label: 'Profile' },
];

export function Sidebar() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <aside className="w-64 bg-blue-900 text-white flex flex-col h-screen sticky top-0">
      {/* Logo */}
      <div className="p-6 border-b border-blue-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
            <span className="text-blue-900 font-bold text-sm">D</span>
          </div>
          <div>
            <p className="font-bold text-sm">Doctor Data</p>
            <p className="text-blue-300 text-xs">Platform</p>
          </div>
        </div>
      </div>

      {/* Credit Balance */}
      <div className="mx-4 my-4 bg-blue-800 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-1">
          <Coins className="w-4 h-4 text-yellow-400" />
          <span className="text-xs text-blue-300 font-medium">Credit Balance</span>
        </div>
        <p className="text-2xl font-bold">{user?.credit_balance ?? 0}</p>
        <button
          onClick={() => navigate('/credits')}
          className="mt-2 text-xs text-blue-300 hover:text-white flex items-center gap-1 transition-colors"
        >
          Buy more credits <ChevronRight className="w-3 h-3" />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-2">
        <ul className="space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <li key={to}>
              <NavLink
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'text-blue-200 hover:bg-white/10 hover:text-white'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                {label}
              </NavLink>
            </li>
          ))}
          {user?.is_admin && (
            <li>
              <NavLink
                to="/admin"
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'text-blue-200 hover:bg-white/10 hover:text-white'
                  }`
                }
              >
                <Settings className="w-5 h-5" />
                Admin
              </NavLink>
            </li>
          )}
        </ul>
      </nav>

      {/* User info */}
      <div className="p-4 border-t border-blue-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-700 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium">{user?.full_name?.charAt(0).toUpperCase()}</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.full_name}</p>
            <p className="text-xs text-blue-300 truncate">{user?.email}</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
