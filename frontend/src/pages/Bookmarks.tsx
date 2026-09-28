import { useQuery } from '@tanstack/react-query'
import client from '../api/client'

export default function Bookmarks() {
  const { data } = useQuery({
    queryKey: ['bookmarks'],
    queryFn: async () => (await client.get('/bookmarks')).data,
  })
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">जतन केलेल्या नोंदी</h1>
      {data?.length === 0 && <p className="text-gray-500">अजून काहीही जतन केलेले नाही.</p>}
      <div className="space-y-2">
        {data?.map((b: any) => (
          <div key={b.id} className="border rounded p-3 text-sm">{b.item_type} — {b.item_id}</div>
        ))}
      </div>
    </div>
  )
}
