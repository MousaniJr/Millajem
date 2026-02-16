'use client';

import { useEffect, useState } from 'react';
import { recommendationsApi, CreditCard, EarningOpportunity } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

// Cadenas de conversión por país (estructuras permanentes del PDF)
const CONVERSION_CHAINS: Record<string, { steps: string[]; result: string; score: number }[]> = {
  ES: [
    { steps: ['Gasolina Cepsa', 'Cepsa Más', 'Iberia Club'], result: '2 Avios/litro', score: 90 },
    { steps: ['Gasolina Repsol', 'Waylet Travel Club', 'Viajes/catálogo'], result: 'Puntos Travel Club', score: 82 },
    { steps: ['Gasolina Repsol', 'Waylet + Más Renfe', 'Billetes AVE'], result: 'Puntos Renfe', score: 75 },
    { steps: ['Gasto diario', 'Amex Gold/Platinum ES', 'MR → Iberia/BA'], result: '1 Avios/€', score: 92 },
    { steps: ['Compras online', 'Iberia Plus Store', 'Iberia Club'], result: '2-10 Avios/€', score: 82 },
    { steps: ['Duty Free aeropuerto', 'Club Avolta', 'Iberia/BA'], result: '1 Avios/€', score: 80 },
    { steps: ['Vuelos Vueling/Iberia', 'Iberia Club', 'Canje MAD-GRU'], result: '~50.500 Avios ida biz', score: 95 },
  ],
  BR: [
    { steps: ['Gasolina Petrobras', 'Premmia', 'TudoAzul'], result: '2x en posto premiado', score: 82 },
    { steps: ['Gasolina Ipiranga', 'Km de Vantagens', 'LATAM Pass / TudoAzul'], result: '1 km/R$ + cashback', score: 78 },
    { steps: ['Gasolina Shell', 'Shell Box', 'Smiles / TudoAzul'], result: 'Pontos → millas', score: 75 },
    { steps: ['Tarjeta Santander BR', 'Esfera', 'Iberia Club'], result: '2 Esfera = 1 Avios ★', score: 95 },
    { steps: ['Tarjeta Itaú/Bradesco', 'Livelo', 'LATAM / Smiles / TudoAzul'], result: '1:1 con bonos 100%', score: 88 },
    { steps: ['Shopping Livelo/Iupp', 'Campañas 10x', 'Aerolíneas bonificadas'], result: 'Máxima acumulación', score: 88 },
  ],
  GI: [
    { steps: ['Gasolina BP', 'BPme Rewards', 'Avios BA/Iberia'], result: '1-2 pts/litro → Avios', score: 88 },
    { steps: ['Compras Tesco GIB', 'Clubcard Points', 'Partners Boost'], result: 'Descuentos/viajes', score: 72 },
    { steps: ['Tránsito Heathrow', 'Heathrow Rewards', 'Avios BA/Iberia'], result: '1 pto/£1 gastado', score: 80 },
    { steps: ['Vuelo BA GIB-LHR', 'BA Executive Club', 'Canje vuelos long-haul'], result: '7.250 Avios/vuelo', score: 85 },
    { steps: ['Gasto diario GIB', 'Amex España (pago en GIB)', 'MR → Avios (comisión FX ~2%)'], result: '1 Avios/€', score: 78 },
    { steps: ['Compras online UK', 'BA Avios eStore', 'BA Executive Club'], result: '2-10 Avios/£', score: 82 },
  ],
};

