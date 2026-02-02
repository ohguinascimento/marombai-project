import React from 'react';
import { 
  Play, Clock, Zap, Star, MoreHorizontal, 
  Home, Calendar, Activity, Utensils, User, 
  Brain, RefreshCw 
} from 'lucide-react';

export default function Dashboard() {
  
  // Dados simulados (No futuro virão do Python)
  const treinoDoDia = {
    titulo: "Peito & Tríceps",
    foco: "Hipertrofia",
    duracao: "50 min",
    intensidade: "Alta",
    xp: 350,
    aiInsight: "Baseado na sua recuperação lenta de ontem, foquei em Carga e reduzi as repetições hoje.",
    exercicios: [
      {
        id: 1,
        nome: "Supino Inclinado",
        series: "4x10-12",
        carga: "40kg",
        img: "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&q=80" // Foto ilustrativa
      },
      {
        id: 2,
        nome: "Crucifixo com Halteres",
        series: "3x12-15",
        carga: "16kg",
        img: "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400&q=80"
      },
      {
        id: 3,
        nome: "Tríceps Corda",
        series: "4x12-15",
        carga: "25kg",
        img: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&q=80"
      }
    ]
  };

  return (
    <div className="min-h-screen bg-dark-bg text-white pb-24 font-sans">
      
      {/* Topo / Header */}
      <header className="p-6 flex justify-between items-center bg-gradient-to-b from-black/50 to-transparent sticky top-0 z-10 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gray-700 overflow-hidden border-2 border-neon-green">
            <img src="https://github.com/shadcn.png" alt="Avatar" />
          </div>
          <div>
            <h1 className="font-bold text-lg">Olá, Bruno 👋</h1>
            <p className="text-xs text-gray-400">Vamos esmagar hoje?</p>
          </div>
        </div>
        <button className="p-2 bg-gray-800 rounded-full text-gray-400">
          <Clock size={20} />
        </button>
      </header>

      <div className="px-6 space-y-6">

        {/* Card de Insight da IA (O Cérebro) */}
        <div className="relative overflow-hidden rounded-2xl bg-card-bg border border-gray-800 p-5 group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-neon-green/10 blur-3xl rounded-full -mr-10 -mt-10 transition-all group-hover:bg-neon-green/20"></div>
          
          <div className="flex items-center gap-2 mb-2 text-neon-green">
            <Brain size={18} />
            <span className="text-xs font-bold tracking-wider uppercase">Análise da IA</span>
          </div>
          <p className="text-sm text-gray-300 leading-relaxed">
            "{treinoDoDia.aiInsight}"
          </p>
        </div>

        {/* Cabeçalho do Treino */}
        <div>
          <div className="flex justify-between items-end mb-4">
            <div>
              <h2 className="text-3xl font-bold text-white mb-1">{treinoDoDia.titulo}</h2>
              <span className="text-neon-green text-sm font-medium bg-neon-green/10 px-3 py-1 rounded-full">
                {treinoDoDia.foco}
              </span>
            </div>
            <button className="text-xs text-gray-500 underline">Personalizar</button>
          </div>

          {/* Stats Row */}
          <div className="flex gap-3 mb-6">
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Clock size={14} className="text-neon-green" /> {treinoDoDia.duracao}
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Zap size={14} className="text-yellow-500" /> {treinoDoDia.intensidade}
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Star size={14} className="text-purple-500" /> {treinoDoDia.xp} XP
            </div>
          </div>
        </div>

        {/* Lista de Exercícios */}
        <div className="space-y-4">
          <div className="flex justify-between items-center text-xs text-gray-500 uppercase tracking-wider font-bold">
            <span>Exercícios</span>
            <span className="flex items-center gap-1"><RefreshCw size={12}/> Trocas: 3/3</span>
          </div>

          {treinoDoDia.exercicios.map((ex) => (
            <div key={ex.id} className="bg-card-bg rounded-xl p-4 flex gap-4 border border-gray-800 hover:border-gray-600 transition-colors cursor-pointer group">
              {/* Imagem do Exercicio */}
              <div className="w-20 h-20 rounded-lg bg-gray-800 overflow-hidden flex-shrink-0 relative">
                <img src={ex.img} alt={ex.nome} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                  <Play size={20} className="text-white drop-shadow-lg" fill="white" />
                </div>
              </div>

              {/* Detalhes */}
              <div className="flex-1 flex flex-col justify-center">
                <h3 className="font-bold text-white mb-1">{ex.nome}</h3>
                <div className="flex gap-3 text-sm">
                  <span className="text-neon-green font-mono">{ex.series}</span>
                  <span className="text-gray-500">|</span>
                  <span className="text-gray-400">Carga: {ex.carga}</span>
                </div>
              </div>

              <div className="flex items-center text-gray-600">
                <MoreHorizontal size={20} />
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Botão Flutuante Gigante (Iniciar Treino) */}
      <div className="fixed bottom-24 left-0 w-full px-6 z-20">
        <button className="w-full bg-neon-green text-black font-bold text-lg py-4 rounded-2xl shadow-[0_0_20px_rgba(0,255,148,0.4)] hover:shadow-[0_0_30px_rgba(0,255,148,0.6)] hover:scale-[1.02] transition-all flex items-center justify-center gap-2">
          INICIAR TREINO <Zap size={20} fill="black" />
        </button>
      </div>

      {/* Bottom Navigation (Menu Inferior) */}
      <nav className="fixed bottom-0 w-full bg-[#121212]/95 backdrop-blur-md border-t border-gray-800 py-4 px-6 z-30">
        <div className="flex justify-between items-center max-w-md mx-auto">
          <button className="flex flex-col items-center gap-1 text-neon-green">
            <Home size={20} />
            <span className="text-[10px] font-bold">Treino</span>
          </button>
          
          <button className="flex flex-col items-center gap-1 text-gray-500 hover:text-white transition-colors">
            <Calendar size={20} />
            <span className="text-[10px] font-medium">Diário</span>
          </button>

          <button className="flex flex-col items-center gap-1 text-gray-500 hover:text-white transition-colors">
            <Activity size={20} />
            <span className="text-[10px] font-medium">Evolução</span>
          </button>

          <button className="flex flex-col items-center gap-1 text-gray-500 hover:text-white transition-colors">
            <Utensils size={20} />
            <span className="text-[10px] font-medium">Dieta</span>
          </button>

          <button className="flex flex-col items-center gap-1 text-gray-500 hover:text-white transition-colors">
            <User size={20} />
            <span className="text-[10px] font-medium">Perfil</span>
          </button>
        </div>
      </nav>

    </div>
  );
}