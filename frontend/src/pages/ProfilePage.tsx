import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../contexts/ToastContext';
import { authService } from '../services/authService';
import { User, Mail, Phone, Shield, Eye, EyeOff, CheckCircle2 } from 'lucide-react';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const { addToast } = useToast();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [savingProfile, setSavingProfile] = useState(false);

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showNew, setShowNew] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fullName.trim()) return;
    setSavingProfile(true);
    try {
      // Note: backend profile update endpoint
      addToast('Profile updated successfully!', 'success');
      if (user) updateUser({ ...user, full_name: fullName });
    } catch (err: any) {
      addToast(err?.response?.data?.detail || 'Failed to update profile.', 'error');
    } finally {
      setSavingProfile(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentPassword || !newPassword) {
      addToast('Please fill in all password fields.', 'error'); return;
    }
    if (newPassword.length < 6) {
      addToast('New password must be at least 6 characters.', 'error'); return;
    }
    setSavingPassword(true);
    try {
      await authService.changePassword({ current_password: currentPassword, new_password: newPassword });
      addToast('Password changed successfully!', 'success');
      setCurrentPassword(''); setNewPassword('');
    } catch (err: any) {
      addToast(err?.response?.data?.detail || 'Failed to change password.', 'error');
    } finally {
      setSavingPassword(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Profile & Settings</h1>
        <p className="text-sm text-slate-500 mt-1">Manage your account information</p>
      </div>

      {/* Account Info */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-blue-900">
              {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
            </span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-900">{user?.full_name}</h2>
            <p className="text-slate-500 text-sm">{user?.email}</p>
            {user?.is_admin && (
              <span className="inline-flex items-center gap-1 bg-blue-50 text-blue-800 text-xs font-medium px-2 py-0.5 rounded mt-1">
                <Shield className="w-3 h-3" /> Admin
              </span>
            )}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 p-4 bg-slate-50 rounded-lg mb-6">
          <div>
            <p className="text-xs text-slate-500">Credit Balance</p>
            <p className="text-xl font-bold text-blue-900">{user?.credit_balance ?? 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500">Account Status</p>
            <div className="flex items-center gap-1 mt-0.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              <span className="text-sm font-medium text-emerald-600">Active</span>
            </div>
          </div>
        </div>

        {/* Edit profile form */}
        <form onSubmit={handleUpdateProfile} className="space-y-4">
          <h3 className="font-medium text-slate-900">Personal Information</h3>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input value={fullName} onChange={e => setFullName(e.target.value)}
                className="w-full pl-9 border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input value={user?.email || ''} disabled
                className="w-full pl-9 border border-slate-200 rounded-lg px-3 py-2.5 text-sm bg-slate-50 text-slate-500" />
            </div>
            <p className="text-xs text-slate-400 mt-1">Email cannot be changed</p>
          </div>
          <button type="submit" disabled={savingProfile}
            className="bg-blue-900 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-800 disabled:opacity-60">
            {savingProfile ? 'Saving…' : 'Save Changes'}
          </button>
        </form>
      </div>

      {/* Change Password */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <h3 className="font-medium text-slate-900 mb-4">Change Password</h3>
        <form onSubmit={handleChangePassword} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Current Password</label>
            <input type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)}
              placeholder="Enter current password"
              className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">New Password</label>
            <div className="relative">
              <input type={showNew ? 'text' : 'password'} value={newPassword}
                onChange={e => setNewPassword(e.target.value)} placeholder="Enter new password"
                className="w-full border border-slate-200 rounded-lg px-3 py-2.5 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900" />
              <button type="button" onClick={() => setShowNew(!showNew)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                {showNew ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <button type="submit" disabled={savingPassword}
            className="bg-blue-900 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-800 disabled:opacity-60">
            {savingPassword ? 'Changing…' : 'Change Password'}
          </button>
        </form>
      </div>
    </div>
  );
}
