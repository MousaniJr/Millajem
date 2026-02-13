'use client';

import { useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';

// ── Tabla de premios Iberia (off-peak, one-way) ─────────────────────────────
const AWARD_CHART = [
  { band: '0–650 mi', example: 'Madrid–Barcelona', eco_basic: 3500, eco_comfort: 7000, premium_eco: null, business: 9750 },
  { band: '651–1.150 mi', example: 'MAD–Londres/París', eco_basic: 6500, eco_comfort: 12500, premium_eco: null, business: 16500 },
  { band: '1.151–2.000 mi', example: 'MAD–Canarias/Cairo', eco_basic: 9500, eco_comfort: 16000, premium_eco: null, business: 22000 },
  { band: '2.001–3.000 mi', example: 'MAD–Oriente Medio', eco_basic: 10500, eco_comfort: 17000, premium_eco: null, business: 23000 },
  { band: '3.001–4.000 mi', example: 'MAD–Nueva York', eco_basic: 16000, eco_comfort: 25000, premium_eco: 29500, business: 40500 },
  { band: '4.001–5.500 mi ★', example: 'MAD–GRU/MIA', eco_basic: 20000, eco_comfort: 31250, premium_eco: 36750, business: 50500 },
  { band: '5.501–6.500 mi', example: 'MAD–Buenos Aires', eco_basic: 24000, eco_comfort: 37250, premium_eco: 44000, business: 60500 },
  { band: '6.501–7.000 mi', example: 'MAD–Bangkok/Tokio', eco_basic: 28250, eco_comfort: 42750, premium_eco: 51000, business: 70500 },
  { band: '+7.000 mi', example: 'MAD–Sydney/Auckland', eco_basic: 41000, eco_comfort: 60000, premium_eco: 71000, business: 97000 },
];

// ── Surcharges por método de reserva ───────────────────────────────────────
const SURCHARGES = [
  { method: 'Iberia Avios (metal Iberia)', route: 'MAD–GRU', surcharge: '~100–140 €', rating: 'good', note: 'MEJOR VALOR. Tasas bajas para la industria.' },
  { method: 'Qatar Avios (vía Doha)', route: 'MAD–DOH–GRU', surcharge: 'Reducidos/0 (2026)', rating: 'good', note: 'Mejor producto (QSuite). Surcharges eliminados en 2026.' },
  { method: 'BA Avios (metal BA vía Londres)', route: 'MAD–LHR–GRU', surcharge: '~135–270 GBP', rating: 'bad', note: 'EVITAR. Surcharges altísimos en metal BA.' },
  { method: 'Vuelos saliendo de Brasil', route: 'GRU–MAD', surcharge: '10–35 USD', rating: 'best', note: 'TRUCO: Brasil prohíbe fuel surcharges en vuelos de salida. Reservar tramo vuelta por separado.' },
  { method: 'BA GIB–LHR (Banda 2)', route: 'GIB–LHR', surcharge: '~1 GBP economy', rating: 'best', note: 'Sweet spot: tasas mínimas, 7.250 Avios off-peak.' },
];

// ── Los 7 programas Avios y sus transferencias ─────────────────────────────
const AVIOS_PROGRAMS = [
  { name: 'Iberia Club', flag: '🇪🇸', note: 'PRINCIPAL. Vuelos directos MAD-Brasil. Family Account.' },
  { name: 'BA Executive Club', flag: '🇬🇧', note: 'Household Account. GIB-LHR sweet spot.' },
  { name: 'Qatar Privilege Club', flag: '🇶🇦', note: 'QSuites (mejor business del mundo). Surcharges 0.' },
  { name: 'Vueling Club', flag: '🇪🇸', note: 'Vuelos low-cost Europa con Avios. IAG.' },
  { name: 'Finnair Plus', flag: '🇫🇮', note: 'Conexiones Asia vía Helsinki. oneworld.' },
  { name: 'Aer Lingus AerClub', flag: '🇮🇪', note: 'Transatlántico económico desde Europa.' },
  { name: 'Loganair', flag: '🏴󠁧󠁢󠁳󠁣󠁴󠁿', note: 'Regional UK. Poca relevancia.' },
];

// ── Simulador MAD-GRU familiar ─────────────────────────────────────────────
const CABIN_DATA = [
  { cabin: 'Economy Basic', avios_ow: 20000, label: 'Economy Basic' },
  { cabin: 'Economy Comfort', avios_ow: 31250, label: 'Economy Comfort' },
  { cabin: 'Premium Economy', avios_ow: 36750, label: 'Premium Economy' },
  { cabin: 'Business', avios_ow: 50500, label: 'Business ★' },
];

// ── Mejores rutas de canje ──────────────────────────────────────────────────
const BEST_REDEMPTIONS = [
  { route: 'MAD–GRU (directo)', avios: '50.500', surcharge: '~120 €', rating: 'best', note: 'Iberia directo. Mejor valor Avios para Brasil.' },
  { route: 'MAD–REC/FOR (directo)', avios: '50.500', surcharge: '~120 €', rating: 'best', note: 'Nordeste de Brasil. Misma banda que GRU.' },
  { route: 'MAD–DOH–GRU (Qatar)', avios: '60.000–80.000', surcharge: '~0 (2026)', rating: 'good', note: 'QSuite. Mejor producto aunque más Avios.' },
  { route: 'GIB–LHR Economy', avios: '7.250', surcharge: '~1 GBP', rating: 'best', note: 'Sweet spot. Tasas mínimas.' },
  { route: 'GIB–LHR Business', avios: '13.500', surcharge: '~15 GBP', rating: 'good', note: 'Club Europe. Buen valor corta distancia.' },
  { route: 'MAD–JFK/BOS', avios: '40.500', surcharge: 'Variable', rating: 'good', note: 'USA Este Business. Sweet spot premier.' },
  { route: 'MAD–NRT (Tokio)', avios: '70.500', surcharge: 'Variable', rating: 'ok', note: 'Iberia directo o Finnair vía HEL.' },
  { route: 'MAD–BCN (doméstico)', avios: '3.500', surcharge: 'Mínima', rating: 'good', note: 'Banda 1. Buena relación para viajes domésticos.' },
];

export default function Strategy() {
  const [passengers, setPassengers] = useState(4);
  const [trips, setTrips] = useState(1);
  const [selectedCabin, setSelectedCabin] = useState(3); // Business por defecto
  const [peakSeason, setPeakSeason] = useState(false);
  const [activeTab, setActiveTab] = useState<'awards' | 'surcharges' | 'simulator' | 'programs' | 'redemptions'>('simulator');

  const cabin = CABIN_DATA[selectedCabin];
  const peakMultiplier = peakSeason ? 1.35 : 1;
  const aviosNeeded = Math.round(cabin.avios_ow * 2 * passengers * trips * peakMultiplier);

  // Fuentes para acumular esos Avios
  const sources = [
    { label: 'Amex Gold ES (2.000€/mes)', annual: 24000 },
    { label: 'Amex Platinum ES (2.000€/mes)', annual: 24000 },
    { label: 'Cepsa (60 L/mes)', annual: Math.round(60 * 2 * 12) },
    { label: 'Esfera BR → Iberia (2:1)', annual: 0 },
    { label: 'Bonus bienvenida Amex Gold', annual: 20000, oneTime: true },
    { label: 'Bonus bienvenida Amex Platinum', annual: 120000, oneTime: true },
  ];

  const ratingColor = (r: string) => {
    if (r === 'best') return 'bg-green-100 text-green-800 border-green-200';
    if (r === 'good') return 'bg-blue-50 text-blue-800 border-blue-200';
    if (r === 'bad') return 'bg-red-50 text-red-800 border-red-200';
    return 'bg-gray-50 text-gray-700 border-gray-200';
  };

  const tabs = [
    { key: 'simulator', label: 'Simulador MAD-GRU', icon: '✈️' },
    { key: 'awards', label: 'Tabla de Premios', icon: '📋' },
    { key: 'surcharges', label: 'Surcharges', icon: '💰' },
    { key: 'programs', label: '7 Programas Avios', icon: '🔗' },
    { key: 'redemptions', label: 'Mejores Canjes', icon: '⭐' },
  ] as const;

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Estrategia</h2>
          <p className="mt-2 text-sm text-gray-600">
            Tabla de premios Iberia, surcharges, simulador familiar y mejores canjes
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow">
          <div className="flex overflow-x-auto border-b">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex-shrink-0 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.key
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <span className="mr-1">{tab.icon}</span>
                <span className="hidden sm:inline">{tab.label}</span>
              </button>
            ))}
          </div>

          <div className="p-6">

            {/* ── SIMULADOR ── */}
            {activeTab === 'simulator' && (
              <div className="space-y-6">
                <h3 className="text-xl font-bold text-gray-900">Simulador MAD-GRU Familiar</h3>
                <p className="text-sm text-gray-600">Calcula los Avios necesarios para volar a Brasil con tu familia.</p>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Pasajeros</label>
                    <input type="number" min={1} max={8} value={passengers}
                      onChange={e => setPassengers(parseInt(e.target.value) || 1)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Viajes/año</label>
                    <input type="number" min={1} max={5} value={trips}
                      onChange={e => setTrips(parseInt(e.target.value) || 1)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Cabina</label>
                    <select value={selectedCabin} onChange={e => setSelectedCabin(parseInt(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500">
                      {CABIN_DATA.map((c, i) => (
                        <option key={i} value={i}>{c.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Temporada</label>
                    <select value={peakSeason ? 'peak' : 'offpeak'} onChange={e => setPeakSeason(e.target.value === 'peak')}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500">
                      <option value="offpeak">Off-Peak</option>
                      <option value="peak">Peak (+35%)</option>
                    </select>
                  </div>
                </div>

                {/* Result */}
                <div className="bg-gradient-to-br from-primary-50 to-blue-50 rounded-xl p-6 border border-primary-200">
                  <div className="text-center mb-4">
                    <p className="text-sm text-gray-600 mb-1">
                      {passengers} persona{passengers > 1 ? 's' : ''} · {trips} viaje{trips > 1 ? 's' : ''}/año · {cabin.label} · {peakSeason ? 'Peak' : 'Off-Peak'}
                    </p>
                    <p className="text-5xl font-bold text-primary-600">{aviosNeeded.toLocaleString('es-ES')}</p>
                    <p className="text-lg text-gray-700 mt-1">Avios necesarios (ida + vuelta)</p>
                  </div>

                  <div className="grid grid-cols-3 gap-3 text-center mt-4">
                    <div className="bg-white rounded-lg p-3">
                      <p className="text-xs text-gray-500">Por persona ida+vuelta</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {(cabin.avios_ow * 2 * (peakSeason ? 1.35 : 1)).toLocaleString('es-ES', {maximumFractionDigits: 0})}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <p className="text-xs text-gray-500">Tasas aprox.</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {passengers * trips * (selectedCabin >= 3 ? 240 : 120)}–{passengers * trips * (selectedCabin >= 3 ? 560 : 240)} €
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <p className="text-xs text-gray-500">Avios/año Amex Gold</p>
                      <p className="text-lg font-semibold text-gray-900">~24.000</p>
                    </div>
                  </div>
                </div>

                {/* Fuentes de acumulación */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">¿Cómo acumular {aviosNeeded.toLocaleString('es-ES')} Avios?</h4>
                  <div className="space-y-2">
                    {[
                      { label: 'Amex Gold ES (2.000€/mes gasto)', avios: 24000, recurring: true },
                      { label: 'Cepsa (60 litros/mes)', avios: 1440, recurring: true },
                      { label: 'Iberia Plus Store (200€/mes online)', avios: 4800, recurring: true },
                      { label: 'Bonus bienvenida Amex Gold', avios: 20000, recurring: false },
                      { label: 'Bonus bienvenida Amex Platinum', avios: 120000, recurring: false },
                      { label: 'Esfera BR → Iberia 2:1 (compra Avios promo)', avios: 30000, recurring: false },
                    ].map((s, i) => {
                      const pct = Math.min(100, Math.round((s.avios / aviosNeeded) * 100));
                      return (
                        <div key={i} className="flex items-center gap-3">
                          <div className="flex-1">
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-gray-700">
                                {s.label}
                                {s.recurring && <span className="ml-1 text-gray-400">(recurrente/año)</span>}
                              </span>
                              <span className="font-medium text-gray-900">{s.avios.toLocaleString('es-ES')}</span>
                            </div>
                            <div className="h-2 bg-gray-100 rounded-full">
                              <div className="h-2 bg-primary-400 rounded-full" style={{ width: `${pct}%` }} />
                            </div>
                          </div>
                          <span className="text-xs text-gray-500 w-10 text-right">{pct}%</span>
                        </div>
                      );
                    })}
                  </div>
                  <p className="text-xs text-gray-500 mt-3">
                    Con Amex Gold + Cepsa + portales: ~30.240 Avios/año recurrentes. Con bonus bienvenida Amex Platinum: potencial de +144.000 Avios el primer año.
                  </p>
                </div>
              </div>
            )}

            {/* ── TABLA DE PREMIOS ── */}
            {activeTab === 'awards' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Tabla de Premios Iberia</h3>
                  <p className="text-sm text-gray-600 mt-1">Avios necesarios por banda de distancia · One-way · Off-peak · Desde mayo 2025</p>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 text-sm">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Banda</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ejemplo</th>
                        <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase">Eco Basic</th>
                        <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase">Eco Comfort</th>
                        <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase">Premium Eco</th>
                        <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase">Business</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-100">
                      {AWARD_CHART.map((row, i) => (
                        <tr key={i} className={row.band.includes('★') ? 'bg-primary-50 font-semibold' : 'hover:bg-gray-50'}>
                          <td className="px-3 py-2 text-gray-900 whitespace-nowrap">{row.band}</td>
                          <td className="px-3 py-2 text-gray-500 text-xs">{row.example}</td>
                          <td className="px-3 py-2 text-right text-gray-900">{row.eco_basic.toLocaleString('es-ES')}</td>
                          <td className="px-3 py-2 text-right text-gray-900">{row.eco_comfort.toLocaleString('es-ES')}</td>
                          <td className="px-3 py-2 text-right text-gray-500">{row.premium_eco ? row.premium_eco.toLocaleString('es-ES') : '–'}</td>
                          <td className="px-3 py-2 text-right font-semibold text-primary-700">{row.business.toLocaleString('es-ES')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-amber-800 space-y-1">
                  <p><strong>★ Banda 4.001–5.500 mi</strong> = MAD–GRU/MIA/BOG. Business off-peak: 50.500 Avios one-way.</p>
                  <p><strong>Peak season:</strong> Los precios suben ~25–45%. Consultar calendario peak/off-peak de Iberia.</p>
                  <p><strong>Rutas directas Iberia a Brasil desde Madrid:</strong> GRU, GIG, REC, FOR.</p>
                </div>
              </div>
            )}

            {/* ── SURCHARGES ── */}
            {activeTab === 'surcharges' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Comparativa de Surcharges</h3>
                  <p className="text-sm text-gray-600 mt-1">Las tasas y recargos varían enormemente según cómo reserves. Este dato es crítico para maximizar el valor de tus Avios.</p>
                </div>
                <div className="space-y-3">
                  {SURCHARGES.map((s, i) => (
                    <div key={i} className={`rounded-lg border p-4 ${ratingColor(s.rating)}`}>
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex-1">
                          <p className="font-semibold">{s.method}</p>
                          <p className="text-xs mt-0.5 opacity-75">{s.route}</p>
                          <p className="text-sm mt-1">{s.note}</p>
                        </div>
                        <div className="text-right shrink-0">
                          <p className="font-bold">{s.surcharge}</p>
                          {s.rating === 'best' && <span className="text-xs font-medium">✓ RECOMENDADO</span>}
                          {s.rating === 'bad' && <span className="text-xs font-medium">✗ EVITAR</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-sm text-green-800">
                  <p className="font-semibold mb-1">Truco clave: Tramo de vuelta desde Brasil</p>
                  <p>Brasil prohíbe los fuel surcharges en vuelos de salida. Reservar el tramo GRU→MAD como billete separado one-way te ahorra hasta 270 GBP/persona en tasas.</p>
                </div>
              </div>
            )}

            {/* ── 7 PROGRAMAS AVIOS ── */}
            {activeTab === 'programs' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Los 7 Programas Avios</h3>
                  <p className="text-sm text-gray-600 mt-1">Desde otoño 2025: transferencias 1:1 bidireccionales entre cualquier par. Sin intermediarios, sin límites, gratis.</p>
                </div>

                {/* Transfer diagram */}
                <div className="bg-gray-50 rounded-xl p-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
                    {AVIOS_PROGRAMS.map((p, i) => (
                      <div key={i} className={`bg-white rounded-lg p-3 border text-center ${i < 3 ? 'border-primary-300' : 'border-gray-200'}`}>
                        <div className="text-2xl mb-1">{p.flag}</div>
                        <p className="text-xs font-semibold text-gray-900">{p.name}</p>
                        <p className="text-xs text-gray-500 mt-1">{p.note}</p>
                      </div>
                    ))}
                  </div>
                  <div className="text-center text-sm text-gray-600 bg-white rounded-lg p-3 border">
                    <span className="font-semibold text-primary-700">Ratio siempre 1:1</span> · Gratis · Sin límite de transferencia · Instantáneo
                  </div>
                </div>

                {/* Cuando usar cada programa */}
                <div className="space-y-3">
                  <h4 className="font-semibold text-gray-900">¿Cuándo usar cada uno?</h4>
                  {[
                    { prog: 'Iberia Club', use: 'Vuelos MAD-Brasil directo. Family Account (hasta 7 miembros). Surcharges más bajos.', priority: 1 },
                    { prog: 'BA Executive Club', use: 'Household Account. Partners BookWithAvios. GIB-LHR sweet spot (7.250 Avios).', priority: 2 },
                    { prog: 'Qatar Privilege Club', use: 'QSuites (mejor business del mundo). Surcharges eliminados en 2026. MAD-DOH-GRU.', priority: 2 },
                    { prog: 'Vueling Club', use: 'Vuelos domésticos e intraeuropeos baratos con Avios. Desde 2.000 Avios.', priority: 3 },
                    { prog: 'Finnair Plus', use: 'Conexiones a Asia vía Helsinki. oneworld. Buen valor destinos asiáticos.', priority: 4 },
                    { prog: 'Aer Lingus AerClub', use: 'Transatlántico económico desde Europa. IAG. Alternativa USA.', priority: 4 },
                  ].map((item, i) => (
                    <div key={i} className="flex items-start gap-3 bg-white rounded-lg p-3 border border-gray-100">
                      <span className={`shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                        item.priority === 1 ? 'bg-primary-600' : item.priority === 2 ? 'bg-blue-500' : 'bg-gray-400'
                      }`}>{item.priority}</span>
                      <div>
                        <p className="text-sm font-semibold text-gray-900">{item.prog}</p>
                        <p className="text-xs text-gray-600">{item.use}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* ── MEJORES CANJES ── */}
            {activeTab === 'redemptions' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Mejores Rutas de Canje</h3>
                  <p className="text-sm text-gray-600 mt-1">Avios one-way off-peak. Business salvo donde se indique.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {BEST_REDEMPTIONS.map((r, i) => (
                    <div key={i} className={`rounded-lg border p-4 ${ratingColor(r.rating)}`}>
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <p className="font-semibold">{r.route}</p>
                          <p className="text-xs mt-1 opacity-75">{r.note}</p>
                        </div>
                        <div className="text-right shrink-0">
                          <p className="font-bold">{r.avios} Avios</p>
                          <p className="text-xs">+{r.surcharge} tasas</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                  <p className="font-semibold mb-1">Otras alianzas complementarias</p>
                  <ul className="space-y-1">
                    <li><strong>Air Europa SUMA (SkyTeam):</strong> MAD-GRU directo, alternativa a Iberia.</li>
                    <li><strong>Flying Blue (AF/KLM):</strong> Promo Rewards mensuales hasta 50% off. Economy Europa desde 15K millas.</li>
                    <li><strong>Turkish M&S (Star Alliance):</strong> Sin surcharges en Lufthansa. Acceso Lufthansa First.</li>
                    <li><strong>TAP Miles&Go:</strong> Lisboa–Brasil. Útil si vuelas vía LIS.</li>
                  </ul>
                </div>
              </div>
            )}

          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
