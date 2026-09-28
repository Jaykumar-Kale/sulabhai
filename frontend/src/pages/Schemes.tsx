import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import client from '../api/client'

export default function Schemes() {
  const [q, setQ] = useState('')
  const { data, isLoading } = useQuery({
    queryKey: ['schemes', q],
    queryFn: async () => (await client.get('/schemes', { params: { q: q || undefined } })).data,
  })

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">सरकारी योजना</h1>
      <input placeholder="योजना शोधा..." value={q} onChange={e => setQ(e.target.value)}
        className="border rounded px-3 py-2 w-full mb-6" />
      {isLoading && <p>लोड होत आहे...</p>}
      <div className="grid md:grid-cols-2 gap-4">
        {data?.map((s: any) => (
          <Link key={s.id} to={`/schemes/${s.id}`} className="border rounded-lg p-4 hover:shadow-md block">
            <div className="flex justify-between items-start mb-1">
              <h3 className="font-semibold">{s.title_marathi || s.title}</h3>
              {s.is_demo && <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">DEMO</span>}
            </div>
            <p className="text-sm text-gray-500 mb-2">{s.department} · {s.category}</p>
            <p className="text-sm text-gray-700 line-clamp-2">{s.description_marathi}</p>
          </Link>
        ))}
      </div>
      {data?.length === 0 && <p className="text-gray-500">कोणतीही योजना सापडली नाही.</p>}
    </div>
  )
}
