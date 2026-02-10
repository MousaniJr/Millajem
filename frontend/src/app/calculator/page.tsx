'use client';

import { useEffect, useState } from 'react';
import { programsApi, calculatorApi, LoyaltyProgram, ConversionResult } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Calculator() {
  const [programs, setPrograms] = useState<LoyaltyProgram[]>([]);
  const [selectedProgram, setSelectedProgram] = useState<number | null>(null);
  const [points, setPoints] = useState<string>('');
  const [result, setResult] = useState<ConversionResult | null>(null);
  const [allResults, setAllResults] = useState<ConversionResult[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPrograms();
  }, []);

  const loadPrograms = async () => {
    try {
      const response = await programsApi.getAll();
      const convertiblePrograms = response.data.filter(p => p.avios_ratio !== null);
      setPrograms(convertiblePrograms);
    } catch (err) {
      console.error('Error loading programs:', err);
    }
  };

  const handleCalculate = async () => {
    if (!selectedProgram || !points) return;

    setLoading(true);
    try {
      const response = await calculatorApi.toAvios(selectedProgram, parseFloat(points));
      setResult(response.data);
    } catch (err) {
      console.error('Error calculating:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompareAll = async () => {
    if (!points) return;

    setLoading(true);
    try {
      const response = await calculatorApi.allToAvios(parseFloat(points));
      setAllResults(response.data);
    } catch (err) {
      console.error('Error comparing:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        {/* Header */}
        <div>
        <h2 className="text-3xl font-bold text-gray-900">Calculadora de Conversión</h2>
        <p className="mt-2 text-sm text-gray-600">
          Calcula cuántos Avios valen tus puntos
        </p>
      </div>

        {/* Calculator Form */}
        <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Programa
            </label>
            <select
              value={selectedProgram || ''}
              onChange={(e) => setSelectedProgram(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Selecciona un programa</option>
              {programs.map((program) => (
                <option key={program.id} value={program.id}>
                  {program.name} ({program.currency}) - {program.country}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cantidad de Puntos
            </label>
            <input
              type="number"
              value={points}
              onChange={(e) => setPoints(e.target.value)}
              placeholder="10000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleCalculate}
              disabled={!selectedProgram || !points || loading}
              className="flex-1 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {loading ? 'Calculando...' : 'Calcular'}
            </button>
            <button
              onClick={handleCompareAll}
              disabled={!points || loading}
              className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Comparar Todos
            </button>
          </div>
        </div>

        {/* Single Result */}
        {result && (
          <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Conversión</p>
                <p className="text-lg font-semibold text-gray-900">{result.message}</p>
              </div>
              <div className="text-right">
                <p className="text-3xl font-bold text-primary-600">
                  {result.avios_output?.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
                </p>
                <p className="text-sm text-gray-600">Avios</p>
              </div>
            </div>
          </div>
        )}
      </div>

        {/* Comparison Results */}
        {allResults.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="bg-gray-50 px-6 py-3 border-b">
            <h3 className="text-lg font-medium text-gray-900">
              Comparación de Valor ({points} puntos)
            </h3>
          </div>
          <div className="divide-y">
            {allResults.map((res, idx) => {
              const isTop = idx === 0;
              return (
                <div
                  key={idx}
                  className={`px-6 py-4 ${isTop ? 'bg-green-50' : 'hover:bg-gray-50'}`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="text-sm font-medium text-gray-900">
                          {res.program_name}
                        </h4>
                        {isTop && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                            Mejor Valor
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        Ratio: {res.avios_ratio}:1
                      </p>
                    </div>
                    <div className="text-right">
                      <p className={`text-lg font-semibold ${isTop ? 'text-green-600' : 'text-gray-900'}`}>
                        {res.avios_output?.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
                      </p>
                      <p className="text-xs text-gray-500">Avios</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">💡 Mejores Ratios a Avios</h4>
          <ul className="space-y-1 text-sm text-blue-800">
            <li>• <strong>Esfera (BR)</strong>: 2:1 - La mejor opción desde Brasil</li>
            <li>• <strong>Amex MR (ES)</strong>: 1:1 - Ideal para España</li>
            <li>• <strong>Accor ALL</strong>: 1:1 - Mejor programa hotelero</li>
          </ul>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h4 className="font-medium text-amber-900 mb-2">⚠️ Consejos</h4>
          <ul className="space-y-1 text-sm text-amber-800">
            <li>• Espera promociones de bonus de transferencia</li>
            <li>• Livelo suele dar 80-100% bonus a Smiles</li>
            <li>• Iberia tiene 50% bonus en compra de Avios varias veces al año</li>
          </ul>
        </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
