import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

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
  confidence: string | null;
  last_verified_at: string | null;
  start_date: string | null;
  end_date: string | null;
  detected_bonus_percentage: number | null;
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

export interface PartnerStoreOption {
  name: string;
  portal_name: string;
  program_name: string | null;
  base_rate: number;
  promo_rate: number | null;
  effective_rate: number;
  total_points: number;
  total_avios: number;
  supports_gift_card: boolean;
  supports_stacking: boolean;
  confidence: string | null;
  notes: string | null;
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
  partner_store_options: PartnerStoreOption[];
  stack_steps: string[];
  warnings: string[];
}

export interface StrategyResponse {
  category: string;
  amount: number;
  country: string;
  strategies: StrategyItem[];
}

export interface AwardRouteItem {
  id: number;
  route_name: string;
  origin: string;
  destination: string;
  cabin: string;
  program_name: string;
  operating_airlines: string | null;
  alliance: string | null;
  table_type: string | null;
  points_one_way: number | null;
  total_points: number | null;
  taxes_estimate: number | null;
  taxes_currency: string | null;
  baggage_included: boolean;
  change_policy: string | null;
  cancellation_policy: string | null;
  recommended_booking_window: string | null;
  notes: string | null;
}

export interface TransferRouteItem {
  id: number;
  source_program: string;
  target_program: string;
  base_ratio: number;
  typical_bonus_min: number | null;
  typical_bonus_max: number | null;
  current_bonus: number | null;
  effective_ratio: number;
  confidence: string | null;
  notes: string | null;
}

export interface TripMapResponse {
  origin: string;
  destination: string;
  passengers: number;
  cabin: string;
  routes: AwardRouteItem[];
  transfer_routes: TransferRouteItem[];
  decision_steps: string[];
  warnings: string[];
}

export interface LostMilesResponse {
  country: string;
  annual_spend: number;
  conservative_points: number;
  aggressive_points: number;
  conservative_avios: number;
  aggressive_avios: number;
  recommendations: string[];
}

export const plannerApi = {
  getStrategies: (data: { category: string; amount: number; country: string }) =>
    api.post<StrategyResponse>('/api/planner/strategies', data),
  getTripMap: (data: {
    origin: string;
    destination: string;
    passengers: number;
    cabin: string;
    country: string;
    flexibility: string;
  }) => api.post<TripMapResponse>('/api/planner/trip-map', data),
  getLostMiles: (data: {
    country: string;
    monthly_hotel: number;
    monthly_fuel: number;
    monthly_restaurants: number;
    monthly_supermarkets: number;
    monthly_travel: number;
    monthly_shopping: number;
    monthly_rideshare: number;
    monthly_utilities: number;
  }) => api.post<LostMilesResponse>('/api/planner/lost-miles', data),
  getPartnerStores: (country?: string, category?: string) =>
    api.get<PartnerStoreOption[]>('/api/planner/partner-stores', { params: { country, category } }),
  getTransferRoutes: (source_program?: string, target_program?: string) =>
    api.get<TransferRouteItem[]>('/api/planner/transfer-routes', { params: { source_program, target_program } }),
  getAwardRoutes: (origin?: string, destination?: string, cabin?: string) =>
    api.get<AwardRouteItem[]>('/api/planner/award-routes', { params: { origin, destination, cabin } }),
};

// Data export/import types
export interface SourceExport {
  name: string;
  source_type: string;
  country: string;
  url: string;
  website_url?: string | null;
  is_active: boolean;
  priority: number;
  description?: string | null;
  notes?: string | null;
}

export interface DataExport {
  version: number;
  exported_at: string;
  balances: { program_name: string; points: number; notes: string | null }[];
  enrolled_programs: string[];
  sources?: SourceExport[] | null;
  deactivated_sources?: string[] | null;
}

export interface ImportResult {
  balances_imported: number;
  balances_skipped: number;
  programs_enrolled: number;
  programs_not_found: string[];
  sources_added: number;
  sources_toggled: number;
}

export const dataApi = {
  export: () => api.get<DataExport>('/api/data/export'),
  import: (data: DataExport) => api.post<ImportResult>('/api/data/import', data),
};
