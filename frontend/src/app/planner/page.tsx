'use client';

import { useState } from 'react';
import {
  LostMilesResponse,
  StrategyItem,
  TripMapResponse,
  plannerApi,
} from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

const CATEGORIES = [
  { value: 'hotel', label: 'Hotel' },
  { value: 'fuel', label: 'Gasolina' },
  { value: 'restaurants', label: 'Restaurantes' },
  { value: 'supermarkets', label: 'Supermercados' },
  { value: 'travel', label: 'Viajes' },
  { value: 'shopping', label: 'Compras online' },
  { value: 'gift_cards', label: 'Gift cards' },
  { value: 'utilities', label: 'Cuentas' },
  { value: 'rideshare', label: 'Transporte' },
];

const COUNTRIES = [
  { value: 'ES', label: 'España' },
  { value: 'BR', label: 'Brasil' },
  { value: 'GI', label: 'Gibraltar' },
];

const CURRENCY: Record<string, string> = {
  ES: 'EUR',
  BR: 'BRL',
  GI: 'GBP',
};

const CURRENCY_SYMBOL: Record<string, string> = {
  ES: '€',
  BR: 'R$',
  GI: '£',
};

export default function Planner() {
  const [tab, setTab] = useState<'purchase' | 'trip' | 'lost'>('purchase');
  const [country, setCountry] = useState('ES');
  const [category, setCategory] = useState('shopping');
  const [amount, setAmount] = useState(100);
  const [strategies, setStrategies] = useState<StrategyItem[]>([]);
  const [trip, setTrip] = useState({
    origin: 'MAD',
    destination: 'GRU',
    passengers: 1,
    cabin: 'business',
    flexibility: 'medium',
  });
  const [tripMap, setTripMap] = useState<TripMapResponse | null>(null);
  const [spend, setSpend] = useState({
    monthly_hotel: 100,
    monthly_fuel: 150,
    monthly_restaurants: 250,
    monthly_supermarkets: 450,
    monthly_travel: 150,
    monthly_shopping: 250,
    monthly_rideshare: 50,
    monthly_utilities: 200,
  });
  const [lostMiles, setLostMiles] = useState<LostMilesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const currencySymbol = CURRENCY_SYMBOL[country];

  const searchStrategies = async () => {
    setLoading(true);
    try {
      const res = await plannerApi.getStrategies({ country, category, amount });
      setStrategies(res.data.strategies);
      setSearched(true);
    } finally {
      setLoading(false);
    }
  };

  const searchTrip = async () => {
    setLoading(true);
    try {
      const res = await plannerApi.getTripMap({ ...trip, country });
      setTripMap(res.data);
    } finally {
      setLoading(false);
    }
  };

  const calculateLostMiles = async () => {
    setLoading(true);
    try {
      const res = await plannerApi.getLostMiles({ country, ...spend });
      setLostMiles(res.data);
    } finally {
      setLoading(false);
    }
  };

  const renderStrategy = (strategy: StrategyItem) => (
    <div key={strategy.rank} className="bg-white rounded-lg shadow border border-gray-100 p-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-800">
              {strategy.rank}
            </span>
            <h3 className="text-lg font-semibold text-gray-900">
              {strategy.opportunity_name || 'Solo tarjeta'}
            </h3>
          </div>
          {strategy.opportunity_earning_description && (
            <p className="mt-2 text-sm text-gray-600">{strategy.opportunity_earning_description}</p>
          )}
          {strategy.opportunity_how_to_use && (
            <p className="mt-1 text-sm text-gray-500">{strategy.opportunity_how_to_use}</p>
          )}
        </div>
        <div className="text-left md:text-right">
          <p className="text-2xl font-bold text-primary-700">
            {strategy.best_total_avios.toLocaleString('es-ES')}
          </p>
          <p className="text-xs text-gray-500">
            {strategy.best_avios_per_euro} Avios/{currencySymbol}
          </p>
        </div>
      </div>

      {strategy.partner_store_options.length > 0 && (
        <div className="mt-4 rounded-md border border-blue-100 bg-blue-50 p-3">
          <p className="mb-2 text-xs font-semibold uppercase text-blue-900">Portales y tiendas a comparar</p>
          <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
            {strategy.partner_store_options.map((store) => (
              <div key={`${store.portal_name}-${store.name}`} className="rounded-md bg-white p-3 text-sm">
                <div className="flex justify-between gap-2">
                  <span className="font-medium text-gray-900">{store.name}</span>
                  <span className="font-semibold text-blue-700">{store.effective_rate}x</span>
                </div>
                <p className="text-xs text-gray-500">{store.portal_name}</p>
                <p className="mt-1 text-xs text-gray-600">
                  {store.supports_gift_card ? 'Gift card posible. ' : ''}
                  {store.supports_stacking ? 'Stacking posible.' : 'Sin stacking confirmado.'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {strategy.stack_steps.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-semibold uppercase text-gray-500">Secuencia recomendada</p>
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            {strategy.stack_steps.map((step, idx) => (
              <div key={step} className="rounded-md bg-gray-50 p-3 text-sm text-gray-700">
                <span className="mr-2 font-bold text-primary-700">{idx + 1}</span>
                {step}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 space-y-2">
        <p className="text-xs font-semibold uppercase text-gray-500">Mejores formas de pago</p>
        {strategy.payment_options.slice(0, 3).map((option) => (
          <div key={`${strategy.rank}-${option.card_name}`} className="flex flex-col justify-between gap-1 rounded-md bg-gray-50 px-3 py-2 text-sm md:flex-row md:items-center">
            <span className="font-medium text-gray-800">{option.card_name}</span>
            <span className="text-gray-600">
              {option.total_avios.toLocaleString('es-ES')} Avios · {option.card_earning_rate} pts/{currencySymbol}
            </span>
          </div>
        ))}
      </div>

      {strategy.warnings.length > 0 && (
        <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">
          {strategy.warnings.join(' ')}
        </div>
      )}
    </div>
  );

  return (
    <ProtectedRoute>
      <div className="mx-auto max-w-7xl space-y-6 p-4 sm:p-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Planificador</h1>
            <p className="mt-1 text-sm text-gray-600">
              Decide primero el viaje, luego la mejor cadena para acumular, transferir y emitir.
            </p>
          </div>
          <a href="/planner/programs" className="inline-flex rounded-md bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200">
            Mis programas activos
          </a>
        </div>

        <div className="flex flex-wrap gap-2">
          {[
            ['purchase', 'Compra y stacking'],
            ['trip', 'Viaje objetivo'],
            ['lost', 'Millas perdidas'],
          ].map(([key, label]) => (
            <button
              key={key}
              onClick={() => setTab(key as 'purchase' | 'trip' | 'lost')}
              className={`rounded-md px-4 py-2 text-sm font-medium ${tab === key ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 shadow hover:bg-gray-50'}`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="rounded-lg bg-white p-4 shadow">
          <label className="mb-2 block text-sm font-medium text-gray-700">Pais de gasto</label>
          <div className="flex flex-wrap gap-2">
            {COUNTRIES.map((item) => (
              <button
                key={item.value}
                onClick={() => setCountry(item.value)}
                className={`rounded-md px-4 py-2 text-sm font-medium ${country === item.value ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {tab === 'purchase' && (
          <>
            <div className="rounded-lg bg-white p-5 shadow">
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_220px]">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">Categoria</label>
                  <div className="grid grid-cols-2 gap-2 md:grid-cols-3 lg:grid-cols-5">
                    {CATEGORIES.map((cat) => (
                      <button
                        key={cat.value}
                        onClick={() => setCategory(cat.value)}
                        className={`rounded-md border px-3 py-2 text-sm font-medium ${category === cat.value ? 'border-primary-500 bg-primary-50 text-primary-800' : 'border-gray-200 bg-gray-50 text-gray-700 hover:bg-gray-100'}`}
                      >
                        {cat.label}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">Importe ({CURRENCY[country]})</label>
                  <input
                    type="number"
                    min={1}
                    value={amount}
                    onChange={(e) => setAmount(Number(e.target.value))}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary-500 focus:ring-2 focus:ring-primary-500"
                  />
                  <button
                    onClick={searchStrategies}
                    disabled={loading || amount <= 0}
                    className="mt-3 w-full rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:bg-gray-300"
                  >
                    {loading ? 'Calculando...' : 'Buscar estrategia'}
                  </button>
                </div>
              </div>
            </div>

            {searched && strategies.length === 0 && (
              <div className="rounded-lg bg-white p-8 text-center text-gray-500 shadow">
                No hay estrategias para esta combinacion.
              </div>
            )}
            <div className="space-y-4">{strategies.map(renderStrategy)}</div>
          </>
        )}

        {tab === 'trip' && (
          <>
            <div className="rounded-lg bg-white p-5 shadow">
              <div className="grid grid-cols-2 gap-4 lg:grid-cols-6">
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">Origen</label>
                  <input className="w-full rounded-md border border-gray-300 px-3 py-2" value={trip.origin} onChange={(e) => setTrip({ ...trip, origin: e.target.value.toUpperCase() })} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">Destino</label>
                  <input className="w-full rounded-md border border-gray-300 px-3 py-2" value={trip.destination} onChange={(e) => setTrip({ ...trip, destination: e.target.value.toUpperCase() })} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">Pasajeros</label>
                  <input type="number" min={1} className="w-full rounded-md border border-gray-300 px-3 py-2" value={trip.passengers} onChange={(e) => setTrip({ ...trip, passengers: Number(e.target.value) })} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">Cabina</label>
                  <select className="w-full rounded-md border border-gray-300 px-3 py-2" value={trip.cabin} onChange={(e) => setTrip({ ...trip, cabin: e.target.value })}>
                    <option value="economy">Economy</option>
                    <option value="business">Business</option>
                  </select>
                </div>
                <div className="lg:col-span-2">
                  <label className="mb-1 block text-sm font-medium text-gray-700">Flexibilidad</label>
                  <select className="w-full rounded-md border border-gray-300 px-3 py-2" value={trip.flexibility} onChange={(e) => setTrip({ ...trip, flexibility: e.target.value })}>
                    <option value="low">Fechas fijas</option>
                    <option value="medium">Algo flexible</option>
                    <option value="high">Muy flexible</option>
                  </select>
                </div>
              </div>
              <button onClick={searchTrip} disabled={loading} className="mt-4 rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:bg-gray-300">
                {loading ? 'Buscando...' : 'Crear mapa de emision'}
              </button>
            </div>

            {tripMap && (
              <div className="space-y-4">
                <div className="rounded-lg bg-white p-5 shadow">
                  <h2 className="text-lg font-semibold text-gray-900">Pasos de decision</h2>
                  <div className="mt-3 grid grid-cols-1 gap-2 md:grid-cols-4">
                    {tripMap.decision_steps.map((step, idx) => (
                      <div key={step} className="rounded-md bg-gray-50 p-3 text-sm text-gray-700">
                        <span className="font-bold text-primary-700">{idx + 1}. </span>{step}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                  {tripMap.routes.map((route) => (
                    <div key={route.id} className="rounded-lg bg-white p-5 shadow">
                      <div className="flex justify-between gap-3">
                        <div>
                          <h3 className="font-semibold text-gray-900">{route.route_name}</h3>
                          <p className="text-sm text-gray-500">{route.program_name} · {route.operating_airlines}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-primary-700">
                            {route.total_points ? route.total_points.toLocaleString('es-ES') : 'Variable'}
                          </p>
                          <p className="text-xs text-gray-500">puntos total</p>
                        </div>
                      </div>
                      <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                        <div className="rounded-md bg-gray-50 p-2">Tabla: {route.table_type || 'n/d'}</div>
                        <div className="rounded-md bg-gray-50 p-2">Equipaje: {route.baggage_included ? 'Incluido' : 'Verificar'}</div>
                        <div className="rounded-md bg-gray-50 p-2">Tasas: {route.taxes_estimate ? `${route.taxes_estimate} ${route.taxes_currency}` : 'Variable'}</div>
                        <div className="rounded-md bg-gray-50 p-2">Alianza: {route.alliance || 'n/d'}</div>
                      </div>
                      {route.recommended_booking_window && <p className="mt-3 text-sm text-gray-600">{route.recommended_booking_window}</p>}
                    </div>
                  ))}
                </div>

                {tripMap.transfer_routes.length > 0 && (
                  <div className="rounded-lg bg-white p-5 shadow">
                    <h2 className="text-lg font-semibold text-gray-900">Transferencias relevantes</h2>
                    <div className="mt-3 grid grid-cols-1 gap-2 md:grid-cols-2">
                      {tripMap.transfer_routes.map((route) => (
                        <div key={route.id} className="rounded-md border border-gray-100 p-3 text-sm">
                          <p className="font-medium text-gray-900">{route.source_program} → {route.target_program}</p>
                          <p className="text-gray-600">
                            Ratio efectivo: {route.effective_ratio}:1
                            {route.typical_bonus_max ? ` · bonus tipico hasta ${route.typical_bonus_max}%` : ''}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {tab === 'lost' && (
          <>
            <div className="rounded-lg bg-white p-5 shadow">
              <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                {Object.entries(spend).map(([key, value]) => (
                  <div key={key}>
                    <label className="mb-1 block text-sm font-medium capitalize text-gray-700">
                      {key.replace('monthly_', '').replace('_', ' ')} ({currencySymbol})
                    </label>
                    <input
                      type="number"
                      min={0}
                      value={value}
                      onChange={(e) => setSpend({ ...spend, [key]: Number(e.target.value) })}
                      className="w-full rounded-md border border-gray-300 px-3 py-2"
                    />
                  </div>
                ))}
              </div>
              <button onClick={calculateLostMiles} disabled={loading} className="mt-4 rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:bg-gray-300">
                {loading ? 'Calculando...' : 'Calcular millas perdidas'}
              </button>
            </div>

            {lostMiles && (
              <div className="rounded-lg bg-white p-5 shadow">
                <h2 className="text-lg font-semibold text-gray-900">Potencial anual</h2>
                <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                  <div className="rounded-md bg-gray-50 p-4">
                    <p className="text-sm text-gray-500">Gasto anual</p>
                    <p className="text-2xl font-bold text-gray-900">{lostMiles.annual_spend.toLocaleString('es-ES')} {CURRENCY[country]}</p>
                  </div>
                  <div className="rounded-md bg-blue-50 p-4">
                    <p className="text-sm text-blue-700">Conservador</p>
                    <p className="text-2xl font-bold text-blue-900">{lostMiles.conservative_avios.toLocaleString('es-ES')} Avios</p>
                  </div>
                  <div className="rounded-md bg-green-50 p-4">
                    <p className="text-sm text-green-700">Con stacking</p>
                    <p className="text-2xl font-bold text-green-900">{lostMiles.aggressive_avios.toLocaleString('es-ES')} Avios</p>
                  </div>
                </div>
                <div className="mt-4 rounded-md bg-amber-50 p-3 text-sm text-amber-900">
                  {lostMiles.recommendations.join(' ')}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
