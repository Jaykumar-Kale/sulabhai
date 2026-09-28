import { useState, useRef, useEffect } from 'react'
import client from '../api/client'
import { Send, FileText } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'

interface Message {
  role: 'user' | 'assistant'
  content: string
  citations?: any[]
  confidence?: string
  next_steps?: string[]
}

export default function Assistant() {
  const { user } = useAuth()
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'नमस्कार! मी SulabhAI आहे. मला सरकारी योजना किंवा शिष्यवृत्तीबद्दल मराठीत प्रश्न विचारा.' },
  ])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState<string | undefined>()
  const [loading, setLoading] = useState(false)
  const [level, setLevel] = useState(1)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  if (!user) {
    return (
      <div className="max-w-md mx-auto text-center mt-20">
        <p className="mb-4">AI सहाय्यक वापरण्यासाठी कृपया लॉगिन करा.</p>
        <Link to="/login" className="bg-navy text-white px-4 py-2 rounded">लॉगिन करा</Link>
      </div>
    )
  }

  const send = async () => {
    if (!input.trim()) return
    const userMsg: Message = { role: 'user', content: input }
    setMessages(m => [...m, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await client.post('/chat', { session_id: sessionId, message: userMsg.content, readability_level: level })
      setSessionId(res.data.session_id)
      setMessages(m => [...m, {
        role: 'assistant', content: res.data.answer, citations: res.data.citations,
        confidence: res.data.confidence, next_steps: res.data.next_steps,
      }])
    } catch (e) {
      setMessages(m => [...m, { role: 'assistant', content: 'क्षमस्व, काहीतरी चूक झाली.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 flex flex-col h-[calc(100vh-70px)]">
      <div className="flex justify-between items-center mb-3">
        <h1 className="text-xl font-bold">AI सहाय्यक</h1>
        <select value={level} onChange={e => setLevel(Number(e.target.value))} className="border rounded px-2 py-1 text-sm">
          <option value={1}>अगदी सोपी भाषा</option>
          <option value={2}>सोपी भाषा</option>
          <option value={3}>मानक भाषा</option>
          <option value={4}>तपशीलवार</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-lg px-4 py-3 text-sm ${m.role === 'user' ? 'bg-navy text-white' : 'bg-gray-100'}`}>
              <p className="whitespace-pre-line">{m.content}</p>
              {m.citations && m.citations.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-300 space-y-1">
                  {m.citations.map((c, ci) => (
                    <div key={ci} className="flex items-center gap-1 text-xs text-gray-600">
                      <FileText size={12} /> {c.document_title} {c.page ? `· पान ${c.page}` : ''}
                    </div>
                  ))}
                </div>
              )}
              {m.confidence && (
                <span className={`text-xs mt-1 inline-block ${
                  m.confidence === 'high' ? 'text-green-600' : m.confidence === 'low' ? 'text-orange-600' : 'text-gray-500'
                }`}>विश्वासार्हता: {m.confidence}</span>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="text-sm text-gray-400">विचार करत आहे...</div>}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2 border-t pt-3">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="उदा. मी शेतकरी आहे, माझ्यासाठी कोणत्या योजना आहेत?"
          className="flex-1 border rounded px-3 py-2"
        />
        <button onClick={send} className="bg-navy text-white px-4 rounded flex items-center gap-1">
          <Send size={16} />
        </button>
      </div>
    </div>
  )
}
