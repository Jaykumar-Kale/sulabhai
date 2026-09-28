import { useQuery } from '@tanstack/react-query'
import client from '../api/client'

const statusLabels: Record<string, string> = {
  interested: 'स्वारस्य आहे', documents_pending: 'कागदपत्रे प्रलंबित', ready_to_apply: 'अर्ज करण्यास तयार',
  applied: 'अर्ज केला', verification: 'पडताळणी', approved: 'मंजूर', rejected: 'नाकारले', completed: 'पूर्ण',
}

export default function Applications() {
  const { data } = useQuery({
    queryKey: ['applications'],
    queryFn: async () => (await client.get('/applications')).data,
  })
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">माझे अर्ज</h1>
      {data?.length === 0 && <p className="text-gray-500">अजून कोणताही अर्ज ट्रॅक केलेला नाही.</p>}
      <div className="space-y-2">
        {data?.map((a: any) => (
          <div key={a.id} className="border rounded p-3 text-sm flex justify-between">
            <span>{a.item_type} — {a.item_id}</span>
            <span className="text-navy">{statusLabels[a.status] || a.status}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
