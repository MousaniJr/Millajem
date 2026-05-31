'use client';

import { useEffect, useState } from 'react';
import { alertsApi, promotionsApi, Alert } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Promotions() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [socialAccounts, setSocialAccounts] = useState<any[]>([]);
  const [showSocial, setShowSocial] = useState(false);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [filters, setFilters] = useState({
    country: 'all',
    type: 'all',
    source_type: 'all',
    priority: 'all',
    related_program: 'all',
    unread_only: false,
    favorites_only: false,
    order_by: 'date_desc',
  });

  useEffect(() => {
    loadAlerts();
    loadSocialAccounts();
  }, [filters]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (filters.country !== 'all') params.country = filters.country;
      if (filters.type !== 'all') params.alert_type = filters.type;
      if (filters.source_type !== 'all') params.source_type = filters.source_type;
      if (filters.priority !== 'all') params.priority = filters.priority;
      if (filters.related_program !== 'all') params.related_program = filters.related_program;
      if (filters.unread_only) params.unread_only = true;
      if (filters.favorites_only) params.favorites_only = true;
      params.order_by = filters.order_by;

      const response = await alertsApi.getAll(params);
      setAlerts(response.data);
    } catch (err) {
      console.error('Error loading alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSocialAccounts = async () => {
    try {
      const response = await promotionsApi.getSocialAccounts();
      setSocialAccounts(response.data.recommendations);
    } catch (err) {
      console.error('Error loading social accounts:', err);
    }
  };

  const handleScan = async () => {
    try {
      setScanning(true);
      await promotionsApi.scan(50);
      await loadAlerts();
      alert('Escaneo completado! Se han encontrado nuevas promociones.');
    } catch (err) {
      console.error('Error scanning:', err);
      alert('Error al escanear promociones');
    } finally {
      setScanning(false);
    }
  };

  const handleToggleFavorite = async (id: number) => {
    try {
      await alertsApi.toggleFavorite(id);
      loadAlerts();
    } catch (err) {
      console.error('Error toggling favorite:', err);
    }
  };

  const handleMarkAsRead = async (id: number) => {
    try {
      await alertsApi.markAsRead(id);
      loadAlerts();
    } catch (err) {
      console.error('Error marking as read:', err);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'normal':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'low':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      bonus_transfer: '🔄 Bonus Transferencia',
      purchase_bonus: '💰 Bonus Compra',
      stackable_combo: 'Combo Apilable',
      award_discount: 'Descuento Emision',
      promo_detected: '🎯 Promoción',
      error_fare: '✈️ Error Fare',
      general_info: 'ℹ️ Info General',
    };
    return labels[type] || type;
  };

  const getSourceTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      rss_blog: '📰 Blog',
      official_web: 'Web Oficial',
      promo_landing: 'Landing Promo',
      partner_catalog: 'Catalogo Partner',
      instagram: '📸 Instagram',
      twitter: '🐦 Twitter/X',
      telegram: '✈️ Telegram',
      manual: '✍️ Manual',
    };
    return labels[type] || type;
  };

  const getCountryFlag = (country: string | null) => {
    const flags: Record<string, string> = {
      ES: '🇪🇸',
      BR: '🇧🇷',
      UK: '🇬🇧',
      INT: '🌍',
    };
    return country ? flags[country] || '🌍' : '🌍';
  };

  // Obtener valores únicos para filtros
  const uniquePrograms = [...new Set(alerts.map((a) => a.related_program).filter((p): p is string => p !== null && p !== undefined))];
  const uniqueSources = [...new Set(alerts.map((a) => a.source_name).filter((s): s is string => s !== null && s !== undefined))];

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Promociones y Alertas</h2>
          <p className="mt-2 text-sm text-gray-600">
            {alerts.length} promociones encontradas desde blogs y redes sociales
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowSocial(!showSocial)}
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
          >
            📱 Cuentas Sociales
          </button>
          <button
            onClick={handleScan}
            disabled={scanning}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:bg-gray-300"
          >
            {scanning ? 'Escaneando...' : '🔄 Escanear Ahora'}
          </button>
        </div>
      </div>

        {/* Social Media Accounts Modal */}
        {showSocial && (
        <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-purple-300">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">📱 Cuentas de Redes Sociales</h3>
            <button
              onClick={() => setShowSocial(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            Sigue estas cuentas para recibir promociones en tiempo real
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {socialAccounts
              .filter((acc) => filters.country === 'all' || acc.country === filters.country)
              .map((acc, idx) => (
                <a
                  key={idx}
                  href={acc.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 p-3 border rounded-md hover:bg-gray-50 transition"
                >
                  <span className="text-2xl">
                    {acc.platform === 'Instagram' ? '📸' : '🐦'}
                  </span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{acc.account}</p>
                    <p className="text-xs text-gray-500">
                      {acc.platform} • {getCountryFlag(acc.country)}
                    </p>
                  </div>
                  <span className="text-primary-600">→</span>
                </a>
              ))}
          </div>
        </div>
      )}

        {/* Advanced Filters */}
        <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {/* Country */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">País</label>
            <select
              value={filters.country}
              onChange={(e) => setFilters({ ...filters, country: e.target.value })}
              className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">Todos</option>
              <option value="ES">🇪🇸 España</option>
              <option value="BR">🇧🇷 Brasil</option>
              <option value="INT">🌍 Internacional</option>
            </select>
          </div>

          {/* Type */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Tipo</label>
            <select
              value={filters.type}
              onChange={(e) => setFilters({ ...filters, type: e.target.value })}
              className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">Todos</option>
              <option value="bonus_transfer">Bonus Transferencia</option>
              <option value="purchase_bonus">Bonus Compra</option>
              <option value="stackable_combo">Combo Apilable</option>
              <option value="award_discount">Descuento Emision</option>
              <option value="promo_detected">Promoción</option>
              <option value="error_fare">Error Fare</option>
            </select>
          </div>

          {/* Source Type */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Fuente</label>
            <select
              value={filters.source_type}
              onChange={(e) => setFilters({ ...filters, source_type: e.target.value })}
              className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">Todas</option>
              <option value="rss_blog">📰 Blogs</option>
              <option value="official_web">Web Oficial</option>
              <option value="promo_landing">Landing Promo</option>
              <option value="partner_catalog">Catalogo Partner</option>
              <option value="instagram">📸 Instagram</option>
              <option value="twitter">🐦 Twitter</option>
              <option value="telegram">✈️ Telegram</option>
            </select>
          </div>

          {/* Priority */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Prioridad</label>
            <select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
              className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">Todas</option>
              <option value="urgent">🔴 Urgent</option>
              <option value="high">🟠 High</option>
              <option value="normal">🔵 Normal</option>
              <option value="low">⚪ Low</option>
            </select>
          </div>

          {/* Program */}
          {uniquePrograms.length > 0 && (
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Programa</label>
              <select
                value={filters.related_program}
                onChange={(e) => setFilters({ ...filters, related_program: e.target.value })}
                className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">Todos</option>
                {uniquePrograms.map((prog) => (
                  <option key={prog} value={prog}>
                    {prog}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Order */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Ordenar</label>
            <select
              value={filters.order_by}
              onChange={(e) => setFilters({ ...filters, order_by: e.target.value })}
              className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="date_desc">Más recientes</option>
              <option value="date_asc">Más antiguas</option>
              <option value="priority_desc">Por prioridad</option>
            </select>
          </div>

          {/* Toggle Filters */}
          <div className="flex items-end gap-2">
            <label className="flex items-center text-sm text-gray-700">
              <input
                type="checkbox"
                checked={filters.unread_only}
                onChange={(e) => setFilters({ ...filters, unread_only: e.target.checked })}
                className="mr-1.5"
              />
              Solo no leídas
            </label>
          </div>

          <div className="flex items-end gap-2">
            <label className="flex items-center text-sm text-gray-700">
              <input
                type="checkbox"
                checked={filters.favorites_only}
                onChange={(e) => setFilters({ ...filters, favorites_only: e.target.checked })}
                className="mr-1.5"
              />
              Solo favoritas
            </label>
          </div>
        </div>
      </div>

        {/* Alerts List */}
        {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary-600 border-r-transparent"></div>
          <p className="mt-2 text-gray-600">Cargando promociones...</p>
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <span className="text-6xl">🔍</span>
          <h3 className="mt-4 text-lg font-medium text-gray-900">No hay promociones</h3>
          <p className="mt-2 text-sm text-gray-600">
            Ajusta los filtros o haz clic en "Escanear Ahora"
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`bg-white rounded-lg shadow p-6 border-l-4 ${
                alert.alert_type === 'stackable_combo'
                  ? 'border-l-green-500 ring-1 ring-green-200'
                  : alert.priority === 'high' || alert.priority === 'urgent'
                  ? 'border-l-orange-500'
                  : 'border-l-blue-500'
              } ${alert.is_read ? 'opacity-60' : ''}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  {/* Header */}
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className="text-xl">{getCountryFlag(alert.country)}</span>
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(
                        alert.priority
                      )}`}
                    >
                      {alert.priority.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500">{getTypeLabel(alert.alert_type)}</span>
                    <span className="text-xs text-purple-600">
                      {getSourceTypeLabel(alert.source_type)}
                    </span>
                    {alert.source_name && (
                      <span className="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded">
                        {alert.source_name}
                      </span>
                    )}
                    {alert.related_program && (
                      <span className="text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded">
                        {alert.related_program}
                      </span>
                    )}
                    {alert.detected_bonus_percentage !== null && (
                      <span className="text-xs bg-green-50 text-green-700 px-2 py-0.5 rounded">
                        +{alert.detected_bonus_percentage}% detectado
                      </span>
                    )}
                  </div>

                  {/* Title */}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{alert.title}</h3>

                  {/* Message */}
                  <p className="text-sm text-gray-600 mb-3">{alert.message}</p>

                  {/* Footer */}
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>
                      {new Date(alert.created_at).toLocaleDateString('es-ES', {
                        day: '2-digit',
                        month: 'short',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                    {alert.source_url && (
                      <a
                        href={alert.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-800 underline"
                      >
                        Ver oferta completa →
                      </a>
                    )}
                    {alert.end_date && (
                      <span>Fin: {new Date(alert.end_date).toLocaleDateString('es-ES')}</span>
                    )}
                    {alert.confidence && (
                      <span className="uppercase">{alert.confidence}</span>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2 ml-4">
                  <button
                    onClick={() => handleToggleFavorite(alert.id)}
                    className="text-2xl hover:scale-110 transition-transform"
                    title={alert.is_favorite ? 'Quitar de favoritos' : 'Añadir a favoritos'}
                  >
                    {alert.is_favorite ? '⭐' : '☆'}
                  </button>
                  {!alert.is_read && (
                    <button
                      onClick={() => handleMarkAsRead(alert.id)}
                      className="text-xs text-gray-500 hover:text-gray-700"
                      title="Marcar como leída"
                    >
                      ✓
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Sistema de Monitoreo Automático</h4>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• El sistema escanea automáticamente cada 2 horas ({alerts.filter(a => a.source_type === 'rss_blog').length} de blogs RSS)</li>
          <li>• {socialAccounts.length} cuentas de redes sociales recomendadas para seguir</li>
          <li>• Usa filtros avanzados para encontrar exactamente lo que necesitas</li>
          <li>• Marca favoritas las promociones que quieras revisar después</li>
        </ul>
        </div>
      </div>
    </ProtectedRoute>
  );
}
