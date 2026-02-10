'use client'

import { useEffect, useState } from 'react'
import { usePathname } from 'next/navigation'
import { isAuthenticated, logout } from '@/lib/auth'

export default function Navigation() {
  const pathname = usePathname()
  const [authenticated, setAuthenticated] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    setAuthenticated(isAuthenticated())
  }, [pathname])

  // Don't show navigation on login page
  if (pathname === '/login') {
    return null
  }

  const navLinks = [
    { href: '/', label: 'Dashboard', icon: '📊' },
    { href: '/recommendations', label: 'Recomendaciones', icon: '💡' },
    { href: '/promotions', label: 'Promociones', icon: '🎁' },
    { href: '/sources', label: 'Fuentes', icon: '📰' },
    { href: '/calculator', label: 'Calculadora', icon: '🧮' },
    { href: '/balances', label: 'Mis Saldos', icon: '💰' },
  ]

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl sm:text-2xl font-bold text-primary-600">
              Millajem
            </h1>
            <span className="hidden sm:inline ml-3 text-sm text-gray-500">
              Gestión de Puntos y Avios
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-2 lg:space-x-4">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-gray-700 hover:text-primary-600 px-2 lg:px-3 py-2 rounded-md text-sm font-medium whitespace-nowrap"
              >
                <span className="hidden lg:inline">{link.label}</span>
                <span className="lg:hidden">{link.icon}</span>
              </a>
            ))}
            {authenticated && (
              <button
                onClick={logout}
                className="bg-red-600 text-white px-3 lg:px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 whitespace-nowrap"
              >
                Salir
              </button>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              aria-expanded="false"
            >
              <span className="sr-only">Abrir menú</span>
              {!mobileMenuOpen ? (
                <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-gray-700 hover:text-primary-600 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="mr-2">{link.icon}</span>
                {link.label}
              </a>
            ))}
            {authenticated && (
              <button
                onClick={() => {
                  logout()
                  setMobileMenuOpen(false)
                }}
                className="w-full text-left bg-red-600 text-white px-3 py-2 rounded-md text-base font-medium hover:bg-red-700"
              >
                Salir
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
