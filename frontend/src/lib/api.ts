import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface LoyaltyProgram {
  id: number;
  name: string;
  currency: string;
  country: string;
  category: string;
  avios_ratio: number | null;
  website_url: string | null;
  login_url: string | null;
  is_enrolled: boolean;
  notes: string | null;
}

export interface Balance {
  id: number;
  program_id: number;
  points: number;
  last_updated: string;
  notes: string | null;
  program: LoyaltyProgram;
}

export interface ConversionResult {
  program_name: string;
  program_currency: string;
  input_points: number;
  avios_ratio: number | null;
  avios_output: number | null;
  convertible: boolean;
  message: string;
}

// API functions
export const programsApi = {
  getAll: (enrolled?: boolean) =>
    api.get<LoyaltyProgram[]>('/api/programs/', { params: enrolled !== undefined ? { enrolled } : {} }),
  getById: (id: number) => api.get<LoyaltyProgram>(`/api/programs/${id}`),
  create: (data: {
    name: string;
    currency: string;
    country: string;
    category: string;
    avios_ratio?: number;
    website_url?: string;
    login_url?: string;
    notes?: string;
  }) => api.post<LoyaltyProgram>('/api/programs/', data),
  toggleEnrollment: (id: number) =>
    api.patch<LoyaltyProgram>(`/api/programs/${id}/toggle-enrollment`),
};

export const balancesApi = {
  getAll: () => api.get<Balance[]>('/api/balances/'),
  getById: (id: number) => api.get<Balance>(`/api/balances/${id}`),
  create: (data: { program_id: number; points: number; notes?: string }) =>
    api.post<Balance>('/api/balances/', data),
  update: (id: number, data: { points: number; notes?: string }) =>
    api.put<Balance>(`/api/balances/${id}`, data),
  delete: (id: number) => api.delete(`/api/balances/${id}`),
};

export const calculatorApi = {
  toAvios: (program_id: number, points: number) =>
    api.post<ConversionResult>('/api/calculator/to-avios', { program_id, points }),
  allToAvios: (points: number) =>
    api.get<ConversionResult[]>(`/api/calculator/all-to-avios/${points}`),
};

export interface Alert {
  id: number;
  title: string;
  message: string;
  alert_type: string;
  priority: string;
  source_url: string | null;
  source_type: string;
  source_name: string | null;
  related_program: string | null;
  country: string | null;
  full_content: string | null;
  is_read: boolean;
  is_favorite: boolean;
  created_at: string;
}

export const alertsApi = {
  getAll: (params?: {
    unread_only?: boolean;
    favorites_only?: boolean;
    country?: string;
    alert_type?: string;
    source_type?: string;
    source_name?: string;
    related_program?: string;
    priority?: string;
    order_by?: string;
  }) => api.get<Alert[]>('/api/alerts/', { params }),
  getById: (id: number) => api.get<Alert>(`/api/alerts/${id}`),
  markAsRead: (id: number) => api.patch(`/api/alerts/${id}/read`),
  toggleFavorite: (id: number) => api.patch(`/api/alerts/${id}/favorite`),
  delete: (id: number) => api.delete(`/api/alerts/${id}`),
  getStats: () => api.get('/api/alerts/stats/summary'),
};

export const promotionsApi = {
  scan: (min_relevance?: number) =>
    api.post('/api/promotions/scan', null, { params: { min_relevance } }),
  getTop: (limit?: number, country?: string) =>
    api.get('/api/promotions/top', { params: { limit, country } }),
  listFeeds: () => api.get('/api/promotions/feeds'),
  getSocialAccounts: (country?: string) =>
    api.get('/api/promotions/social-accounts', { params: { country } }),
};

export interface CreditCard {
  id: number;
  name: string;
  bank: string;
  country: string;
  card_network: string;
  base_earning_rate: number;
  bonus_categories: string | null;
  annual_fee: number;
  currency: string;
  first_year_fee: number | null;
  welcome_bonus: number | null;
  welcome_bonus_requirement: string | null;
  minimum_income: number | null;
  is_available: boolean;
  application_url: string | null;
  image_url: string | null;
  notes: string | null;
  recommendation_score: number;
  loyalty_program: LoyaltyProgram | null;
}

export interface EarningOpportunity {
  id: number;
  name: string;
  category: string;
  country: string;
  earning_rate: number;
  earning_description: string;
  how_to_use: string;
  requirements: string | null;
  signup_url: string | null;
  more_info_url: string | null;
  is_active: boolean;
  notes: string | null;
  recommendation_score: number;
  loyalty_program: LoyaltyProgram | null;
}

export const recommendationsApi = {
  getCards: (country?: string, min_score?: number) =>
    api.get<CreditCard[]>('/api/recommendations/cards', { params: { country, min_score } }),
  getCard: (id: number) => api.get<CreditCard>(`/api/recommendations/cards/${id}`),
  getOpportunities: (country?: string, category?: string, min_score?: number) =>
    api.get<EarningOpportunity[]>('/api/recommendations/opportunities', {
      params: { country, category, min_score },
    }),
  getTopCards: (country: string, limit?: number) =>
    api.get(`/api/recommendations/top-cards/${country}`, { params: { limit } }),
  getStrategy: (country: string) => api.get(`/api/recommendations/strategy/${country}`),
};

// Planner types
export interface PaymentOption {
  card_name: string;
  card_bank: string;
  card_points: number;
  card_earning_rate: number;
  card_program_name: string | null;
  total_avios: number;
  avios_per_euro: number;
  programs_needed: string[];
}

export interface StrategyItem {
  rank: number;
  opportunity_name: string | null;
  opportunity_earning_description: string | null;
  opportunity_points: number;
  opportunity_how_to_use: string | null;
  opportunity_program_name: string | null;
  is_avios_redeemable: boolean;
  opportunity_earns_redeemable: boolean;
  earning_currency: string | null;
  payment_options: PaymentOption[];
  best_avios_per_euro: number;
  best_total_avios: number;
}

export interface StrategyResponse {
  category: string;
  amount: number;
  country: string;
  strategies: StrategyItem[];
}

export const plannerApi = {
  getStrategies: (data: { category: string; amount: number; country: string }) =>
    api.post<StrategyResponse>('/api/planner/strategies', data),
};

// Data export/import types
export interface DataExport {
  version: number;
  exported_at: string;
  balances: { program_name: string; points: number; notes: string | null }[];
  enrolled_programs: string[];
}

export interface ImportResult {
  balances_imported: number;
  balances_skipped: number;
  programs_enrolled: number;
  programs_not_found: string[];
}

export const dataApi = {
  export: () => api.get<DataExport>('/api/data/export'),
  import: (data: DataExport) => api.post<ImportResult>('/api/data/import', data),
};
