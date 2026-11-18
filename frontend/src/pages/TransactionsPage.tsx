import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { transactionService } from '../services/transactionService';
import { Transaction } from '../types';
import { CreditCard, TrendingUp, TrendingDown, ChevronLeft, ChevronRight, Filter } from 'lucide-react';
import { format } from 'date-fns';

function TransactionRow({ txn }: { txn: Transaction }) {
  const isCredit = txn.credits_delta > 0;
  return (
    <tr className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
      <td className="py-3 px-4 text-sm text-slate-500">{txn.id}</td>
      <td className="py-3 px-4">
        <div className="flex items-center gap-2">
          <div className={`w-7 h-7 rounded-full flex items-center justify-center ${
            isCredit ? 'bg-emerald-50' : 'bg-blue-50'
          }`}>
            {isCredit
              ? <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
              : <TrendingDown className="w-3.5 h-3.5 text-blue-600" />}
          </div>
          <span className="text-sm font-medium text-slate-700 capitalize">
            {txn.transaction_type.replace('_', ' ')}
          </span>
        </div>
      </td>
      <td className="py-3 px-4 text-sm text-slate-600 max-w-xs truncate">{txn.description || '—'}</td>
      <td className={`py-3 px-4 text-sm font-semibold text-right ${
        isCredit ? 'text-emerald-600' : 'text-red-500'
      }`}>
        {isCredit ? '+' : ''}{txn.credits_delta}
      </td>
      <td className="py-3 px-4 text-sm text-slate-600 text-right">{txn.balance_after}</td>
      <td className="py-3 px-4 text-sm text-slate-400 text-right">
        {txn.created_at ? format(new Date(txn.created_at), 'dd MMM yyyy, HH:mm') : '—'}
      </td>
    </tr>
  );
}

export default function TransactionsPage() {
  const [page, setPage] = useState(0);
  const [typeFilter, setTypeFilter] = useState('');
  const pageSize = 20;

  const { data, isLoading } = useQuery({
    queryKey: ['transactions', page, typeFilter],
    queryFn: () => transactionService.getTransactions({
      skip: page * pageSize,
      limit: pageSize,
      ...(typeFilter && { transaction_type: typeFilter }),
    }),
  });

  const totalPages = data ? Math.ceil(data.total / pageSize) : 1;
  const currentPage = page + 1;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Transactions</h1>
          <p className="text-sm text-slate-500 mt-1">Your complete credit activity history</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 flex items-center gap-3">
        <Filter className="w-4 h-4 text-slate-400" />
        <select value={typeFilter} onChange={e => { setTypeFilter(e.target.value); setPage(0); }}
          className="border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900 bg-white">
          <option value="">All Types</option>
          <option value="credit_purchase">Credit Purchases</option>
          <option value="doctor_unlock">Doctor Unlocks</option>
          <option value="refund">Refunds</option>
        </select>
        {typeFilter && (
          <button onClick={() => { setTypeFilter(''); setPage(0); }}
            className="text-sm text-slate-500 hover:text-slate-700">Clear</button>
        )}
        <div className="ml-auto text-sm text-slate-500">
          {data?.total ?? 0} transactions
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center">
            <div className="animate-spin h-8 w-8 border-b-2 border-blue-900 rounded-full mx-auto"></div>
          </div>
        ) : !data?.transactions?.length ? (
          <div className="p-16 text-center">
            <CreditCard className="w-12 h-12 text-slate-200 mx-auto mb-4" />
            <p className="text-slate-500 font-medium">No transactions yet</p>
            <p className="text-sm text-slate-400 mt-1">Your credit activity will appear here</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="py-3 px-4 text-left text-xs font-medium text-slate-500 uppercase tracking-wide">ID</th>
                  <th className="py-3 px-4 text-left text-xs font-medium text-slate-500 uppercase tracking-wide">Type</th>
                  <th className="py-3 px-4 text-left text-xs font-medium text-slate-500 uppercase tracking-wide">Description</th>
                  <th className="py-3 px-4 text-right text-xs font-medium text-slate-500 uppercase tracking-wide">Credits</th>
                  <th className="py-3 px-4 text-right text-xs font-medium text-slate-500 uppercase tracking-wide">Balance</th>
                  <th className="py-3 px-4 text-right text-xs font-medium text-slate-500 uppercase tracking-wide">Date</th>
                </tr>
              </thead>
              <tbody>
                {data.transactions.map((txn: Transaction) => (
                  <TransactionRow key={txn.id} txn={txn} />
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="border-t border-slate-100 p-4 flex items-center justify-between">
            <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
              className="flex items-center gap-1 text-sm text-slate-600 disabled:opacity-40">
              <ChevronLeft className="w-4 h-4" /> Previous
            </button>
            <span className="text-sm text-slate-500">Page {currentPage} of {totalPages}</span>
            <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={currentPage === totalPages}
              className="flex items-center gap-1 text-sm text-slate-600 disabled:opacity-40">
              Next <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
