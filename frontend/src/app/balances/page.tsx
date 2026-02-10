'use client';

import { useEffect, useState } from 'react';
import { programsApi, balancesApi, LoyaltyProgram, Balance } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Balances() {
  const [programs, setPrograms] = useState<LoyaltyProgram[]>([]);
  const [balances, setBalances] = useState<Balance[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showProgramModal, setShowProgramModal] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    program_id: '',
    points: '',
    notes: '',
  });
  const [editingId, setEditingId] = useState<number | null>(null);

  // New program form state
  const [newProgramData, setNewProgramData] = useState({
    name: '',
    currency: 'Puntos',
    country: 'INT',
    category: 'other',
    avios_ratio: 0,
    notes: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [programsRes, balancesRes] = await Promise.all([
        programsApi.getAll(),
        balancesApi.getAll(),
      ]);
      setPrograms(programsRes.data);
      setBalances(balancesRes.data);
    } catch (err) {
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingId) {
        await balancesApi.update(editingId, {
          points: parseFloat(formData.points),
          notes: formData.notes || undefined,
        });
      } else {
        await balancesApi.create({
          program_id: parseInt(formData.program_id),
          points: parseFloat(formData.points),
          notes: formData.notes || undefined,
        });
      }

      setFormData({ program_id: '', points: '', notes: '' });
      setEditingId(null);
      setShowForm(false);
      loadData();
    } catch (err) {
      console.error('Error saving balance:', err);
      alert('Error al guardar el saldo');
    }
  };

  const handleEdit = (balance: Balance) => {
    setFormData({
      program_id: balance.program_id.toString(),
      points: balance.points.toString(),
      notes: balance.notes || '',
    });
    setEditingId(balance.id);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Estás seguro de eliminar este saldo?')) return;

    try {
      await balancesApi.delete(id);
      loadData();
    } catch (err) {
      console.error('Error deleting balance:', err);
      alert('Error al eliminar el saldo');
    }
  };

  const handleCancel = () => {
    setFormData({ program_id: '', points: '', notes: '' });
    setEditingId(null);
    setShowForm(false);
  };

  const handleCreateProgram = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await programsApi.create({
        name: newProgramData.name,
        currency: newProgramData.currency,
        country: newProgramData.country,
        category: newProgramData.category,
        avios_ratio: newProgramData.avios_ratio > 0 ? newProgramData.avios_ratio : 0,
        notes: newProgramData.notes || undefined,
      });

      // Reload programs
      const programsRes = await programsApi.getAll();
      setPrograms(programsRes.data);

      // Auto-select the new program
      setFormData({ ...formData, program_id: response.data.id.toString() });

      // Reset and close modal
      setNewProgramData({
        name: '',
        currency: 'Puntos',
        country: 'INT',
        category: 'other',
        avios_ratio: 0,
        notes: '',
      });
      setShowProgramModal(false);

      alert(`Programa "${response.data.name}" creado correctamente`);
    } catch (err: any) {
      console.error('Error creating program:', err);
      alert(err.response?.data?.detail || 'Error al crear programa');
    }
  };

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Mis Saldos</h2>
          <p className="mt-2 text-sm text-gray-600">
            Registra y actualiza tus saldos manualmente
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
        >
          {showForm ? 'Cancelar' : '+ Añadir Saldo'}
        </button>
      </div>

        {/* Form */}
        {showForm && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {editingId ? 'Editar Saldo' : 'Nuevo Saldo'}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Programa
              </label>
              <select
                value={formData.program_id}
                onChange={(e) => setFormData({ ...formData, program_id: e.target.value })}
                required
                disabled={editingId !== null}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
              >
                <option value="">Selecciona un programa</option>
                {programs.map((program) => (
                  <option key={program.id} value={program.id}>
                    {program.name} ({program.currency})
                  </option>
                ))}
              </select>
              {editingId === null && (
                <button
                  type="button"
                  onClick={() => setShowProgramModal(true)}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-800 underline"
                >
                  ➕ ¿No encuentras tu programa? Crear uno nuevo
                </button>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cantidad de Puntos
              </label>
              <input
                type="number"
                value={formData.points}
                onChange={(e) => setFormData({ ...formData, points: e.target.value })}
                required
                placeholder="15000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas (opcional)
              </label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                placeholder="Ej: Saldo inicial, obtenido en promoción..."
                rows={2}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                className="flex-1 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
              >
                {editingId ? 'Actualizar' : 'Guardar'}
              </button>
              <button
                type="button"
                onClick={handleCancel}
                className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

        {/* Balances List */}
        {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary-600 border-r-transparent"></div>
          <p className="mt-2 text-gray-600">Cargando saldos...</p>
        </div>
      ) : balances.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <span className="text-6xl">💰</span>
          <h3 className="mt-4 text-lg font-medium text-gray-900">No hay saldos registrados</h3>
          <p className="mt-2 text-sm text-gray-600">
            Haz clic en "Añadir Saldo" para registrar tu primer saldo
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Programa
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Puntos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Equiv. Avios
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Última Actualización
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {balances.map((balance) => {
                const aviosEquivalent = balance.program.avios_ratio
                  ? balance.points / balance.program.avios_ratio
                  : null;
                const lastUpdated = new Date(balance.last_updated).toLocaleDateString('es-ES');

                return (
                  <tr key={balance.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {balance.program.name}
                        </div>
                        <div className="text-xs text-gray-500">
                          {balance.program.currency} • {balance.program.country}
                        </div>
                        {balance.notes && (
                          <div className="text-xs text-gray-400 mt-1">{balance.notes}</div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-semibold text-gray-900">
                        {balance.points.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {aviosEquivalent !== null ? (
                        <div className="text-sm text-primary-600 font-medium">
                          {aviosEquivalent.toLocaleString('es-ES', { maximumFractionDigits: 0 })}
                        </div>
                      ) : (
                        <div className="text-sm text-gray-400">N/A</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {lastUpdated}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleEdit(balance)}
                        className="text-primary-600 hover:text-primary-900 mr-3"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleDelete(balance.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

        {/* Modal para crear nuevo programa */}
        {showProgramModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">Crear Programa Personalizado</h2>
              <p className="text-sm text-gray-600 mb-6">
                Crea un programa para puntos que no están en la lista, como Revolut Rev Points,
                tarjetas de tiendas, programas locales, etc.
              </p>

              <form onSubmit={handleCreateProgram}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nombre del Programa *
                    </label>
                    <input
                      type="text"
                      required
                      value={newProgramData.name}
                      onChange={(e) => setNewProgramData({ ...newProgramData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Ej: Revolut Rev Points, El Corte Inglés Club"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Moneda/Unidad *
                      </label>
                      <input
                        type="text"
                        required
                        value={newProgramData.currency}
                        onChange={(e) => setNewProgramData({ ...newProgramData, currency: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        placeholder="Ej: Puntos, Rev Points, Estrellas"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        País
                      </label>
                      <select
                        value={newProgramData.country}
                        onChange={(e) => setNewProgramData({ ...newProgramData, country: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      >
                        <option value="ES">🇪🇸 España</option>
                        <option value="BR">🇧🇷 Brasil</option>
                        <option value="GI">🇬🇮 Gibraltar</option>
                        <option value="UK">🇬🇧 Reino Unido</option>
                        <option value="US">🇺🇸 Estados Unidos</option>
                        <option value="INT">🌍 Internacional</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Ratio de conversión a Avios (opcional)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      value={newProgramData.avios_ratio}
                      onChange={(e) => setNewProgramData({ ...newProgramData, avios_ratio: parseFloat(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Ej: 1 (si 1 punto = 1 Avios), 2 (si 2 puntos = 1 Avios)"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                      Si tus puntos NO se convierten a Avios, deja en 0. Ejemplo: 2 significa que necesitas 2 puntos para 1 Avios.
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Notas (opcional)
                    </label>
                    <textarea
                      value={newProgramData.notes}
                      onChange={(e) => setNewProgramData({ ...newProgramData, notes: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      rows={2}
                      placeholder="Ej: Programa de fidelidad de Revolut, acumulo 1 punto por cada libra gastada"
                    />
                  </div>
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                  >
                    Crear Programa
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowProgramModal(false)}
                    className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
