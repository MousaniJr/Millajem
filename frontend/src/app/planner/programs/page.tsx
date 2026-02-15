'use client';

import { useEffect, useState } from 'react';
import { programsApi, LoyaltyProgram } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

const COUNTRY_LABELS: Record<string, { label: string; flag: string }> = {
  ES: { label: 'España', flag: '🇪🇸' },
  BR: { label: 'Brasil', flag: '🇧🇷' },
  GI: { label: 'Gibraltar / UK', flag: '🇬🇮' },
  INT: { label: 'Internacional', flag: '🌍' },
};

const CATEGORY_ICONS: Record<string, string> = {
  airline: '✈️',
  hotel: '🏨',
  transfer: '🔄',
  shopping: '🛍️',
  fuel: '⛽',
  supermarket: '🛒',
  transport: '🚗',
  airport: '🛫',
};

export default function ActivePrograms() {
  const [programs, setPrograms] = useState<LoyaltyProgram[]>([]);
  const [loading, setLoading] = useState(true);
  const [toggling, setToggling] = useState<number | null>(null);

  useEffect(() => {
    loadPrograms();
  }, []);

  const loadPrograms = async () => {
    try {
      setLoading(true);
      const res = await programsApi.getAll();
      setPrograms(res.data);
    } catch (err) {
      console.error('Error loading programs:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleEnrollment = async (programId: number) => {
    try {
      setToggling(programId);
      const res = await programsApi.toggleEnrollment(programId);
      setPrograms((prev) =>
        prev.map((p) => (p.id === programId ? res.data : p))
      );
    } catch (err) {
      console.error('Error toggling enrollment:', err);
    } finally {
      setToggling(null);
    }
  };

  // Group programs by country
  const grouped = programs.reduce<Record<string, LoyaltyProgram[]>>((acc, p) => {
    const key = p.country || 'INT';
    if (!acc[key]) acc[key] = [];
    acc[key].push(p);
    return acc;
  }, {});

  const enrolledCount = programs.filter((p) => p.is_enrolled).length;

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto p-4 sm:p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
              Mis Programas Activos
            </h1>
            <p className="text-gray-600 mt-1">
              Marca los programas de fidelidad en los que estás inscrito
            </p>
          </div>
          <a
            href="/planner"
            className="mt-3 sm:mt-0 inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium"
          >
            ← Volver al Planificador
          </a>
        </div>

        {/* Summary */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex items-center gap-4">
            <div className="bg-primary-100 rounded-full p-3">
              <span className="text-2xl">✅</span>
            </div>
            <div>
              <p className="text-2xl font-bold text-primary-700">{enrolledCount}</p>
              <p className="text-sm text-gray-500">
                de {programs.length} programas activos
              </p>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600 mx-auto"></div>
            <p className="text-gray-500 mt-3">Cargando programas...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(grouped)
              .sort(([a], [b]) => {
                const order = ['ES', 'BR', 'GI', 'INT'];
                return order.indexOf(a) - order.indexOf(b);
              })
              .map(([countryCode, progs]) => {
                const countryInfo = COUNTRY_LABELS[countryCode] || {
                  label: countryCode,
                  flag: '🏳️',
                };
                return (
                  <div key={countryCode} className="bg-white rounded-lg shadow">
                    <div className="px-5 py-3 border-b bg-gray-50 rounded-t-lg">
                      <h2 className="text-lg font-semibold text-gray-900">
                        {countryInfo.flag} {countryInfo.label}
                      </h2>
                    </div>
                    <div className="divide-y">
                      {progs.map((program) => (
                        <div
                          key={program.id}
                          className="flex items-center justify-between px-5 py-3 hover:bg-gray-50"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-lg">
                              {CATEGORY_ICONS[program.category] || '📌'}
                            </span>
                            <div>
                              <p className="font-medium text-gray-900">
                                {program.name}
                              </p>
                              <p className="text-sm text-gray-500">
                                {program.currency}
                                {program.avios_ratio
                                  ? ` · ${program.avios_ratio}:1 Avios`
                                  : ''}
                              </p>
                            </div>
                          </div>
                          <button
                            onClick={() => toggleEnrollment(program.id)}
                            disabled={toggling === program.id}
                            className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                              program.is_enrolled
                                ? 'bg-primary-600'
                                : 'bg-gray-200'
                            } ${toggling === program.id ? 'opacity-50' : ''}`}
                          >
                            <span
                              className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                                program.is_enrolled
                                  ? 'translate-x-5'
                                  : 'translate-x-0'
                              }`}
                            />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
