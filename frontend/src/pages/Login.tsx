import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'लॉगिन अयशस्वी झाले.')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 p-6 border rounded-xl">
      <h1 className="text-2xl font-bold mb-1">लॉगिन करा</h1>
      <p className="text-sm text-gray-500 mb-4">Demo: student@sulabhai.demo / student123</p>
      {error && <div className="bg-red-50 text-red-600 text-sm p-2 rounded mb-3">{error}</div>}
      <form onSubmit={submit} className="space-y-3">
        <input required type="email" placeholder="ईमेल" value={email} onChange={e => setEmail(e.target.value)}
          className="w-full border rounded px-3 py-2" />
        <input required type="password" placeholder="पासवर्ड" value={password} onChange={e => setPassword(e.target.value)}
          className="w-full border rounded px-3 py-2" />
        <button className="w-full bg-navy text-white py-2 rounded font-medium">लॉगिन</button>
      </form>
      <p className="text-sm mt-4">खाते नाही? <Link to="/register" className="text-navy underline">नोंदणी करा</Link></p>
    </div>
  )
}
