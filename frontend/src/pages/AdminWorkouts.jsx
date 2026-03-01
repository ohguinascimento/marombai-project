import React, { useState, useEffect } from 'react';
import { Dumbbell, Search, User } from 'lucide-react';

export default function AdminWorkouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      console.log("🔄 Buscando treinos...");
      const response = await fetch('http://127.0.0.1:8000/treinos');
      if (response.ok) {
        const data = await response.json();
        console.log("✅ Treinos recebidos:", data);
        setWorkouts(Array.isArray(data) ? data : []);
      } else {
        console.error("Erro ao buscar treinos");
      }
    } catch (error) {
      console.error("Erro de conexão:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredWorkouts = workouts.filter(workout => 
    // Proteção: Verifica se workout e seus campos existem antes de filtrar
    workout && (
      (workout.titulo && workout.titulo.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (workout.foco && workout.foco.toLowerCase().includes(searchTerm.toLowerCase()))
    )
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gray-800 rounded-xl text-purple-400 border border-purple-400/20">
              <Dumbbell size={24} className="text-purple-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Histórico de Treinos</h1>
              <p className="text-gray-400 text-sm">Monitoramento de planos gerados pela IA</p>
            </div>
          </div>

          {/* Barra de Busca */}
          <div className="relative w-full md:w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Buscar treino..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-purple-400 focus:outline-none transition-colors text-white"
            />
          </div>
        </div>

        {/* Tabela */}
        <div className="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-2xl">
          {loading ? (
            <div className="p-12 flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-400"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-900 text-gray-400 text-xs uppercase tracking-wider border-b border-gray-700">
                    <th className="p-4 font-bold">ID</th>
                    <th className="p-4 font-bold">Título do Treino</th>
                    <th className="p-4 font-bold">Foco Muscular</th>
                    <th className="p-4 font-bold">Dificuldade</th>
                    <th className="p-4 font-bold">ID Usuário</th>
                    <th className="p-4 font-bold">Data Criação</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {filteredWorkouts.map((workout) => (
                    <tr key={workout.id} className="hover:bg-gray-700/50 transition-colors group">
                      <td className="p-4 text-gray-500 font-mono text-xs">#{workout.id}</td>
                      <td className="p-4 font-bold text-white group-hover:text-purple-400 transition-colors">
                        {workout.titulo || "Sem título"}
                      </td>
                      <td className="p-4">
                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-gray-900 border border-gray-600 text-gray-300">
                          {workout.foco || "Geral"}
                        </span>
                      </td>
                      <td className="p-4 text-sm text-gray-400 capitalize">{workout.nivel_dificuldade}</td>
                      <td className="p-4 text-sm text-gray-400 font-mono">
                        <div className="flex items-center gap-2">
                          <User size={14} /> {workout.user_id}
                        </div>
                      </td>
                      <td className="p-4 text-xs text-gray-500 font-mono">
                        {/* Proteção extra para datas inválidas */}
                        {(() => {
                          try {
                            return workout.created_at ? new Date(workout.created_at).toLocaleDateString('pt-BR') : '-';
                          } catch (e) { return '-'; }
                        })()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {filteredWorkouts.length === 0 && (
                <div className="p-8 text-center text-gray-500">
                  Nenhum treino registrado no banco.
                </div>
              )}
            </div>
          )}
        </div>
        
        <div className="mt-4 text-right text-xs text-gray-600">
          Total de treinos: <span className="text-purple-400">{filteredWorkouts.length}</span>
        </div>
      </div>
    </div>
  );
}