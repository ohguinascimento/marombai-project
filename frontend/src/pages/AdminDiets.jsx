import React, { useState, useEffect } from 'react';
import { Utensils, Search, User, AlertTriangle } from 'lucide-react';

export default function AdminDiets() {
  const [diets, setDiets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchDiets();
  }, []);

  const fetchDiets = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/dietas');
      if (response.ok) {
        const data = await response.json();
        setDiets(Array.isArray(data) ? data : []);
      } else {
        console.error("Erro ao buscar dietas");
      }
    } catch (error) {
      console.error("Erro de conexão:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredDiets = diets.filter(diet => 
    diet && (
      (diet.titulo && diet.titulo.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (diet.objetivo && diet.objetivo.toLowerCase().includes(searchTerm.toLowerCase()))
    )
  );

  const parseAndFormatList = (jsonString) => {
    try {
      const list = JSON.parse(jsonString);
      if (Array.isArray(list) && list.length > 0) {
        return list.join(', ');
      }
      return 'Nenhuma';
    } catch (e) {
      return jsonString || 'N/A';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gray-800 rounded-xl text-blue-400 border border-blue-400/20">
              <Utensils size={24} className="text-blue-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Histórico de Dietas</h1>
              <p className="text-gray-400 text-sm">Monitoramento de planos nutricionais</p>
            </div>
          </div>

          {/* Barra de Busca */}
          <div className="relative w-full md:w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Buscar por título ou objetivo..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-blue-400 focus:outline-none transition-colors text-white"
            />
          </div>
        </div>

        {/* Tabela */}
        <div className="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-2xl">
          {loading ? (
            <div className="p-12 flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-400"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-900 text-gray-400 text-xs uppercase tracking-wider border-b border-gray-700">
                    <th className="p-4 font-bold">ID</th>
                    <th className="p-4 font-bold">Título</th>
                    <th className="p-4 font-bold">Objetivo</th>
                    <th className="p-4 font-bold">Restrições</th>
                    <th className="p-4 font-bold">ID Usuário</th>
                    <th className="p-4 font-bold">Data Criação</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {filteredDiets.map((diet) => (
                    <tr key={diet.id} className="hover:bg-gray-700/50 transition-colors group">
                      <td className="p-4 text-gray-500 font-mono text-xs">#{diet.id}</td>
                      <td className="p-4 font-bold text-white group-hover:text-blue-400 transition-colors">{diet.titulo}</td>
                      <td className="p-4"><span className="px-3 py-1 rounded-full text-xs font-bold bg-gray-900 border border-gray-600 text-gray-300">{diet.objetivo}</span></td>
                      <td className="p-4 text-sm text-yellow-400 capitalize flex items-center gap-2"><AlertTriangle size={14} /> {parseAndFormatList(diet.restricoes)}</td>
                      <td className="p-4 text-sm text-gray-400 font-mono"><div className="flex items-center gap-2"><User size={14} /> {diet.user_id}</div></td>
                      <td className="p-4 text-xs text-gray-500 font-mono">{diet.created_at ? new Date(diet.created_at).toLocaleString('pt-BR') : '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filteredDiets.length === 0 && (<div className="p-8 text-center text-gray-500">Nenhuma dieta registrada no banco.</div>)}
            </div>
          )}
        </div>
        <div className="mt-4 text-right text-xs text-gray-600">Total de dietas: <span className="text-blue-400">{filteredDiets.length}</span></div>
      </div>
    </div>
  );
}