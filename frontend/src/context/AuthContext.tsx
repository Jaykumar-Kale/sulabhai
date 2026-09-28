import React, { createContext, useContext, useState, ReactNode } from 'react'
import client from '../api/client'

interface User {
  id: string
  name: string
  email: string
  role: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string, role: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem('sulabhai_user')
    return stored ? JSON.parse(stored) : null
  })

  const persist = (token: string, u: User) => {
    localStorage.setItem('sulabhai_token', token)
    localStorage.setItem('sulabhai_user', JSON.stringify(u))
    setUser(u)
  }

  const login = async (email: string, password: string) => {
    const res = await client.post('/auth/login', { email, password })
    persist(res.data.access_token, res.data.user)
  }

  const register = async (name: string, email: string, password: string, role: string) => {
    const res = await client.post('/auth/register', { name, email, password, role })
    persist(res.data.access_token, res.data.user)
  }

  const logout = () => {
    localStorage.removeItem('sulabhai_token')
    localStorage.removeItem('sulabhai_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
