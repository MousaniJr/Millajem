'use client';

import { useState } from 'react';
import { plannerApi, StrategyItem } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

const CATEGORIES = [
  { value: 'hotel', label: 'Hotel', icon: '🏨' },
  { value: 'fuel', label: 'Gasolina', icon: '⛽' },
  { value: 'restaurants', label: 'Restaurantes', icon: '🍽️' },
  { value: 'supermarkets', label: 'Supermercados', icon: '🛒' },
  { value: 'travel', label: 'Viajes / Vuelos', icon: '✈️' },
  { value: 'shopping', label: 'Compras Online', icon: '🛍️' },
  { value: 'rideshare', label: 'Transporte', icon: '🚗' },
];

const COUNTRIES = [
  { value: 'ES', label: 'España', flag: '🇪🇸' },
  { value: 'BR', label: 'Brasil', flag: '🇧🇷' },
  { value: 'GI', label: 'Gibraltar', flag: '🇬🇮' },
];

export default function Planner() {
  const [country, setCountry] = useState('ES');
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState<number>(100);
  const [strategies, setStrategies] = useState<StrategyItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [showSecondary, setShowSecondary] = useState(false);
  const [expandedInfo, setExpandedInfo] = useState<number | null>(null);

  const currencySymbol = country === 'BR' ? 'R$' : country === 'GI' ? '£' : '€';

  const search = async () => {
    if (!category || amount <= 0) return;
    try {
      setLoading(true);
      setShowSecondary(false);
      const res = await plannerApi.getStrategies({ category, amount, country });
      setStrategies(res.data.strategies);
      setSearched(true);
    } catch (err) {
      console.error('Error loading strategies:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderStrategyCard = (s: StrategyItem, index: number) => (
    <div
      key={`${s.rank}-${index}`}
      className={`bg-white rounded-lg shadow p-5 border-l-4 ${
        !s.is_avios_redeemable
          ? 'border-l-gray-300 opacity-80'
          : index === 0 && s.opportunity_earns_redeemable
          ? 'border-l-yellow-400'
          : index < 3 && s.opportunity_earns_redeemable
          ? 'border-l-primary-400'
          : 'border-l-gray-200'
      }`}
    >
      {/* Opportunity (step 1) */}
      <div className="flex items-center gap-2 mb-3">
        <span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-sm font-bold ${
          index === 0 && s.opportunity_earns_redeemable ? 'bg-yellow-100 text-yellow-800' :
          index < 3 && s.opportunity_earns_redeemable ? 'bg-primary-100 text-primary-800' :
          'bg-gray-100 text-gray-600'
        }`}>
          #{index + 1}
        </span>
        {!s.is_avios_redeemable && (
          <button
            onClick={() => setExpandedInfo(expandedInfo === s.rank ? null : s.rank)}
            className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs font-bold hover:bg-blue-200"
            title="Más información"
          >
            i
          </button>
        )}
      </div>

      {s.opportunity_name && (
        <div className="mb-3">
          <div className="flex items-start gap-2">
            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mt-0.5 shrink-0">1</span>
            <div>
              <span className="font-semibold text-gray-900">{s.opportunity_name}</span>
              {s.opportunity_earning_description && (
                <span className="text-gray-500 text-sm ml-1">— {s.opportunity_earning_description}</span>
              )}
              {s.opportunity_how_to_use && (
                <p className="text-gray-400 text-xs mt-0.5">{s.opportunity_how_to_use}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {!s.is_avios_redeemable && expandedInfo === s.rank && (
        <div className="text-xs text-gray-500 mb-3 bg-blue-50 rounded p-2">
          {s.earning_currency || 'Puntos'} — no canjeable directamente por Avios
        </div>
      )}

      {/* Payment options (step 2) */}
      <div className="space-y-1.5">
        <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          {s.opportunity_name ? 'Formas de pago' : 'Tarjetas disponibles'}
        </p>
        {s.payment_options.map((p, pi) => (
          <div
            key={pi}
            className={`flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 py-2 px-3 rounded-lg ${
              pi === 0 ? 'bg-primary-50 border border-primary-100' : 'bg-gray-50'
            }`}
          >
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-purple-100 text-purple-700 text-xs font-bold shrink-0">
                {s.opportunity_name ? String(pi + 2) : String(pi + 1)}
              </span>
              <div>
                <span className={`font-medium ${pi === 0 ? 'text-primary-800' : 'text-gray-700'} text-sm`}>
                  {p.card_name}
                </span>
                <span className="text-gray-400 text-xs ml-1">
                  ({p.card_bank}) — {p.card_earning_rate} pts/{currencySymbol}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-2 sm:ml-auto">
              <span className={`font-bold text-sm ${pi === 0 ? 'text-primary-700' : 'text-gray-600'}`}>
                {p.avios_per_euro} Avios/{currencySymbol}
              </span>
              <span className="text-xs text-gray-400">
                ({p.total_avios.toLocaleString()} total)
              </span>
              {p.programs_needed.length > 0 && (
                <span className="text-orange-500 text-xs" title={p.programs_needed.join(', ')}>
                  *
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Programs needed note */}
      {s.payment_options.some((p) => p.programs_needed.length > 0) && (
        <p className="text-orange-600 text-xs mt-2">
          * Requiere inscripción en programas indicados
        </p>
      )}
    </div>
  );

  const primary = strategies.filter((s) => s.opportunity_earns_redeemable);
  const secondary = strategies.filter((s) => !s.opportunity_earns_redeemable);

  return (
    <ProtectedRoute>
      <div className="max-w-6xl mx-auto p-4 sm:p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
              Planificador de Compras
            </h1>
            <p className="text-gray-600 mt-1">
              Encuentra la mejor estrategia para ganar más puntos en tus compras
            </p>
          </div>
          <a
            href="/planner/programs"
            className="mt-3 sm:mt-0 inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium"
          >
            Mis Programas Activos
          </a>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">País</label>
            <div className="flex gap-2">
              {COUNTRIES.map((c) => (
                <button
                  key={c.value}
                  onClick={() => setCountry(c.value)}
                  className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                    country === c.value
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {c.flag} {c.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Categoría de compra</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat.value}
                  onClick={() => setCategory(cat.value)}
                  className={`px-3 py-3 rounded-lg font-medium text-sm transition-colors text-center ${
                    category === cat.value
                      ? 'bg-primary-600 text-white ring-2 ring-primary-300'
                      : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                  }`}
                >
                  <span className="text-lg block mb-1">{cat.icon}</span>
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Importe ({currencySymbol})
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              min={1}
              className="w-full sm:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Ej: 200"
            />
          </div>

          <button
            onClick={search}
            disabled={!category || amount <= 0 || loading}
            className="w-full sm:w-auto px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Buscando...' : 'Buscar Estrategias'}
          </button>
        </div>

        {/* Results */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600 mx-auto"></div>
            <p className="text-gray-500 mt-3">Calculando estrategias...</p>
          </div>
        )}

        {searched && !loading && strategies.length === 0 && (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500 text-lg">No se encontraron estrategias para esta combinación.</p>
            <p className="text-gray-400 text-sm mt-2">Prueba con otra categoría o país.</p>
          </div>
        )}

        {!loading && strategies.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              {primary.length} estrategias con puntos canjeables para{' '}
              <span className="text-primary-600">{currencySymbol}{amount}</span> en{' '}
              <span className="text-primary-600">
                {CATEGORIES.find((c) => c.value === category)?.label}
              </span>
            </h2>

            <div className="space-y-4">
              {primary.map((s, i) => renderStrategyCard(s, i))}
            </div>

            {secondary.length > 0 && (
              <div className="mt-6">
                <button
                  onClick={() => setShowSecondary(!showSecondary)}
                  className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 font-medium"
                >
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-gray-600 text-xs font-bold">
                    {showSecondary ? '−' : '+'}
                  </span>
                  {showSecondary ? 'Ocultar' : 'Mostrar'} {secondary.length} ofertas con saldo/descuentos
                </button>

                {showSecondary && (
                  <div className="space-y-3 mt-3">
                    {secondary.map((s, i) => renderStrategyCard(s, i))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
