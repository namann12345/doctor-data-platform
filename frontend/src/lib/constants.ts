export const API_URL = '/api';
export const CREDIT_COST_PER_PROFILE = 10;
export const TOKEN_KEY = 'auth_token';
export const USER_KEY = 'auth_user';

export const SPECIALTIES = [
  'Cardiology',
  'Dermatology',
  'Endocrinology',
  'Gastroenterology',
  'General Medicine',
  'Neurology',
  'Oncology',
  'Ophthalmology',
  'Orthopedics',
  'Pediatrics',
  'Psychiatry',
  'Pulmonology',
  'Rheumatology',
  'Urology',
];

export const CITIES = [
  'Mumbai',
  'Delhi',
  'Bangalore',
  'Chennai',
  'Kolkata',
  'Hyderabad',
  'Pune',
  'Ahmedabad',
  'Jaipur',
  'Lucknow',
];

export const SORT_OPTIONS = [
  { value: 'rating_desc', label: 'Rating (High to Low)' },
  { value: 'experience_desc', label: 'Experience (High to Low)' },
  { value: 'name_asc', label: 'Name (A-Z)' },
];

export const TRANSACTION_TYPES = [
  { value: '', label: 'All Types' },
  { value: 'credit_purchase', label: 'Credit Purchase' },
  { value: 'doctor_unlock', label: 'Doctor Unlock' },
  { value: 'refund', label: 'Refund' },
];

export const TRANSACTION_STATUSES = [
  { value: '', label: 'All Statuses' },
  { value: 'success', label: 'Success' },
  { value: 'failed', label: 'Failed' },
  { value: 'pending', label: 'Pending' },
];
