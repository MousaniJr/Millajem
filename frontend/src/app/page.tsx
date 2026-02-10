'use client';

import { useEffect, useState } from 'react';
import { balancesApi, Balance } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Home() {
  const [balances, setBalances] = useState<Balance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadBalances();
  }, []);

  const loadBalances = async () => {
    try {
      setLoading(true);
      const response = await balancesApi.getAll();
      setBalances(response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar los saldos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const totalAvios = balances
    .filter(b => b.program.avios_ratio !== null)
    .reduce((sum, b) => {
      const avios = b.points / (b.program.avios_ratio || 1);
      return sum + avios;
    }, 0);

  const groupedByCountry = balances.reduce((acc, balance) => {
    const country = balance.program.country;
    if (!acc[country]) acc[country] = [];
    acc[country].push(balance);
    return acc;
  }, {} as Record<string, Balance[]>);

  const countryNames: Record<string, string> = {
    'ES': 'España',
    'BR': 'Brasil',
    'UK': 'Reino Unido',
    'QA': 'Qatar',
    'PT': 'Portugal',
    'INT': 'Internacional',
  };

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
          <p className="mt-2 text-sm text-gray-600">
            Vista general de tus puntos, millas y Avios
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Total Programas</p>
              <p className="text-2xl font-bold text-gray-900">{balances.length}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-2xl">💳</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Equivalente en Avios</p>
              <p className="text-2xl font-bold text-primary-600">
                {totalAvios.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
              </p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-2xl">✈️</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Mercados Activos</p>
              <p className="text-2xl font-bold text-gray-900">
                {Object.keys(groupedByCountry).length}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-2xl">🌍</span>
            </div>
          </div>
        </div>
        </div>

        {/* Balances by Country */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary-600 border-r-transparent"></div>
            <p className="mt-2 text-gray-600">Cargando saldos...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        ) : balances.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <span className="text-6xl">📊</span>
            <h3 className="mt-4 text-lg font-medium text-gray-900">No hay saldos registrados</h3>
            <p className="mt-2 text-sm text-gray-600">
              Comienza registrando tus primeros saldos en la sección "Mis Saldos"
            </p>
            <a
              href="/balances"
              className="mt-4 inline-block bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
            >
              Registrar Saldos
            </a>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedByCountry).map(([country, countryBalances]) => (
              <div key={country} className="bg-white rounded-lg shadow overflow-hidden">
                <div className="bg-gray-50 px-6 py-3 border-b">
                  <h3 className="text-lg font-medium text-gray-900">
                    {countryNames[country] || country}
                  </h3>
                </div>
                <div className="divide-y">
                  {countryBalances.map((balance) => {
                    const aviosEquivalent = balance.program.avios_ratio
                      ? balance.points / balance.program.avios_ratio
                      : null;

                    return (
                      <div key={balance.id} className="px-6 py-4 hover:bg-gray-50">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <h4 className="text-sm font-medium text-gray-900">
                              {balance.program.name}
                            </h4>
                            <p className="text-xs text-gray-500 mt-1">
                              {balance.program.category === 'airline' && '✈️ Aerolínea'}
                              {balance.program.category === 'hotel' && '🏨 Hotel'}
                              {balance.program.category === 'transfer' && '🔄 Transferible'}
                              {balance.program.category === 'shopping' && '🛍️ Shopping'}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-lg font-semibold text-gray-900">
                              {balance.points.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
                            </p>
                            <p className="text-xs text-gray-500">
                              {balance.program.currency}
                            </p>
                            {aviosEquivalent !== null && (
                              <p className="text-xs text-primary-600 mt-1">
                                ≈ {aviosEquivalent.toLocaleString('es-ES', { maximumFractionDigits: 0 })} Avios
                              </p>
                            )}
                          </div>
                        </div>
                        {balance.notes && (
                          <p className="text-xs text-gray-600 mt-2">{balance.notes}</p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
