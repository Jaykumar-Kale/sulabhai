import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Landmark, MessageCircle, GraduationCap, ClipboardCheck, Bookmark, LogOut } from 'lucide-react'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <nav className="bg-navy text-white sticky top-0 z-10 shadow-md">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <Landmark size={22} />
          SulabhAI
        </Link>
        <div className="hidden md:flex items-center gap-5 text-sm">
          <Link to="/schemes" className="hover:text-saffron">योजना</Link>
          <Link to="/scholarships" className="hover:text-saffron">शिष्यवृत्ती</Link>
          <Link to="/eligibility" className="hover:text-saffron">पात्रता तपासा</Link>
          <Link to="/assistant" className="flex items-center gap-1 hover:text-saffron">
            <MessageCircle size={16} /> सहाय्यक
          </Link>
          {user && (
            <>
              <Link to="/bookmarks" className="flex items-center gap-1 hover:text-saffron">
                <Bookmark size={16} /> जतन केलेले
              </Link>
              <Link to="/applications" className="flex items-center gap-1 hover:text-saffron">
                <ClipboardCheck size={16} /> अर्ज
              </Link>
              {user.role === 'admin' && (
                <Link to="/admin" className="hover:text-saffron">Admin</Link>
              )}
            </>
          )}
        </div>
        <div className="flex items-center gap-3">
          {user ? (
            <button
              onClick={() => { logout(); navigate('/') }}
              className="flex items-center gap-1 text-sm bg-white/10 px-3 py-1.5 rounded hover:bg-white/20"
            >
              <LogOut size={14} /> {user.name}
            </button>
          ) : (
            <>
              <Link to="/login" className="text-sm px-3 py-1.5 rounded hover:bg-white/10">लॉगिन</Link>
              <Link to="/register" className="text-sm bg-saffron px-3 py-1.5 rounded font-medium">नोंदणी</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
