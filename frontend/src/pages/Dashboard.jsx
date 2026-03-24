import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Play, Clock, Zap, Star, MoreHorizontal, 
  Home, Calendar, Activity, Utensils, User, 
  Brain, RefreshCw 
} from 'lucide-react';
import { Coffee } from 'lucide-react';

export default function Dashboard({ data }) {
  const location = useLocation();
  const navigate = useNavigate();
  const [isDietLoading, setIsDietLoading] = useState(false);

  // Estados locais para dados (caso venham da API e não do state)
  const [treino, setTreino] = useState(location.state?.treinoData || null);
  const [userId, setUserId] = useState(location.state?.userId || localStorage.getItem('marombai_user_id'));
  const [userProfile, setUserProfile] = useState(location.state?.userProfile || null);
  const [loadingData, setLoadingData] = useState(!treino); // Se não tem treino no state, carrega
  
  // Efeito para buscar dados se o usuário deu F5 ou veio do Login
  useEffect(() => {
    const fetchData = async () => {
      if (!treino && userId) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/user/${userId}/dashboard`);
          if (response.ok) {
            const data = await response.json();
            setTreino(data.treino);
            setUserProfile(data.user); // Perfil básico
            // Se quiser carregar a dieta também, pode setar aqui
          }
        } catch (error) {
          console.error("Erro ao buscar dados do dashboard:", error);
        } finally {
          setLoadingData(false);
        }
      } else if (!userId) {
        setLoadingData(false);
      }
    };

    fetchData();
  }, [userId, treino]);

  if (loadingData) {
    return (
        <div className="h-screen flex flex-col items-center justify-center bg-dark-bg text-white">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-neon-green mb-4"></div>
            <p className="text-gray-400">Carregando seu perfil...</p>
        </div>
    );
  }

  // Se não tiver treino nenhum (usuário tentou acessar /dashboard direto), manda voltar
  if (!treino) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-dark-bg text-white gap-4">
        <p className="text-gray-400">Nenhum treino encontrado. Gere um novo ou faça login.</p>
        <button 
          onClick={() => navigate('/login')} 
          className="text-neon-green hover:underline font-bold"
        >
          Ir para Login
        </button>
      </div>
    );
  }

  const handleGenerateDiet = async () => {
    if (!userId || !userProfile) {
      alert("Dados do usuário não encontrados para gerar a dieta.");
      return;
    }
    setIsDietLoading(true);

    const dietPayload = {
      user_id: userId,
      objetivo: userProfile.objetivo,
      restricoes: userProfile.restricoes,
      preferencias: [], // Pode adicionar no futuro
      dieta: userProfile.dieta,
      suplementos: userProfile.suplementos,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/gerar-dieta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dietPayload),
      });

      const dietData = await response.json();

      if (response.ok) {
        navigate('/dieta', { state: { dietData: dietData.dieta } });
      } else {
        throw new Error(dietData.detail || "Falha ao gerar dieta.");
      }
    } catch (error) {
      console.error("Erro ao gerar dieta:", error);
      alert(`Erro: ${error.message}`);
    } finally {
      setIsDietLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg text-white pb-24 font-sans">
      
      {isDietLoading && (
        <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex flex-col items-center justify-center animate-fade-in">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-400 mb-6"></div>
          <h2 className="text-2xl font-bold text-white animate-pulse">Montando sua Dieta...</h2>
        </div>
      )}

      {/* Topo / Header */}
      <header className="p-6 flex justify-between items-center bg-gradient-to-b from-black/50 to-transparent sticky top-0 z-10 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gray-700 overflow-hidden border-2 border-neon-green">
            <img src="https://github.com/shadcn.png" alt="Avatar" />
          </div>
          <div>
            <h1 className="font-bold text-lg">Olá, {userProfile?.nome || localStorage.getItem('marombai_user_nome') || "Maromba"} 👋</h1>
            <p className="text-xs text-gray-400">Hora do show!</p>
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
          <p className="text-sm text-gray-300 leading-relaxed italic">
            "{treino.aiInsight || treino.ai_insight || "Foco total no objetivo! Continue treinando pesado."}"
          </p>
        </div>

        {/* Cabeçalho do Treino */}
        <div>
          <div className="flex justify-between items-end mb-4">
            <div>
              <h2 className="text-3xl font-bold text-white mb-1 leading-tight">{treino.titulo || "Treino Personalizado"}</h2>
              <span className="text-neon-green text-sm font-medium bg-neon-green/10 px-3 py-1 rounded-full">
                {treino.foco || "Geral"}
              </span>
            </div>
            <button className="text-xs text-gray-500 underline">Personalizar</button>
          </div>

          {/* Stats Row */}
          <div className="flex gap-3 mb-6">
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Clock size={14} className="text-neon-green" /> {treino.duracao || "60 min"}
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Zap size={14} className="text-yellow-500" /> {treino.intensidade || "Média"}
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-400">
              <Star size={14} className="text-purple-500" /> {treino.xp || "100"} XP
            </div>
          </div>
        </div>

        {/* Lista de Exercícios */}
        <div className="space-y-4">
          <div className="flex justify-between items-center text-xs text-gray-500 uppercase tracking-wider font-bold">
            <span>Exercícios ({treino.exercicios?.length || 0})</span>
            <span className="flex items-center gap-1"><RefreshCw size={12}/> Trocas disponíveis</span>
          </div>

          {treino.exercicios && Array.isArray(treino.exercicios) && treino.exercicios.map((ex, index) => (
            <div key={ex.id || index} className="bg-card-bg rounded-xl p-4 flex gap-4 border border-gray-800 hover:border-gray-600 transition-colors cursor-pointer group">
              {/* Imagem do Exercicio */}
              <div className="w-20 h-20 rounded-lg bg-gray-800 overflow-hidden flex-shrink-0 relative">
                {/* Fallback de imagem caso a API mande vazio */}
                <img 
                  src={ex.img || "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&q=80"} 
                  alt={ex.nome} 
                  className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" 
                />
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
                  <span className="text-gray-400">{ex.carga}</span>
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

          <button 
            onClick={handleGenerateDiet}
            disabled={isDietLoading}
            className="flex flex-col items-center gap-1 text-gray-500 hover:text-white transition-colors disabled:opacity-50"
          >
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