import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('token')
}

export const setToken = (token: string) => {
  localStorage.setItem('token', token)
}

export const removeToken = () => {
  localStorage.removeItem('token')
}

export const isAuthenticated = (): boolean => {
  return !!getToken()
}

export const verifyToken = async (): Promise<boolean> => {
  const token = getToken()
  if (!token) return false

  try {
    await axios.post(
      `${API_URL}/api/auth/verify`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    return true
  } catch (err) {
    removeToken()
    return false
  }
}

export const logout = () => {
  removeToken()
  if (typeof window !== 'undefined') {
    window.location.href = '/login'
  }
}

// Add token to axios requests
export const configureAxiosAuth = () => {
  axios.interceptors.request.use((config) => {
    const token = getToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  // Handle 401 responses (token expired or invalid)
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401 && typeof window !== 'undefined') {
        removeToken()
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }
  )
}
