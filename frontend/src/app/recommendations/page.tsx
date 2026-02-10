'use client';

import { useEffect, useState } from 'react';
import { recommendationsApi, CreditCard, EarningOpportunity } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Recommendations() {
  const [country, setCountry] = useState('ES');
  const [cards, setCards] = useState<CreditCard[]>([]);
  const [opportunities, setOpportunities] = useState<EarningOpportunity[]>([]);
  const [loading, setLoading] = useState(true);

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
      rideshare: '🚗',
      shopping_portal: '🛍️',
      dining: '🍽️',
      hotels: '🏨',
      supermarket: '🛒',
      pharmacy: '💊',
    };
    return icons[category] || '📍';
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

          {/* Earning Opportunities */}
          {opportunities.length > 0 && (
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Oportunidades para Ganar Puntos
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {opportunities.map((opp) => (
                  <div key={opp.id} className="bg-white rounded-lg shadow p-5">
                    <div className="flex items-start gap-3">
                      <span className="text-3xl">{getCategoryIcon(opp.category)}</span>
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900 mb-1">{opp.name}</h4>
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
