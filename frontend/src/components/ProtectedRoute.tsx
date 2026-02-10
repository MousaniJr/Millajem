'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { isAuthenticated, verifyToken, configureAxiosAuth } from '@/lib/auth'

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [isVerifying, setIsVerifying] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      // Configure axios to use auth token
      configureAxiosAuth()

      // Check if token exists
      if (!isAuthenticated()) {
        router.push('/login')
        return
      }

      // Verify token is still valid
      const valid = await verifyToken()
      if (!valid) {
        router.push('/login')
        return
      }

      setIsVerifying(false)
    }

    checkAuth()
  }, [router])

  if (isVerifying) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-gray-600">Verificando autenticación...</p>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
