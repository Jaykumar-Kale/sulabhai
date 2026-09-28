import { Link } from 'react-router-dom'
import { MessageCircle, ClipboardCheck, GraduationCap, ShieldCheck, Accessibility, FileSearch } from 'lucide-react'

const features = [
  { icon: MessageCircle, title: 'AI सहाय्यक', text: 'तुमचा प्रश्न मराठीत विचारा आणि सोप्या भाषेत उत्तर मिळवा.' },
  { icon: FileSearch, title: 'स्रोत-आधारित उत्तरे', text: 'प्रत्येक उत्तर अधिकृत दस्तऐवजाच्या संदर्भासह दिले जाते.' },
  { icon: ClipboardCheck, title: 'पात्रता तपासा', text: 'योजनेसाठी तुमची प्राथमिक पात्रता तपासा.' },
  { icon: GraduationCap, title: 'शिष्यवृत्ती शोध', text: 'तुमच्या माहितीनुसार योग्य शिष्यवृत्ती शोधा.' },
  { icon: Accessibility, title: 'सुलभ वापर', text: 'मोठे फॉन्ट, सोपी भाषा, मोबाईल-फ्रेंडली रचना.' },
  { icon: ShieldCheck, title: 'विश्वासार्हता', text: 'माहितीची पडताळणी स्थिती व शेवटची तपासणी तारीख दाखवली जाते.' },
]

export default function Landing() {
  return (
    <div>
      <section className="bg-gradient-to-b from-navy to-navy/90 text-white py-16 px-4 text-center">
        <h1 className="text-3xl md:text-5xl font-bold mb-4">सरकारी योजना समजून घेणे आता सोपे.</h1>
        <p className="max-w-2xl mx-auto text-white/85 mb-8 text-lg">
          तुमचा प्रश्न मराठीत विचारा. अधिकृत कागदपत्रांमधून माहिती शोधा आणि सोप्या भाषेत समजून घ्या.
        </p>
        <div className="flex flex-wrap gap-3 justify-center">
          <Link to="/assistant" className="bg-saffron text-navy font-semibold px-6 py-3 rounded-lg">योजनेबद्दल विचारा</Link>
          <Link to="/eligibility" className="bg-white/10 border border-white/40 px-6 py-3 rounded-lg">पात्रता तपासा</Link>
          <Link to="/scholarships" className="bg-indiagreen px-6 py-3 rounded-lg">शिष्यवृत्ती शोधा</Link>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 py-14 grid sm:grid-cols-2 md:grid-cols-3 gap-6">
        {features.map((f) => (
          <div key={f.title} className="border rounded-xl p-5 hover:shadow-md transition">
            <f.icon className="text-navy mb-3" size={28} />
            <h3 className="font-semibold text-lg mb-1">{f.title}</h3>
            <p className="text-gray-600 text-sm">{f.text}</p>
          </div>
        ))}
      </section>

      <section className="bg-gray-50 py-10 px-4">
        <div className="max-w-3xl mx-auto text-center text-sm text-gray-600 border rounded-lg p-5 bg-white">
          <ShieldCheck className="inline mb-2 text-indiagreen" size={22} />
          <p>
            हे व्यासपीठ सरकारी संस्था नाही. येथे दिलेली माहिती अधिकृत स्रोतांवर आधारित माहिती समजून घेण्यास
            मदत करण्यासाठी आहे. अंतिम पात्रता आणि अर्जाच्या अटी संबंधित सरकारी विभागाच्या अधिकृत संकेतस्थळावर तपासा.
          </p>
        </div>
      </section>
    </div>
  )
}
