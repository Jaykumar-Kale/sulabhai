import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import { MessageCircle, ClipboardCheck, GraduationCap, Bookmark } from 'lucide-react'

export default function Dashboard() {
  const { user } = useAuth()
  const cards = [
    { to: '/assistant', icon: MessageCircle, title: 'AI सहाय्यकाशी बोला', desc: 'मराठीत प्रश्न विचारा' },
    { to: '/eligibility', icon: ClipboardCheck, title: 'पात्रता तपासा', desc: 'योजना/शिष्यवृत्तीसाठी' },
    { to: '/scholarships', icon: GraduationCap, title: 'शिष्यवृत्ती शोधा', desc: 'तुमच्यासाठी योग्य शिष्यवृत्ती' },
    { to: '/bookmarks', icon: Bookmark, title: 'जतन केलेले', desc: 'तुमच्या आवडीच्या नोंदी' },
  ]
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-1">नमस्कार, {user?.name}</h1>
      <p className="text-gray-500 mb-6">भूमिका: {user?.role}</p>
      <div className="grid sm:grid-cols-2 gap-4">
        {cards.map(c => (
          <Link key={c.to} to={c.to} className="border rounded-lg p-5 hover:shadow-md">
            <c.icon className="text-navy mb-2" size={24} />
            <h3 className="font-semibold">{c.title}</h3>
            <p className="text-sm text-gray-500">{c.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
