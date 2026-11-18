import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { doctorService } from '../services/doctorService';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../contexts/ToastContext';
import {
  ArrowLeft, Star, MapPin, Building2, Clock, GraduationCap, Phone, Mail,
  Lock, Unlock, AlertCircle, ShoppingCart, User, Languages
} from 'lucide-react';
import { CREDIT_COST_PER_PROFILE } from '../lib/constants';

export default function DoctorProfilePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();
  const { addToast } = useToast();
  const queryClient = useQueryClient();
  const [showConfirm, setShowConfirm] = useState(false);
  const [unlocking, setUnlocking] = useState(false);

  const { data: doctor, isLoading, refetch } = useQuery({
    queryKey: ['doctor', id],
    queryFn: () => doctorService.getDoctor(Number(id)),
    enabled: !!id,
  });

  const handleUnlock = async () => {
    if (!doctor) return;
    const balance = user?.credit_balance ?? 0;
    if (balance < CREDIT_COST_PER_PROFILE) {
      addToast(`Insufficient credits. You have ${balance} but need ${CREDIT_COST_PER_PROFILE}.`, 'error');
      navigate('/credits');
      return;
    }
    setUnlocking(true);
    try {
      const result = await doctorService.unlockDoctor(doctor.id);
      await refreshUser();
      await refetch();
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      if (result.already_unlocked) {
        addToast('Doctor profile is already unlocked.', 'info');
      } else {
        addToast(`Dr. ${doctor.name} unlocked! ${result.credits_spent} credits used.`, 'success');
      }
      setShowConfirm(false);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to unlock profile.';
      if (err?.response?.status === 402) {
        addToast(`Insufficient credits. ${msg}`, 'error');
        navigate('/credits');
      } else {
        addToast(msg, 'error');
      }
    } finally {
      setUnlocking(false);
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto space-y-4 animate-pulse">
        <div className="h-6 bg-slate-200 rounded w-32"></div>
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <div className="h-8 bg-slate-200 rounded w-64 mb-2"></div>
          <div className="h-4 bg-slate-200 rounded w-40 mb-6"></div>
          <div className="space-y-3">
            {[1,2,3,4].map(i => <div key={i} className="h-4 bg-slate-100 rounded w-3/4"></div>)}
          </div>
        </div>
      </div>
    );
  }

  if (!doctor) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-500">Doctor not found.</p>
        <button onClick={() => navigate('/doctors')} className="mt-4 text-blue-900 underline">
          Back to search
        </button>
      </div>
    );
  }

  const balance = user?.credit_balance ?? 0;
  const hasEnoughCredits = balance >= CREDIT_COST_PER_PROFILE;

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <button onClick={() => navigate('/doctors')}
        className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700">
        <ArrowLeft className="w-4 h-4" /> Back to Search
      </button>

      {/* Main card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">{doctor.name}</h1>
            <span className="inline-block bg-blue-50 text-blue-800 font-medium text-sm px-3 py-1 rounded-lg mt-1">
              {doctor.specialty}
            </span>
          </div>
          <div className="flex items-center gap-1 bg-amber-50 px-2 py-1 rounded-lg">
            <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
            <span className="text-sm font-medium text-amber-800">{doctor.rating.toFixed(1)}</span>
            <span className="text-xs text-amber-600">({doctor.total_reviews})</span>
          </div>
        </div>

        {/* Basic info – always visible */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {doctor.city && (
            <div className="flex items-center gap-2 text-slate-600">
              <MapPin className="w-4 h-4 text-slate-400" />
              <span className="text-sm">{doctor.city}{doctor.state ? `, ${doctor.state}` : ''}</span>
            </div>
          )}
          {doctor.hospital && (
            <div className="flex items-center gap-2 text-slate-600">
              <Building2 className="w-4 h-4 text-slate-400" />
              <span className="text-sm">{doctor.hospital}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-slate-600">
            <Clock className="w-4 h-4 text-slate-400" />
            <span className="text-sm">{doctor.experience_years} years experience</span>
          </div>
          {doctor.qualification && (
            <div className="flex items-center gap-2 text-slate-600">
              <GraduationCap className="w-4 h-4 text-slate-400" />
              <span className="text-sm">{doctor.qualification}</span>
            </div>
          )}
        </div>

        {/* Bio – always visible */}
        {doctor.bio && (
          <div className="bg-slate-50 rounded-lg p-4 mb-6">
            <p className="text-sm text-slate-600 leading-relaxed">{doctor.bio}</p>
          </div>
        )}

        {/* UNLOCK SECTION */}
        {!doctor.is_unlocked ? (
          <div className="border-2 border-dashed border-slate-200 rounded-xl p-6 text-center">
            <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Lock className="w-6 h-6 text-slate-400" />
            </div>
            <h3 className="font-semibold text-slate-900 mb-1">Contact Information Locked</h3>
            <p className="text-sm text-slate-500 mb-4">
              Unlock this profile to view phone number, email address, and consultation fees.
            </p>

            {!hasEnoughCredits && (
              <div className="flex items-center gap-2 bg-red-50 border border-red-100 rounded-lg px-4 py-3 mb-4 text-sm text-red-700">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>
                  Insufficient credits. You have <strong>{balance}</strong> but need <strong>{CREDIT_COST_PER_PROFILE}</strong>.
                </span>
              </div>
            )}

            <div className="flex items-center justify-center gap-3">
              <div className="text-sm text-slate-500">
                Your balance: <strong className="text-slate-900">{balance} credits</strong>
              </div>
              {hasEnoughCredits ? (
                <button onClick={() => setShowConfirm(true)}
                  className="flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-800 transition-colors">
                  <Unlock className="w-4 h-4" />
                  Unlock for {CREDIT_COST_PER_PROFILE} credits
                </button>
              ) : (
                <button onClick={() => navigate('/credits')}
                  className="flex items-center gap-2 bg-teal-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors">
                  <ShoppingCart className="w-4 h-4" />
                  Buy Credits
                </button>
              )}
            </div>
          </div>
        ) : (
          /* UNLOCKED PROFILE */
          <div className="border border-emerald-200 bg-emerald-50 rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Unlock className="w-4 h-4 text-emerald-600" />
              <span className="text-sm font-medium text-emerald-700">Profile Unlocked</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {doctor.phone && (
                <div className="flex items-center gap-3 bg-white rounded-lg p-3">
                  <Phone className="w-4 h-4 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-500">Phone</p>
                    <p className="text-sm font-medium text-slate-900">{doctor.phone}</p>
                  </div>
                </div>
              )}
              {doctor.email && (
                <div className="flex items-center gap-3 bg-white rounded-lg p-3">
                  <Mail className="w-4 h-4 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-500">Email</p>
                    <p className="text-sm font-medium text-slate-900">{doctor.email}</p>
                  </div>
                </div>
              )}
              {doctor.consultation_fee && (
                <div className="flex items-center gap-3 bg-white rounded-lg p-3">
                  <User className="w-4 h-4 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-500">Consultation Fee</p>
                    <p className="text-sm font-medium text-slate-900">₹{doctor.consultation_fee}</p>
                  </div>
                </div>
              )}
            </div>
            <p className="text-xs text-slate-400 mt-3">
              ⚕️ Fictional demo data only — not real contact information
            </p>
          </div>
        )}
      </div>

      {/* Confirmation Modal */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm">
            <h3 className="font-semibold text-slate-900 text-lg mb-2">Confirm Unlock</h3>
            <p className="text-sm text-slate-600 mb-4">
              You are about to unlock <strong>{doctor.name}</strong>'s full profile.
            </p>
            <div className="bg-slate-50 rounded-lg p-3 mb-5 space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Cost</span>
                <span className="font-medium text-slate-900">{CREDIT_COST_PER_PROFILE} credits</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Your balance</span>
                <span className="font-medium text-slate-900">{balance} credits</span>
              </div>
              <div className="flex justify-between border-t border-slate-200 pt-1 mt-1">
                <span className="text-slate-500">After unlock</span>
                <span className="font-medium text-slate-900">{balance - CREDIT_COST_PER_PROFILE} credits</span>
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={() => setShowConfirm(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm hover:bg-slate-50">
                Cancel
              </button>
              <button onClick={handleUnlock} disabled={unlocking}
                className="flex-1 bg-blue-900 text-white py-2.5 rounded-lg text-sm font-medium hover:bg-blue-800 disabled:opacity-60">
                {unlocking ? 'Unlocking…' : `Unlock (${CREDIT_COST_PER_PROFILE} credits)`}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
