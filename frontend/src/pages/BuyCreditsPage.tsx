import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { creditService } from '../services/creditService';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../contexts/ToastContext';
import { CreditPackage, PurchaseResponse } from '../types';
import { Star, Zap, CheckCircle2, AlertCircle, Info, CreditCard, Shield } from 'lucide-react';
const uuidv4 = () => Math.random().toString(36).substring(2) + Date.now().toString(36);

function PackageCard({
  pkg, selected, onSelect,
}: {
  pkg: CreditPackage; selected: boolean; onSelect: () => void;
}) {
  return (
    <div
      onClick={onSelect}
      className={`relative cursor-pointer rounded-xl border-2 p-5 transition-all ${
        selected ? 'border-blue-900 bg-blue-50 shadow-md' : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm'
      } ${pkg.is_featured ? 'ring-2 ring-blue-900 ring-offset-1' : ''}`}
    >
      {pkg.is_featured && (
        <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-900 text-white text-xs font-medium px-3 py-1 rounded-full flex items-center gap-1">
          <Star className="w-3 h-3 fill-white" /> Most Popular
        </span>
      )}
      <div className="mb-3">
        <h3 className="font-semibold text-slate-900">{pkg.name}</h3>
        {pkg.description && <p className="text-xs text-slate-500 mt-0.5">{pkg.description}</p>}
      </div>
      <div className="mb-3">
        <span className="text-3xl font-bold text-slate-900">₹{pkg.price}</span>
      </div>
      <div className="space-y-1.5 text-sm text-slate-600">
        <div className="flex items-center gap-2">
          <Zap className="w-3.5 h-3.5 text-blue-900" />
          <span>{pkg.credits.toLocaleString()} credits</span>
        </div>
        {pkg.bonus_credits > 0 && (
          <div className="flex items-center gap-2 text-emerald-600">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>+{pkg.bonus_credits} bonus credits</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-slate-400 text-xs">
          <span>= {pkg.total_credits.toLocaleString()} total · ₹{pkg.price_per_credit.toFixed(3)}/credit</span>
        </div>
      </div>
      {selected && (
        <div className="absolute top-3 right-3">
          <CheckCircle2 className="w-5 h-5 text-blue-900 fill-blue-100" />
        </div>
      )}
    </div>
  );
}

type PaymentMode = 'success' | 'fail' | 'pending';

export default function BuyCreditsPage() {
  const { user, refreshUser } = useAuth();
  const { addToast } = useToast();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const [selectedPkg, setSelectedPkg] = useState<CreditPackage | null>(null);
  const [paymentMode, setPaymentMode] = useState<PaymentMode>('success');
  const [showConfirm, setShowConfirm] = useState(false);
  const [purchasing, setPurchasing] = useState(false);
  const [lastResult, setLastResult] = useState<PurchaseResponse | null>(null);

  const { data: packages = [], isLoading } = useQuery({
    queryKey: ['packages'],
    queryFn: () => creditService.getPackages(),
  });

  const handlePurchase = async () => {
    if (!selectedPkg) return;
    setPurchasing(true);
    try {
      const result = await creditService.purchase({
        package_id: selectedPkg.id,
        payment_mode: paymentMode,
        idempotency_key: uuidv4(),
      });
      setLastResult(result);
      if (result.status === 'success') {
        await refreshUser();
        queryClient.invalidateQueries({ queryKey: ['dashboard'] });
        addToast(`${result.credits_added + result.bonus_credits} credits added to your account!`, 'success');
      } else if (result.status === 'failed') {
        addToast('Payment failed. No credits were added.', 'error');
      } else {
        addToast('Payment is pending. Credits will be added after confirmation.', 'info');
      }
      setShowConfirm(false);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Purchase failed.';
      addToast(msg, 'error');
    } finally {
      setPurchasing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Buy Credits</h1>
        <p className="text-sm text-slate-500 mt-1">
          Purchase credits to unlock detailed doctor profiles. Each profile costs {10} credits.
        </p>
      </div>

      {/* Current balance */}
      <div className="bg-blue-900 text-white rounded-xl p-5 flex items-center justify-between">
        <div>
          <p className="text-blue-200 text-sm">Current Balance</p>
          <p className="text-3xl font-bold">{user?.credit_balance ?? 0} <span className="text-lg font-normal">credits</span></p>
        </div>
        <CreditCard className="w-10 h-10 text-blue-400" />
      </div>

      {/* Demo payment disclaimer */}
      <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-4">
        <Info className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="text-sm text-amber-800">
          <strong>Demo Payment System</strong> — No real charges are made. This is a simulated payment gateway for
          demonstration purposes. Select a payment outcome below to test different scenarios.
        </div>
      </div>

      {/* Payment Mode selector */}
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <p className="text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
          <Shield className="w-4 h-4" /> Demo Payment Mode
        </p>
        <div className="flex gap-3">
          {([
            { value: 'success', label: '✅ Success', desc: 'Credits added immediately' },
            { value: 'fail', label: '❌ Failed', desc: 'No credits added (SC-002)' },
            { value: 'pending', label: '⏳ Pending', desc: 'Awaiting confirmation (SC-003)' },
          ] as { value: PaymentMode; label: string; desc: string }[]).map(m => (
            <button key={m.value} onClick={() => setPaymentMode(m.value)}
              className={`flex-1 text-center rounded-lg border py-2.5 px-3 text-sm transition-colors ${
                paymentMode === m.value ? 'border-blue-900 bg-blue-50 text-blue-900' : 'border-slate-200 text-slate-600 hover:border-slate-300'
              }`}>
              <div className="font-medium">{m.label}</div>
              <div className="text-xs mt-0.5 opacity-70">{m.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Packages */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1,2,3,4].map(i => (
            <div key={i} className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse h-40"></div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {packages.map(pkg => (
            <PackageCard key={pkg.id} pkg={pkg}
              selected={selectedPkg?.id === pkg.id}
              onSelect={() => setSelectedPkg(pkg)} />
          ))}
        </div>
      )}

      {/* Purchase button */}
      {selectedPkg && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 flex items-center justify-between">
          <div>
            <p className="font-medium text-slate-900">{selectedPkg.name} Package</p>
            <p className="text-sm text-slate-500">{selectedPkg.total_credits.toLocaleString()} total credits · ₹{selectedPkg.price}</p>
          </div>
          <button onClick={() => setShowConfirm(true)}
            className="bg-blue-900 text-white px-6 py-2.5 rounded-lg font-medium text-sm hover:bg-blue-800 transition-colors">
            Purchase Now
          </button>
        </div>
      )}

      {/* Last result */}
      {lastResult && (
        <div className={`rounded-xl border p-4 ${
          lastResult.status === 'success' ? 'bg-emerald-50 border-emerald-200' :
          lastResult.status === 'failed' ? 'bg-red-50 border-red-200' : 'bg-amber-50 border-amber-200'
        }`}>
          <div className="flex items-center gap-2 mb-1">
            {lastResult.status === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> :
             lastResult.status === 'failed' ? <AlertCircle className="w-4 h-4 text-red-600" /> :
             <Info className="w-4 h-4 text-amber-600" />}
            <span className="text-sm font-medium">
              {lastResult.status === 'success' ? 'Payment Successful' :
               lastResult.status === 'failed' ? 'Payment Failed' : 'Payment Pending'}
            </span>
          </div>
          <p className="text-sm text-slate-600">{lastResult.message}</p>
          {lastResult.status === 'success' && (
            <p className="text-sm font-medium text-emerald-700 mt-1">
              New balance: {lastResult.new_balance} credits
            </p>
          )}
        </div>
      )}

      {/* Confirm Modal */}
      {showConfirm && selectedPkg && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm">
            <h3 className="font-semibold text-slate-900 text-lg mb-4">Confirm Purchase</h3>
            <div className="bg-slate-50 rounded-lg p-4 space-y-2 text-sm mb-5">
              <div className="flex justify-between">
                <span className="text-slate-500">Package</span>
                <span className="font-medium">{selectedPkg.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Credits</span>
                <span className="font-medium">{selectedPkg.total_credits.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Amount</span>
                <span className="font-medium">₹{selectedPkg.price}</span>
              </div>
              <div className="flex justify-between text-xs border-t border-slate-200 pt-2">
                <span className="text-amber-600">Payment Mode</span>
                <span className="text-amber-700 font-medium">{paymentMode.toUpperCase()} (Demo)</span>
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={() => setShowConfirm(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm">
                Cancel
              </button>
              <button onClick={handlePurchase} disabled={purchasing}
                className="flex-1 bg-blue-900 text-white py-2.5 rounded-lg text-sm font-medium hover:bg-blue-800 disabled:opacity-60">
                {purchasing ? 'Processing…' : `Pay ₹${selectedPkg.price}`}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