export default function Recommendations() {
  const [country, setCountry] = useState('ES');
  const [cards, setCards] = useState<CreditCard[]>([]);
  const [opportunities, setOpportunities] = useState<EarningOpportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [currencyFilter, setCurrencyFilter] = useState<string>('ALL');
  const [showChains, setShowChains] = useState(true);

  // Calculadora de gasto
  const [monthlySpend, setMonthlySpend] = useState({
    general: 2000,
    restaurants: 300,
    supermarkets: 400,
    travel: 200,
    fuel: 150,
  });

  useEffect(() => {
    loadData();
  }, [country]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [cardsRes, oppsRes] = await Promise.all([
        recommendationsApi.getCards(country),
        recommendationsApi.getOpportunities(country),
      ]);
      setCards(cardsRes.data);
      setOpportunities(oppsRes.data);
    } catch (err) {
      console.error('Error loading recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const calculateMonthlyEarnings = (card: CreditCard) => {
    const { general, restaurants, supermarkets, travel, fuel } = monthlySpend;

    let totalSpend = general;
    let totalPoints = general * card.base_earning_rate;

    // Añadir bonus si aplica
    if (card.bonus_categories) {
      try {
        const bonus = JSON.parse(card.bonus_categories);
        if (bonus.restaurants) {
          totalPoints += restaurants * bonus.restaurants;
          totalSpend += restaurants;
        }
        if (bonus.supermarkets) {
          totalPoints += supermarkets * bonus.supermarkets;
          totalSpend += supermarkets;
        }
        if (bonus.travel) {
          totalPoints += travel * bonus.travel;
          totalSpend += travel;
        }
      } catch (e) {
        // Ignore parsing errors
      }
    }

    const yearlyPoints = totalPoints * 12;
    const withWelcomeBonus = yearlyPoints + (card.welcome_bonus || 0);

    return {
      monthly: totalPoints,
      yearly: yearlyPoints,
      withBonus: withWelcomeBonus,
      totalSpend,
    };
  };

  const calculateOpportunityEarnings = (opp: EarningOpportunity) => {
    if (opp.category === 'fuel') {
      // Fuel en litros
      const liters = monthlySpend.fuel / 1.5; // Asumiendo 1.5 EUR/litro
      return liters * opp.earning_rate * 12;
    }
    return 0;
  };

  const getCategoryIcon = (category: string) => {
    const icons: Record<string, string> = {
      fuel: '⛽',
      flights: '✈️',
      rideshare: '🚗',
      shopping_portal: '🛍️',
      dining: '🍽️',
      hotels: '🏨',
      supermarket: '🛒',
      pharmacy: '💊',
      airport: '✈️',
      transport: '🚆',
    };
    return icons[category] || '📍';
  };

  // Monedas finales disponibles según las oportunidades cargadas
  const availableCurrencies = ['ALL', ...Array.from(
    new Set(opportunities.map(o => o.loyalty_program?.currency).filter(Boolean) as string[])
  )];

  const filteredOpportunities = currencyFilter === 'ALL'
    ? opportunities
    : opportunities.filter(o => o.loyalty_program?.currency === currencyFilter);

  const getCurrencyLabel = (currency: string) => {
    const labels: Record<string, string> = {
      ALL: 'Todas',
      Avios: '✈️ Avios',
      'Milhas Smiles': '🟠 Smiles',
      'Milhas LATAM': '🔵 LATAM',
      'Pontos TudoAzul': '🔷 TudoAzul',
      'Pontos Livelo': '🟣 Livelo',
      'Pontos Iupp': '🟡 Iupp',
      'Pontos Premmia': '🟢 Premmia',
      Km: '🏁 Km Vantagens',
      'Puntos Renfe': '🚆 Renfe',
      'Puntos Travel Club': '🌍 Travel Club',
      RevPoints: '💜 RevPoints',
      'BPme Points': '🟩 BPme',
      'Nectar Points': '🟧 Nectar',
      'Clubcard Points': '🔴 Clubcard',
      'Heathrow Points': '🛬 Heathrow',
    };
    return labels[currency] || currency;
  };

  const getNetworkLogo = (network: string) => {
    const logos: Record<string, string> = {
      Amex: '🟦',
      Visa: '🔷',
      Mastercard: '🔴',
    };
    return logos[network] || '💳';
  };

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        {/* Header */}
        <div>
        <h2 className="text-3xl font-bold text-gray-900">Recomendaciones</h2>
        <p className="mt-2 text-sm text-gray-600">
          Tarjetas y estrategias para maximizar tus puntos y Avios
        </p>
      </div>

        {/* Country Selector */}
        <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">País</label>
        <div className="flex gap-2">
          <button
            onClick={() => setCountry('ES')}
            className={`flex-1 px-4 py-2 rounded-md text-sm font-medium ${
              country === 'ES'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🇪🇸 España
          </button>
          <button
            onClick={() => setCountry('BR')}
            className={`flex-1 px-4 py-2 rounded-md text-sm font-medium ${
              country === 'BR'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🇧🇷 Brasil
          </button>
          <button
            onClick={() => setCountry('GI')}
            className={`flex-1 px-4 py-2 rounded-md text-sm font-medium ${
              country === 'GI'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🇬🇮 Gibraltar
          </button>
        </div>
      </div>

        {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary-600 border-r-transparent"></div>
          <p className="mt-2 text-gray-600">Cargando recomendaciones...</p>
        </div>
      ) : (
        <>
          {/* Credit Cards */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Tarjetas Recomendadas</h3>
            <div className="space-y-4">
              {cards.map((card) => {
                const earnings = calculateMonthlyEarnings(card);
                const isTopPick = card.recommendation_score >= 90;

                return (
                  <div
                    key={card.id}
                    className={`bg-white rounded-lg shadow p-6 ${
                      isTopPick ? 'ring-2 ring-green-500' : ''
                    }`}
                  >
                    {isTopPick && (
                      <div className="mb-3">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ⭐ MEJOR OPCIÓN
                        </span>
                      </div>
                    )}

                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl">{getNetworkLogo(card.card_network)}</span>
                          <h4 className="text-lg font-bold text-gray-900">{card.name}</h4>
                        </div>

                        <p className="text-sm text-gray-600 mb-3">{card.bank}</p>

                        {/* Earning Rate */}
                        <div className="grid grid-cols-2 gap-4 mb-3">
                          <div>
                            <p className="text-xs text-gray-500">Earning Rate</p>
                            <p className="text-sm font-semibold text-gray-900">
                              {card.base_earning_rate} {card.loyalty_program?.currency || 'pts'} /{' '}
                              {card.currency}
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Cuota Anual</p>
                            <p className="text-sm font-semibold text-gray-900">
                              {card.annual_fee} {card.currency}
                              {card.first_year_fee !== null &&
                                card.first_year_fee !== card.annual_fee && (
                                  <span className="text-xs text-green-600 ml-1">
                                    ({card.first_year_fee} primer año)
                                  </span>
                                )}
                            </p>
                          </div>
                        </div>

                        {/* Welcome Bonus */}
                        {card.welcome_bonus && (
                          <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-3">
                            <p className="text-sm font-medium text-blue-900">
                              🎁 Bonus Bienvenida: {card.welcome_bonus.toLocaleString()} puntos
                            </p>
                            {card.welcome_bonus_requirement && (
                              <p className="text-xs text-blue-700 mt-1">
                                {card.welcome_bonus_requirement}
                              </p>
                            )}
                          </div>
                        )}

                        {/* Earnings Calculator */}
                        <div className="bg-gray-50 rounded-md p-3 mb-3">
                          <p className="text-xs text-gray-500 mb-1">
                            Con tu gasto mensual estimado:
                          </p>
                          <div className="grid grid-cols-3 gap-2 text-center">
                            <div>
                              <p className="text-xs text-gray-600">Mensual</p>
                              <p className="text-sm font-semibold text-gray-900">
                                {Math.round(earnings.monthly).toLocaleString()}
                              </p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-600">Anual</p>
                              <p className="text-sm font-semibold text-gray-900">
                                {Math.round(earnings.yearly).toLocaleString()}
                              </p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-600">+ Bienvenida</p>
                              <p className="text-sm font-semibold text-primary-600">
                                {Math.round(earnings.withBonus).toLocaleString()}
                              </p>
                            </div>
                          </div>
                        </div>

                        {/* Notes */}
                        {card.notes && (
                          <p className="text-xs text-gray-600 italic">{card.notes}</p>
                        )}

                        {/* Application Link */}
                        {card.application_url && (
                          <a
                            href={card.application_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block mt-3 text-sm text-primary-600 hover:text-primary-800 underline"
                          >
                            Solicitar tarjeta →
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Conversion Chains */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-900">
                🔗 Cadenas de Conversión
              </h3>
              <button
                onClick={() => setShowChains(!showChains)}
                className="text-sm text-primary-600 hover:text-primary-800"
              >
                {showChains ? 'Ocultar' : 'Mostrar'}
              </button>
            </div>
            {showChains && (
              <div className="space-y-2">
                {(CONVERSION_CHAINS[country] || []).map((chain, idx) => (
                  <div key={idx} className="bg-white rounded-lg shadow px-4 py-3 flex items-center gap-2 flex-wrap">
                    {chain.steps.map((step, si) => (
                      <span key={si} className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          si === 0 ? 'bg-gray-100 text-gray-700' :
                          si === chain.steps.length - 1 ? 'bg-primary-100 text-primary-800' :
                          'bg-blue-50 text-blue-700'
                        }`}>{step}</span>
                        {si < chain.steps.length - 1 && (
                          <span className="text-gray-400 text-xs">→</span>
                        )}
                      </span>
                    ))}
                    <span className="ml-auto text-xs font-semibold text-green-700 bg-green-50 px-2 py-1 rounded">
                      {chain.result}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Earning Opportunities */}
          {opportunities.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                <h3 className="text-xl font-bold text-gray-900">
                  Oportunidades para Ganar Puntos
                </h3>
              </div>

              {/* Currency Filter */}
              {availableCurrencies.length > 2 && (
                <div className="mb-4 flex flex-wrap gap-2">
                  <span className="text-sm text-gray-500 self-center">Filtrar por moneda:</span>
                  {availableCurrencies.map((c) => (
                    <button
                      key={c}
                      onClick={() => setCurrencyFilter(c)}
                      className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                        currencyFilter === c
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {getCurrencyLabel(c)}
                    </button>
                  ))}
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredOpportunities.map((opp) => (
                  <div key={opp.id} className={`bg-white rounded-lg shadow p-5 ${
                    opp.recommendation_score >= 85 ? 'ring-1 ring-green-300' : ''
                  }`}>
                    <div className="flex items-start gap-3">
                      <span className="text-3xl">{getCategoryIcon(opp.category)}</span>
                      <div className="flex-1">
                        <div className="flex items-start justify-between gap-2 mb-1">
                          <h4 className="font-semibold text-gray-900">{opp.name}</h4>
                          {opp.loyalty_program?.currency && (
                            <span className="shrink-0 text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">
                              {opp.loyalty_program.currency}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-primary-600 font-medium mb-2">
                          {opp.earning_description}
                        </p>
                        <p className="text-xs text-gray-600 mb-2">{opp.how_to_use}</p>
                        {opp.notes && (
                          <p className="text-xs text-gray-500 italic">{opp.notes}</p>
                        )}
                        {opp.signup_url && (
                          <a
                            href={opp.signup_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block mt-2 text-xs text-primary-600 hover:text-primary-800 underline"
                          >
                            Más info →
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Spending Calculator */}
          <div className="bg-gradient-to-br from-blue-50 to-primary-50 rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              🧮 Calculadora de Gasto Mensual
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Ajusta tu gasto mensual para ver cuántos puntos ganarías con cada tarjeta
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Gasto General ({country === 'ES' ? 'EUR' : country === 'BR' ? 'BRL' : 'GBP'})
                </label>
                <input
                  type="number"
                  value={monthlySpend.general}
                  onChange={(e) =>
                    setMonthlySpend({ ...monthlySpend, general: parseInt(e.target.value) || 0 })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Restaurantes</label>
                <input
                  type="number"
                  value={monthlySpend.restaurants}
                  onChange={(e) =>
                    setMonthlySpend({
                      ...monthlySpend,
                      restaurants: parseInt(e.target.value) || 0,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Supermercados</label>
                <input
                  type="number"
                  value={monthlySpend.supermarkets}
                  onChange={(e) =>
                    setMonthlySpend({
                      ...monthlySpend,
                      supermarkets: parseInt(e.target.value) || 0,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Combustible</label>
                <input
                  type="number"
                  value={monthlySpend.fuel}
                  onChange={(e) =>
                    setMonthlySpend({ ...monthlySpend, fuel: parseInt(e.target.value) || 0 })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
