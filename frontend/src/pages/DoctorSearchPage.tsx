import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { doctorService } from '../services/doctorService';
import { Doctor } from '../types';
import { Search, Filter, X, Star, MapPin, Building2, Clock, Lock, ChevronLeft, ChevronRight } from 'lucide-react';
import { SPECIALTIES, CITIES } from '../lib/constants';

function DoctorCard({ doctor, onView }: { doctor: Doctor; onView: (id: number) => void }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-sm hover:border-slate-300 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-900 truncate">{doctor.name}</h3>
          <span className="inline-block bg-blue-50 text-blue-800 text-xs font-medium px-2 py-0.5 rounded mt-1">
            {doctor.specialty}
          </span>
        </div>
        {doctor.is_unlocked && (
          <span className="text-xs bg-emerald-50 text-emerald-700 font-medium px-2 py-0.5 rounded">Unlocked</span>
        )}
      </div>
      <div className="space-y-1.5 text-sm text-slate-500 mb-4">
        {doctor.city && (
          <div className="flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5" />
            <span>{doctor.city}{doctor.state ? `, ${doctor.state}` : ''}</span>
          </div>
        )}
        {doctor.hospital && (
          <div className="flex items-center gap-1.5">
            <Building2 className="w-3.5 h-3.5" />
            <span className="truncate">{doctor.hospital}</span>
          </div>
        )}
        <div className="flex items-center gap-1.5">
          <Clock className="w-3.5 h-3.5" />
          <span>{doctor.experience_years} years experience</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
          <span>{doctor.rating.toFixed(1)} ({doctor.total_reviews} reviews)</span>
        </div>
      </div>
      <button
        onClick={() => onView(doctor.id)}
        className="w-full flex items-center justify-center gap-2 bg-blue-900 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-800 transition-colors"
      >
        {doctor.is_unlocked ? 'View Profile' : (
          <><Lock className="w-3.5 h-3.5" /> View Details · 10 credits</>
        )}
      </button>
    </div>
  );
}

export default function DoctorSearchPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [city, setCity] = useState('');
  const [minExperience, setMinExperience] = useState('');
  const [page, setPage] = useState(1);

  // Debounce search
  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(search), 400);
    return () => clearTimeout(t);
  }, [search]);

  // Reset page when filters change
  useEffect(() => { setPage(1); }, [debouncedSearch, specialty, city, minExperience]);

  const params = {
    ...(debouncedSearch && { search: debouncedSearch }),
    ...(specialty && { specialty }),
    ...(city && { city }),
    ...(minExperience && { min_experience: parseInt(minExperience) }),
    page,
    page_size: 12,
  };

  const { data, isLoading, isFetching } = useQuery({
    queryKey: ['doctors', params],
    queryFn: () => doctorService.search(params),
  });

  const hasFilters = !!(debouncedSearch || specialty || city || minExperience);

  const clearFilters = () => {
    setSearch(''); setSpecialty(''); setCity(''); setMinExperience(''); setPage(1);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Find Doctors</h1>
        <p className="text-sm text-slate-500 mt-1">Search from our database of verified medical professionals</p>
      </div>

      {/* Search + Filters */}
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              value={search} onChange={e => setSearch(e.target.value)}
              placeholder="Search by name, specialty, hospital…"
              className="w-full pl-9 pr-4 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-900"
            />
          </div>
          <select value={specialty} onChange={e => setSpecialty(e.target.value)}
            className="border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900 bg-white">
            <option value="">All Specialties</option>
            {SPECIALTIES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          <select value={city} onChange={e => setCity(e.target.value)}
            className="border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900 bg-white">
            <option value="">All Cities</option>
            {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={minExperience} onChange={e => setMinExperience(e.target.value)}
            className="border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-900 bg-white">
            <option value="">Any Experience</option>
            <option value="5">5+ years</option>
            <option value="10">10+ years</option>
            <option value="15">15+ years</option>
            <option value="20">20+ years</option>
          </select>
          {hasFilters && (
            <button onClick={clearFilters}
              className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700 border border-slate-200 rounded-lg px-3 py-2.5">
              <X className="w-4 h-4" /> Clear
            </button>
          )}
        </div>
      </div>

      {/* Results info */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">
          {isLoading ? 'Searching…' : `${data?.total ?? 0} doctors found`}
        </p>
        {isFetching && !isLoading && (
          <span className="text-xs text-blue-600 animate-pulse">Updating…</span>
        )}
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 9 }).map((_, i) => (
            <div key={i} className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse">
              <div className="h-4 bg-slate-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-slate-200 rounded w-1/2 mb-4"></div>
              <div className="space-y-2 mb-4">
                {[1,2,3].map(j => <div key={j} className="h-3 bg-slate-100 rounded w-2/3"></div>)}
              </div>
              <div className="h-9 bg-slate-200 rounded-lg"></div>
            </div>
          ))}
        </div>
      ) : data?.doctors.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-slate-200">
          <Search className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">No doctors found</h3>
          <p className="text-slate-500 text-sm mb-4">
            {hasFilters ? 'Try adjusting your search filters.' : 'No doctors available.'}
          </p>
          {hasFilters && (
            <button onClick={clearFilters}
              className="bg-blue-900 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-800">
              Clear Filters
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data?.doctors.map(doc => (
            <DoctorCard key={doc.id} doctor={doc} onView={id => navigate(`/doctors/${id}`)} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {data && data.total_pages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
            className="p-2 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-40">
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-sm text-slate-600">Page {page} of {data.total_pages}</span>
          <button onClick={() => setPage(p => Math.min(data.total_pages, p + 1))} disabled={page === data.total_pages}
            className="p-2 rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-40">
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}

      <p className="text-xs text-center text-slate-400">
        ⚕️ All doctor profiles are fictional demo data for assessment purposes only
      </p>
    </div>
  );
}
