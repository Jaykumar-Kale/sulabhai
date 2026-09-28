import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Schemes from './pages/Schemes'
import SchemeDetail from './pages/SchemeDetail'
import Scholarships from './pages/Scholarships'
import Eligibility from './pages/Eligibility'
import Assistant from './pages/Assistant'
import Bookmarks from './pages/Bookmarks'
import Applications from './pages/Applications'
import Admin from './pages/Admin'

export default function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/schemes" element={<Schemes />} />
        <Route path="/schemes/:id" element={<SchemeDetail />} />
        <Route path="/scholarships" element={<Scholarships />} />
        <Route path="/eligibility" element={<Eligibility />} />
        <Route path="/assistant" element={<Assistant />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/bookmarks" element={<ProtectedRoute><Bookmarks /></ProtectedRoute>} />
        <Route path="/applications" element={<ProtectedRoute><Applications /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute adminOnly><Admin /></ProtectedRoute>} />
      </Routes>
    </AuthProvider>
  )
}
