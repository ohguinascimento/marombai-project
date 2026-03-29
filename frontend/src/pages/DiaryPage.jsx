import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Calendar, Clock, Zap, CheckCircle2, MessageSquare } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL;

export default function DiaryPage() {
  const navigate = useNavigate();
  const userId = localStorage.getItem('marombai_user_id');
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch(`${API_URL}/user/${userId}/evolution`);
        if (response.ok) {
          const data = await response.json();
          // Ordenamos do mais recente para o mais antigo para o Diário
          setLogs([...data].reverse());
        }
      } catch (error) {
        console.error("Erro ao buscar diário:", error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchLogs();
    } else {
      setLoading(false);
    }
  }, [userId]);

  if (loading) return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center text-neon-green font-black italic">
      CARREGANDO DIÁRIO...
    </div>
  );

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 pb-24 font-sans">
      {/* Header */}
      <header className="flex items-center gap-4 mb-8">
        <button onClick={() => navigate(-1)} className="p-2 bg-gray-900 rounded-xl text-gray-400 active:scale-95 transition-all">
          <ChevronLeft size={24} />
        </button>
        <h1 className="text-2xl font-bold uppercase italic tracking-tighter">Diário de Treino</h1>
      </header>

      {logs.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4 opacity-30">
          <Calendar size={60} />
          <p className="text-sm">Nenhum registro encontrado no seu diário.</p>
        </div>
      ) : (
        <div className="space-y-8 relative">
          {/* Linha Vertical da Timeline */}
          <div className="absolute left-4 top-2 bottom-2 w-0.5 bg-gray-800 -z-10"></div>

          {logs.map((log) => (
            <div key={log.id} className="relative pl-12 animate-fade-in">
              {/* Ponto da Timeline */}
              <div className="absolute left-[11px] top-1 w-2.5 h-2.5 bg-neon-green rounded-full shadow-[0_0_10px_#00FF94]"></div>
              
              <div className="mb-2 flex items-center justify-between">
                <span className="text-neon-green font-black text-sm tracking-widest">{log.data}</span>
                <span className="text-[10px] text-gray-600 font-bold uppercase">Sessão #{log.id}</span>
              </div>

              <div className="bg-card-bg rounded-2xl border border-gray-800 p-5 space-y-4 shadow-xl hover:border-neon-green/30 transition-colors">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-white flex items-center gap-2">
                      Treino Concluído <CheckCircle2 size={16} className="text-neon-green" />
                    </h3>
                    <div className="flex gap-4 mt-2 text-[10px] text-gray-500 font-black uppercase">
                      <span className="flex items-center gap-1"><Clock size={12}/> {log.duracao} min</span>
                      <span className="flex items-center gap-1"><Zap size={12}/> Esforço: {log.esforco}/10</span>
                    </div>
                  </div>
                </div>

                {log.observacoes && (
                   <div className="bg-black/20 p-3 rounded-lg border-l-2 border-neon-green flex gap-2">
                     <MessageSquare size={14} className="text-gray-500 mt-0.5" />
                     <p className="text-xs text-gray-400 italic">"{log.observacoes}"</p>
                   </div>
                )}

                <div className="pt-3 border-t border-gray-800">
                  <p className="text-[10px] text-gray-500 font-black uppercase mb-2">Resumo da Carga:</p>
                  <div className="flex flex-wrap gap-2">
                    {log.exercicios.map((ex, idx) => (
                      <span key={idx} className="bg-black/40 px-3 py-1 rounded-lg text-[10px] text-gray-400 border border-gray-800/50">
                        {ex.nome}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}