import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Activity, TrendingUp, Calendar, Clock, Zap, Trophy } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL;

export default function EvolutionPage() {
  const navigate = useNavigate();
  const userId = localStorage.getItem('marombai_user_id');
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvolution = async () => {
      try {
        const response = await fetch(`${API_URL}/user/${userId}/evolution`);
        if (response.ok) {
          const data = await response.json();
          setLogs(data);
        }
      } catch (error) {
        console.error("Erro ao buscar evolução:", error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchEvolution();
    } else {
      setLoading(false);
    }
  }, [userId]);

  if (loading) return <div className="min-h-screen bg-dark-bg flex items-center justify-center text-neon-green font-black italic">ANALISANDO PERFORMANCE...</div>;

  const totalMinutes = logs.reduce((acc, log) => acc + (log.duracao || 0), 0);
  const avgEffort = logs.length > 0 ? (logs.reduce((acc, log) => acc + (log.esforco || 0), 0) / logs.length).toFixed(1) : 0;

  // Lógica para o gráfico de barras (Últimos 7 treinos)
  const chartData = logs.slice(-7);
  const maxDuration = chartData.length > 0 ? Math.max(...chartData.map(d => d.duracao || 0), 1) : 1;

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 pb-24 font-sans">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <button onClick={() => navigate(-1)} className="p-2 bg-gray-900 rounded-xl text-gray-400">
          <ChevronLeft size={24} />
        </button>
        <h1 className="text-2xl font-bold uppercase italic tracking-tighter">Sua Evolução</h1>
      </div>

      {logs.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
          <div className="w-20 h-20 bg-gray-900 rounded-full flex items-center justify-center text-gray-700 border border-gray-800">
            <Activity size={40} />
          </div>
          <p className="text-gray-500 font-medium">Nenhum treino registrado ainda.<br/>A primeira gota de suor é a mais difícil.</p>
          <button onClick={() => navigate('/dashboard')} className="bg-neon-green text-black px-8 py-3 rounded-xl font-black uppercase text-sm">Iniciar Jornada</button>
        </div>
      ) : (
        <div className="space-y-6 animate-fade-in">
          {/* Cards de Destaque */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-card-bg p-5 rounded-3xl border border-gray-800 relative overflow-hidden group">
                <div className="absolute -right-2 -top-2 text-neon-green/5 group-hover:text-neon-green/10 transition-colors"><Trophy size={80}/></div>
                <p className="text-[10px] text-gray-500 uppercase font-black mb-1 tracking-widest">Treinos</p>
                <p className="text-4xl font-black text-neon-green font-mono">{logs.length}</p>
            </div>
            <div className="bg-card-bg p-5 rounded-3xl border border-gray-800">
                <p className="text-[10px] text-gray-500 uppercase font-black mb-1 tracking-widest">Esforço Médio</p>
                <p className="text-4xl font-black text-white font-mono">{avgEffort}<span className="text-sm text-gray-600">/10</span></p>
            </div>
          </div>

          {/* Gráfico de Barras - Consistência de Tempo */}
          <div className="bg-card-bg border border-gray-800 rounded-3xl p-5 space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-[10px] text-gray-500 uppercase font-black tracking-widest flex items-center gap-2">
                <TrendingUp size={12} className="text-neon-green" /> Minutos por Treino
              </h3>
              <span className="text-[10px] text-neon-green font-bold px-2 py-0.5 bg-neon-green/10 rounded-full">Últimos {chartData.length}</span>
            </div>
            
            <div className="flex items-end justify-around h-32 gap-1 px-1">
              {chartData.map((log, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-2 group relative">
                  <div 
                    className="w-full max-w-[12px] bg-gradient-to-t from-neon-green/5 to-neon-green rounded-t-full transition-all duration-700 ease-out shadow-[0_0_15px_rgba(0,255,148,0.1)] group-hover:shadow-[0_0_20px_rgba(0,255,148,0.3)]"
                    style={{ height: `${(log.duracao / maxDuration) * 100}%` }}
                  >
                    <div className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] font-mono text-neon-green opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{log.duracao}m</div>
                  </div>
                  <span className="text-[8px] text-gray-600 font-bold uppercase">{log.data}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Resumo de Tempo */}
          <div className="bg-neon-green p-5 rounded-3xl text-black flex justify-between items-center shadow-[0_0_30px_rgba(0,255,148,0.1)]">
            <div>
                <p className="text-[10px] uppercase font-black opacity-60">Tempo Total Dedicado</p>
                <p className="text-2xl font-black">{totalMinutes} minutos</p>
            </div>
            <div className="w-12 h-12 bg-black/10 rounded-2xl flex items-center justify-center"><Clock size={24}/></div>
          </div>

          {/* Histórico Diário */}
          <div className="space-y-4">
            <h3 className="text-xs font-black text-gray-500 uppercase tracking-[0.2em] flex items-center gap-2 mb-4">
              <TrendingUp size={14} className="text-neon-green" /> LOGS DE ATIVIDADE
            </h3>
            
            <div className="space-y-3">
              {logs.slice().reverse().map((log) => (
                <div key={log.id} className="bg-card-bg border border-gray-800 rounded-2xl p-4 flex items-center justify-between hover:border-gray-600 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gray-900 rounded-xl flex items-center justify-center text-neon-green border border-gray-800">
                      <Calendar size={20} />
                    </div>
                    <div>
                      <p className="font-bold text-white text-sm">{log.data}</p>
                      <div className="flex gap-3 text-[10px] text-gray-500 uppercase font-black tracking-tighter mt-1">
                        <span className="flex items-center gap-1"><Clock size={10}/> {log.duracao} min</span>
                        <span className="flex items-center gap-1"><Zap size={10}/> RPE: {log.esforco}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                    <div className="h-1.5 w-16 bg-gray-800 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-neon-green" 
                          style={{ width: `${(log.esforco / 10) * 100}%` }}
                        ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}