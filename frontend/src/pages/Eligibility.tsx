import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import client from '../api/client'

export default function Eligibility() {
  const [type, setType] = useState<'scheme' | 'scholarship'>('scheme')
  const [itemId, setItemId] = useState('')
  const [age, setAge] = useState('')
  const [income, setIncome] = useState('')
  const [category, setCategory] = useState('')
  const [occupation, setOccupation] = useState('')

  const { data: items } = useQuery({
    queryKey: ['elig-items', type],
    queryFn: async () => (await client.get(type === 'scheme' ? '/schemes' : '/scholarships')).data,
  })

  const check = useMutation({
    mutationFn: async () => {
      const payload: any = {
        age: age ? Number(age) : undefined,
        income: income ? Number(income) : undefined,
        category: category || undefined,
        occupation: occupation || undefined,
      }
      if (type === 'scheme') payload.scheme_id = itemId
      else payload.scholarship_id = itemId
      return (await client.post('/eligibility/check', payload)).data
    },
  })

  const overallLabel: Record<string, string> = {
    LIKELY_MATCH: 'तुम्ही प्राथमिक निकषांशी जुळत असण्याची शक्यता आहे',
    LIKELY_NOT_MATCH: 'तुम्ही सध्याच्या निकषांशी जुळत नसण्याची शक्यता आहे',
    INSUFFICIENT_INFO: 'तपासणीसाठी पुरेशी माहिती उपलब्ध नाही',
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-1">प्राथमिक पात्रता तपासणी</h1>
      <p className="text-sm text-gray-500 mb-6">ही केवळ प्राथमिक तपासणी आहे, अधिकृत निर्णय नाही.</p>

      <div className="border rounded-lg p-5 space-y-3">
        <div className="flex gap-2">
          <button onClick={() => { setType('scheme'); setItemId('') }}
            className={`px-3 py-1.5 rounded text-sm ${type === 'scheme' ? 'bg-navy text-white' : 'bg-gray-100'}`}>योजना</button>
          <button onClick={() => { setType('scholarship'); setItemId('') }}
            className={`px-3 py-1.5 rounded text-sm ${type === 'scholarship' ? 'bg-navy text-white' : 'bg-gray-100'}`}>शिष्यवृत्ती</button>
        </div>

        <select value={itemId} onChange={e => setItemId(e.target.value)} className="w-full border rounded px-3 py-2">
          <option value="">-- निवडा --</option>
          {items?.map((it: any) => (
            <option key={it.id} value={it.id}>{it.title_marathi || it.name_marathi || it.title || it.name}</option>
          ))}
        </select>

        <div className="grid grid-cols-2 gap-3">
          <input placeholder="वय" value={age} onChange={e => setAge(e.target.value)} className="border rounded px-3 py-2" />
          <input placeholder="वार्षिक उत्पन्न (₹)" value={income} onChange={e => setIncome(e.target.value)} className="border rounded px-3 py-2" />
          <input placeholder="प्रवर्ग (उदा. OPEN, OBC)" value={category} onChange={e => setCategory(e.target.value)} className="border rounded px-3 py-2" />
          <select value={occupation} onChange={e => setOccupation(e.target.value)} className="border rounded px-3 py-2">
            <option value="">व्यवसाय/गट निवडा</option>
            <option value="student">विद्यार्थी</option>
            <option value="farmer">शेतकरी</option>
            <option value="citizen">नागरिक</option>
          </select>
        </div>

        <button disabled={!itemId} onClick={() => check.mutate()} className="w-full bg-indiagreen text-white py-2 rounded disabled:opacity-50">
          पात्रता तपासा
        </button>
      </div>

      {check.data && (
        <div className="mt-6 border rounded-lg p-5">
          <h2 className="font-semibold mb-2">{check.data.item_title}</h2>
          <p className={`font-medium mb-3 ${
            check.data.overall === 'LIKELY_MATCH' ? 'text-green-600' :
            check.data.overall === 'LIKELY_NOT_MATCH' ? 'text-red-600' : 'text-yellow-600'
          }`}>{overallLabel[check.data.overall]}</p>
          <div className="space-y-1 mb-3">
            {check.data.criteria.map((c: any, i: number) => (
              <div key={i} className="flex justify-between text-sm border-b py-1">
                <span>{c.criterion}</span>
                <span className={
                  c.result === 'MATCH' ? 'text-green-600' : c.result === 'NOT_MATCH' ? 'text-red-600' : 'text-gray-400'
                }>{c.result}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500">{check.data.disclaimer}</p>
        </div>
      )}
    </div>
  )
}
