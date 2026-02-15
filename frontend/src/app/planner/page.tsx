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
  const [expandedInfo, setExpandedInfo] = useState<number | null>(null);

  const currencySymbol = country === 'BR' ? 'R$' : country === 'GI' ? '£' : '€';

  const search = async () => {
    if (!category || amount <= 0) return;
    try {
      setLoading(true);
      const res = await plannerApi.getStrategies({ category, amount, country });
      setStrategies(res.data.strategies);
      setSearched(true);
    } catch (err) {
      console.error('Error loading strategies:', err);
    } finally {
      setLoading(false);
    }
  };

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
          {/* Country Selector */}
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

          {/* Category Selector */}
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

          {/* Amount Input */}
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
              placeholder={`Ej: 200`}
            />
          </div>

          {/* Search Button */}
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
            <p className="text-gray-400 text-sm mt-2">
              Prueba con otra categoría o país.
            </p>
          </div>
        )}

        {!loading && strategies.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              {strategies.length} estrategias encontradas para{' '}
              <span className="text-primary-600">{currencySymbol}{amount}</span> en{' '}
              <span className="text-primary-600">
                {CATEGORIES.find((c) => c.value === category)?.label}
              </span>
            </h2>

            <div className="space-y-4">
              {strategies.map((s) => (
                <div
                  key={s.rank}
                  className={`bg-white rounded-lg shadow p-5 border-l-4 ${
                    !s.is_avios_redeemable
                      ? 'border-l-gray-300 opacity-80'
                      : s.rank === 1
                      ? 'border-l-yellow-400'
                      : s.rank <= 3
                      ? 'border-l-primary-400'
                      : 'border-l-gray-200'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                    {/* Left: Strategy Details */}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-sm font-bold ${
                          s.rank === 1 ? 'bg-yellow-100 text-yellow-800' :
                          s.rank <= 3 ? 'bg-primary-100 text-primary-800' :
                          'bg-gray-100 text-gray-600'
                        }`}>
                          #{s.rank}
                        </span>
                        {!s.all_enrolled && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                            Requiere inscripción
                          </span>
                        )}
                        {s.all_enrolled && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Activo
                          </span>
                        )}
                      </div>

                      {/* Steps */}
                      <div className="space-y-2">
                        {s.opportunity_name && (
                          <div className="flex items-start gap-2">
                            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mt-0.5">1</span>
                            <div>
                              <span className="font-medium text-gray-900">{s.opportunity_name}</span>
                              {s.opportunity_earning_description && (
                                <span className="text-gray-500 text-sm ml-1">— {s.opportunity_earning_description}</span>
                              )}
                              {s.opportunity_how_to_use && (
                                <p className="text-gray-400 text-xs mt-0.5">{s.opportunity_how_to_use}</p>
                              )}
                            </div>
                          </div>
                        )}
                        {s.card_name && (
                          <div className="flex items-start gap-2">
                            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-purple-100 text-purple-700 text-xs font-bold mt-0.5">
                              {s.opportunity_name ? '2' : '1'}
                            </span>
                            <div>
                              <span className="font-medium text-gray-900">Pagar con {s.card_name}</span>
                              <span className="text-gray-500 text-sm ml-1">
                                ({s.card_bank}) — {s.card_earning_rate} pts/{currencySymbol}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Non-enrolled programs warning */}
                      {s.programs_needed.length > 0 && (
                        <p className="text-orange-600 text-xs mt-2">
                          Necesitas inscribirte en: {s.programs_needed.join(', ')}
                        </p>
                      )}
                    </div>

                    {/* Right: Points Summary */}
                    <div className="sm:text-right sm:min-w-[180px] bg-gray-50 rounded-lg p-3">
                      {s.is_avios_redeemable ? (
                        <>
                          <div className="text-2xl font-bold text-primary-700">
                            {s.avios_per_euro} <span className="text-sm font-normal text-gray-500">Avios/{currencySymbol}</span>
                          </div>
                          <div className="text-sm text-gray-600 mt-1">
                            {s.avios_equivalent.toLocaleString()} Avios totales
                          </div>
                          {s.opportunity_points > 0 && s.card_points > 0 && (
                            <div className="text-xs text-gray-400 mt-1">
                              {s.opportunity_points.toLocaleString()} (plataforma) + {s.card_points.toLocaleString()} (tarjeta)
                            </div>
                          )}
                        </>
                      ) : (
                        <>
                          <div className="flex items-center sm:justify-end gap-1">
                            <span className="text-lg font-bold text-gray-600">
                              {s.total_points.toLocaleString()} pts
                            </span>
                            <button
                              onClick={() => setExpandedInfo(expandedInfo === s.rank ? null : s.rank)}
                              className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs font-bold hover:bg-blue-200 transition-colors"
                              title="Más información"
                            >
                              i
                            </button>
                          </div>
                          {expandedInfo === s.rank && (
                            <div className="text-xs text-gray-500 mt-2 bg-blue-50 rounded p-2 text-left">
                              {s.earning_currency || 'Puntos'} — no canjeable directamente por Avios
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
