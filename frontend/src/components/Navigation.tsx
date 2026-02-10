'use client'

import { useEffect, useState } from 'react'
import { usePathname } from 'next/navigation'
import { isAuthenticated, logout } from '@/lib/auth'

export default function Navigation() {
  const pathname = usePathname()
  const [authenticated, setAuthenticated] = useState(false)

  useEffect(() => {
    setAuthenticated(isAuthenticated())
  }, [pathname])

  // Don't show navigation on login page
  if (pathname === '/login') {
    return null
  }

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-primary-600">
              Millajem
            </h1>
            <span className="ml-3 text-sm text-gray-500">
              Gestión de Puntos y Avios
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="/" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </a>
            <a href="/recommendations" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Recomendaciones
            </a>
            <a href="/promotions" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Promociones
            </a>
            <a href="/sources" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Fuentes
            </a>
            <a href="/calculator" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Calculadora
            </a>
            <a href="/balances" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Mis Saldos
            </a>
            {authenticated && (
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
              >
                Salir
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
