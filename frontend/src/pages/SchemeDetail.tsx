import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import client from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function SchemeDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const { data: scheme } = useQuery({
    queryKey: ['scheme', id],
    queryFn: async () => (await client.get(`/schemes/${id}`)).data,
  })

  const bookmark = useMutation({
    mutationFn: async () => client.post('/bookmarks', { item_type: 'scheme', item_id: id }),
  })

  if (!scheme) return <div className="max-w-3xl mx-auto px-4 py-8">लोड होत आहे...</div>

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-1">{scheme.title_marathi || scheme.title}</h1>
      <p className="text-gray-500 mb-4">{scheme.department} · {scheme.category}</p>
      {scheme.is_demo && (
        <div className="bg-yellow-50 text-yellow-800 text-sm p-2 rounded mb-4">
          ही डेमो नोंद आहे — अधिकृत माहितीसाठी सरकारी संकेतस्थळ तपासा.
        </div>
      )}
      <Section title="वर्णन" text={scheme.description_marathi} />
      <Section title="पात्रता" text={scheme.eligibility_marathi} />
      <Section title="लाभ" text={scheme.benefits_marathi} />
      <Section title="आवश्यक कागदपत्रे" text={scheme.required_documents} />
      {scheme.official_url && (
        <a href={scheme.official_url} target="_blank" className="text-navy underline text-sm">अधिकृत संकेतस्थळ →</a>
      )}
      <div className="flex gap-3 mt-6">
        <Link to="/eligibility" className="bg-navy text-white px-4 py-2 rounded text-sm">पात्रता तपासा</Link>
        {user && (
          <button onClick={() => bookmark.mutate()} className="border px-4 py-2 rounded text-sm">
            {bookmark.isSuccess ? 'जतन केले ✓' : 'जतन करा'}
          </button>
        )}
      </div>
    </div>
  )
}

function Section({ title, text }: { title: string, text?: string }) {
  if (!text) return null
  return (
    <div className="mb-4">
      <h3 className="font-semibold mb-1">{title}</h3>
      <p className="text-gray-700 text-sm whitespace-pre-line">{text}</p>
    </div>
  )
}
