import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import client from '../api/client'

export default function Admin() {
  const { data: analytics } = useQuery({
    queryKey: ['admin-analytics'],
    queryFn: async () => (await client.get('/admin/analytics')).data,
  })
  const [title, setTitle] = useState('')
  const [department, setDepartment] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState('')

  const upload = async () => {
    if (!file || !title) return
    setStatus('अपलोड होत आहे...')
    const form = new FormData()
    form.append('file', file)
    try {
      await client.post(`/documents/upload?title=${encodeURIComponent(title)}&department=${encodeURIComponent(department)}`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setStatus('दस्तऐवज यशस्वीरित्या अपलोड व प्रक्रिया केला.')
    } catch (e: any) {
      setStatus('त्रुटी: ' + (e?.response?.data?.detail || 'अपलोड अयशस्वी'))
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        {analytics && Object.entries(analytics).map(([k, v]) => (
          <div key={k} className="border rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-navy">{v as any}</div>
            <div className="text-xs text-gray-500">{k}</div>
          </div>
        ))}
      </div>

      <div className="border rounded-lg p-5">
        <h2 className="font-semibold mb-3">दस्तऐवज अपलोड करा (PDF → OCR → RAG index)</h2>
        <div className="space-y-3">
          <input placeholder="शीर्षक" value={title} onChange={e => setTitle(e.target.value)} className="w-full border rounded px-3 py-2" />
          <input placeholder="विभाग" value={department} onChange={e => setDepartment(e.target.value)} className="w-full border rounded px-3 py-2" />
          <input type="file" accept="application/pdf" onChange={e => setFile(e.target.files?.[0] || null)} className="w-full" />
          <button onClick={upload} className="bg-navy text-white px-4 py-2 rounded">अपलोड व प्रक्रिया करा</button>
          {status && <p className="text-sm text-gray-600">{status}</p>}
        </div>
      </div>
    </div>
  )
}
