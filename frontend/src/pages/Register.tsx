import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('citizen')
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await register(name, email, password, role)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'नोंदणी अयशस्वी झाली.')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 p-6 border rounded-xl">
      <h1 className="text-2xl font-bold mb-4">नोंदणी करा</h1>
      {error && <div className="bg-red-50 text-red-600 text-sm p-2 rounded mb-3">{error}</div>}
      <form onSubmit={submit} className="space-y-3">
        <input required placeholder="पूर्ण नाव" value={name} onChange={e => setName(e.target.value)}
          className="w-full border rounded px-3 py-2" />
        <input required type="email" placeholder="ईमेल" value={email} onChange={e => setEmail(e.target.value)}
          className="w-full border rounded px-3 py-2" />
        <input required type="password" placeholder="पासवर्ड" value={password} onChange={e => setPassword(e.target.value)}
          className="w-full border rounded px-3 py-2" />
        <select value={role} onChange={e => setRole(e.target.value)} className="w-full border rounded px-3 py-2">
          <option value="citizen">नागरिक</option>
          <option value="student">विद्यार्थी</option>
          <option value="farmer">शेतकरी</option>
          <option value="ngo">NGO</option>
        </select>
        <button className="w-full bg-navy text-white py-2 rounded font-medium">नोंदणी करा</button>
      </form>
      <p className="text-sm mt-4">आधीच खाते आहे? <Link to="/login" className="text-navy underline">लॉगिन करा</Link></p>
    </div>
  )
}
