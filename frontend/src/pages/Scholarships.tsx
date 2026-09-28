import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import client from '../api/client'

export default function Scholarships() {
  const [income, setIncome] = useState('')
  const [educationLevel, setEducationLevel] = useState('')
  const [showMatches, setShowMatches] = useState(false)

  const { data: all } = useQuery({
    queryKey: ['scholarships'],
    queryFn: async () => (await client.get('/scholarships')).data,
  })

  const { data: matches, refetch } = useQuery({
    queryKey: ['scholarship-matches', income, educationLevel],
    queryFn: async () => (await client.get('/scholarships/matches', {
      params: { income: income || undefined, education_level: educationLevel || undefined },
    })).data,
    enabled: false,
  })

  const findMatches = () => {
    setShowMatches(true)
    refetch()
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">शिष्यवृत्ती शोधा</h1>

      <div className="border rounded-lg p-4 mb-8 bg-gray-50">
        <h2 className="font-semibold mb-3">तुमच्यासाठी योग्य शिष्यवृत्ती शोधा</h2>
        <div className="flex flex-wrap gap-3 mb-3">
          <input placeholder="वार्षिक कौटुंबिक उत्पन्न (₹)" value={income} onChange={e => setIncome(e.target.value)}
            className="border rounded px-3 py-2 flex-1 min-w-[200px]" />
          <select value={educationLevel} onChange={e => setEducationLevel(e.target.value)}
            className="border rounded px-3 py-2 flex-1 min-w-[200px]">
            <option value="">शिक्षण स्तर निवडा</option>
            <option value="undergraduate">पदवी (Undergraduate)</option>
            <option value="postgraduate">पदव्युत्तर (Postgraduate)</option>
            <option value="diploma">डिप्लोमा</option>
          </select>
        </div>
        <button onClick={findMatches} className="bg-indiagreen text-white px-4 py-2 rounded">जुळणाऱ्या शिष्यवृत्ती दाखवा</button>

        {showMatches && matches && (
          <div className="mt-4 space-y-2">
            {matches.length === 0 && <p className="text-sm text-gray-500">कोणतीही जुळणारी शिष्यवृत्ती सापडली नाही.</p>}
            {matches.map((m: any) => (
              <div key={m.item_id} className="bg-white border rounded p-3 text-sm">
                <div className="flex justify-between">
                  <strong>{m.item_title}</strong>
                  <span className={m.overall === 'LIKELY_MATCH' ? 'text-green-600' : 'text-yellow-600'}>
                    {m.overall === 'LIKELY_MATCH' ? 'शक्यतो जुळते' : 'अपुरी माहिती'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <h2 className="font-semibold mb-3">सर्व शिष्यवृत्ती</h2>
      <div className="grid md:grid-cols-2 gap-4">
        {all?.map((s: any) => (
          <div key={s.id} className="border rounded-lg p-4">
            <div className="flex justify-between items-start mb-1">
              <h3 className="font-semibold">{s.name_marathi || s.name}</h3>
              {s.is_demo && <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">DEMO</span>}
            </div>
            <p className="text-sm text-gray-500 mb-1">{s.provider}</p>
            {s.amount && <p className="text-sm">रक्कम: ₹{s.amount}</p>}
            {s.deadline && <p className="text-sm text-red-600">अंतिम तारीख: {s.deadline}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}
