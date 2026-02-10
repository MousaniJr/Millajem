'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import ProtectedRoute from '@/components/ProtectedRoute'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Source {
  id: number
  name: string
  source_type: string
  country: string
  url: string
  website_url?: string
  is_active: boolean
  priority: number
  description?: string
  notes?: string
  last_scraped?: string
  scrape_count: number
  alert_count: number
  created_at: string
}

interface Stats {
  total: number
  active: number
  inactive: number
  by_type: { [key: string]: number }
  by_country: { [key: string]: number }
}

export default function SourcesPage() {
  const [sources, setSources] = useState<Source[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Filtros
  const [filterType, setFilterType] = useState<string>('all')
  const [filterCountry, setFilterCountry] = useState<string>('all')
  const [filterActive, setFilterActive] = useState<string>('all')

  // Modal para añadir/editar
  const [showModal, setShowModal] = useState(false)
  const [editingSource, setEditingSource] = useState<Source | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    source_type: 'rss_feed',
    country: 'ES',
    url: '',
    website_url: '',
    is_active: true,
    priority: 5,
    description: '',
    notes: ''
  })

  useEffect(() => {
    fetchSources()
    fetchStats()
  }, [filterType, filterCountry, filterActive])

  const fetchSources = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (filterType !== 'all') params.append('source_type', filterType)
      if (filterCountry !== 'all') params.append('country', filterCountry)
      if (filterActive !== 'all') params.append('is_active', filterActive)

      const response = await axios.get(`${API_URL}/api/sources/?${params}`)
      setSources(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar fuentes')
      console.error('Error fetching sources:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/sources/stats/summary`)
      setStats(response.data)
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const handleToggleActive = async (sourceId: number) => {
    try {
      await axios.post(`${API_URL}/api/sources/${sourceId}/toggle`)
      fetchSources()
      fetchStats()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error al cambiar estado')
    }
  }

  const handleDelete = async (sourceId: number, name: string) => {
    if (!confirm(`¿Eliminar la fuente "${name}"?`)) return

    try {
      await axios.delete(`${API_URL}/api/sources/${sourceId}`)
      fetchSources()
      fetchStats()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error al eliminar fuente')
    }
  }

  const handleEdit = (source: Source) => {
    setEditingSource(source)
    setFormData({
      name: source.name,
      source_type: source.source_type,
      country: source.country,
      url: source.url,
      website_url: source.website_url || '',
      is_active: source.is_active,
      priority: source.priority,
      description: source.description || '',
      notes: source.notes || ''
    })
    setShowModal(true)
  }

  const handleAddNew = () => {
    setEditingSource(null)
    setFormData({
      name: '',
      source_type: 'rss_feed',
      country: 'ES',
      url: '',
      website_url: '',
      is_active: true,
      priority: 5,
      description: '',
      notes: ''
    })
    setShowModal(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      if (editingSource) {
        // Actualizar
        await axios.put(`${API_URL}/api/sources/${editingSource.id}`, formData)
      } else {
        // Crear
        await axios.post(`${API_URL}/api/sources/`, formData)
      }

      setShowModal(false)
      fetchSources()
      fetchStats()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error al guardar fuente')
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'rss_feed': return '📰'
      case 'instagram': return '📸'
      case 'twitter': return '🐦'
      case 'telegram': return '✈️'
      default: return '📡'
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'rss_feed': return 'RSS Feed'
      case 'instagram': return 'Instagram'
      case 'twitter': return 'Twitter/X'
      case 'telegram': return 'Telegram'
      default: return type
    }
  }

  const getCountryFlag = (country: string) => {
    switch (country) {
      case 'ES': return '🇪🇸'
      case 'BR': return '🇧🇷'
      case 'GI': return '🇬🇮'
      case 'INT': return '🌍'
      default: return ''
    }
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8 px-4">
        <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Gestión de Fuentes
          </h1>
          <p className="text-gray-600">
            Administra feeds RSS y cuentas de redes sociales
          </p>
        </div>

        {/* Estadísticas */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">Total</div>
              <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">Activas</div>
              <div className="text-2xl font-bold text-green-600">{stats.active}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">Inactivas</div>
              <div className="text-2xl font-bold text-gray-600">{stats.inactive}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">RSS Feeds</div>
              <div className="text-2xl font-bold text-purple-600">{stats.by_type.rss_feed || 0}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">Redes Sociales</div>
              <div className="text-2xl font-bold text-pink-600">
                {(stats.by_type.instagram || 0) + (stats.by_type.twitter || 0) + (stats.by_type.telegram || 0)}
              </div>
            </div>
          </div>
        )}

        {/* Controles */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="flex flex-wrap items-center gap-4 mb-4">
            {/* Filtro por tipo */}
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="all">Todos</option>
                <option value="rss_feed">📰 RSS Feed</option>
                <option value="instagram">📸 Instagram</option>
                <option value="twitter">🐦 Twitter/X</option>
                <option value="telegram">✈️ Telegram</option>
              </select>
            </div>

            {/* Filtro por país */}
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                País
              </label>
              <select
                value={filterCountry}
                onChange={(e) => setFilterCountry(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="all">Todos</option>
                <option value="ES">🇪🇸 España</option>
                <option value="BR">🇧🇷 Brasil</option>
                <option value="GI">🇬🇮 Gibraltar</option>
                <option value="INT">🌍 Internacional</option>
              </select>
            </div>

            {/* Filtro por estado */}
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado
              </label>
              <select
                value={filterActive}
                onChange={(e) => setFilterActive(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="all">Todos</option>
                <option value="true">✅ Activas</option>
                <option value="false">❌ Inactivas</option>
              </select>
            </div>

            {/* Botón añadir */}
            <div className="flex-1 min-w-[200px] flex items-end">
              <button
                onClick={handleAddNew}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                ➕ Añadir Fuente
              </button>
            </div>
          </div>
        </div>

        {/* Lista de fuentes */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Cargando fuentes...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
            {error}
          </div>
        ) : sources.length === 0 ? (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
            <p className="text-gray-600">No hay fuentes que coincidan con los filtros</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {sources.map((source) => (
              <div
                key={source.id}
                className={`bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow ${
                  !source.is_active ? 'opacity-60' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">{getTypeIcon(source.source_type)}</span>
                      <span className="text-2xl">{getCountryFlag(source.country)}</span>
                      <h3 className="text-xl font-semibold text-gray-900">
                        {source.name}
                      </h3>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        source.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {source.is_active ? 'Activa' : 'Inactiva'}
                      </span>
                      <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-medium">
                        Prioridad: {source.priority}/10
                      </span>
                    </div>

                    {source.description && (
                      <p className="text-gray-600 text-sm mb-2">{source.description}</p>
                    )}

                    <div className="flex flex-wrap gap-4 text-sm text-gray-500 mb-2">
                      <span>📡 {getTypeLabel(source.source_type)}</span>
                      <span>🌐 <a href={source.url} target="_blank" rel="noopener noreferrer"
                                    className="text-blue-600 hover:underline">
                        {source.url.length > 50 ? source.url.substring(0, 50) + '...' : source.url}
                      </a></span>
                    </div>

                    <div className="flex gap-4 text-xs text-gray-500">
                      <span>Scrapeos: {source.scrape_count}</span>
                      <span>Alertas: {source.alert_count}</span>
                      {source.last_scraped && (
                        <span>Último: {new Date(source.last_scraped).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>

                  {/* Acciones */}
                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={() => handleToggleActive(source.id)}
                      className={`px-3 py-1 rounded text-sm font-medium ${
                        source.is_active
                          ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                          : 'bg-green-100 text-green-800 hover:bg-green-200'
                      }`}
                    >
                      {source.is_active ? 'Desactivar' : 'Activar'}
                    </button>
                    <button
                      onClick={() => handleEdit(source)}
                      className="px-3 py-1 bg-blue-100 text-blue-800 rounded text-sm font-medium hover:bg-blue-200"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(source.id, source.name)}
                      className="px-3 py-1 bg-red-100 text-red-800 rounded text-sm font-medium hover:bg-red-200"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal para añadir/editar */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <h2 className="text-2xl font-bold mb-4">
                  {editingSource ? 'Editar Fuente' : 'Añadir Fuente'}
                </h2>

                <form onSubmit={handleSubmit}>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Nombre *
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        placeholder="Ej: Puntos Viajeros"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Tipo *
                      </label>
                      <select
                        value={formData.source_type}
                        onChange={(e) => setFormData({ ...formData, source_type: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      >
                        <option value="rss_feed">📰 RSS Feed</option>
                        <option value="instagram">📸 Instagram</option>
                        <option value="twitter">🐦 Twitter/X</option>
                        <option value="telegram">✈️ Telegram</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        País *
                      </label>
                      <select
                        value={formData.country}
                        onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      >
                        <option value="ES">🇪🇸 España</option>
                        <option value="BR">🇧🇷 Brasil</option>
                        <option value="GI">🇬🇮 Gibraltar</option>
                        <option value="INT">🌍 Internacional</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Prioridad (1-10) *
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="10"
                        required
                        value={formData.priority}
                        onChange={(e) => setFormData({ ...formData, priority: parseInt(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        URL *
                      </label>
                      <input
                        type="url"
                        required
                        value={formData.url}
                        onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        placeholder="https://..."
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Website URL (opcional)
                      </label>
                      <input
                        type="url"
                        value={formData.website_url}
                        onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        placeholder="https://..."
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Descripción
                      </label>
                      <textarea
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        rows={2}
                        placeholder="Breve descripción de la fuente"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Notas
                      </label>
                      <textarea
                        value={formData.notes}
                        onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        rows={2}
                        placeholder="Notas adicionales"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={formData.is_active}
                          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                          className="mr-2"
                        />
                        <span className="text-sm font-medium text-gray-700">
                          Fuente activa (se usará en scraping automático)
                        </span>
                      </label>
                    </div>
                  </div>

                  <div className="flex gap-3 mt-6">
                    <button
                      type="submit"
                      className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                    >
                      {editingSource ? 'Actualizar' : 'Crear'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowModal(false)}
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
      </div>
    </ProtectedRoute>
  )
}
