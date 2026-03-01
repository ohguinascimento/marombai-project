import React, { useState, useEffect } from 'react';
import { Users, Search, Activity, Calendar } from 'lucide-react';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/usuarios');
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else {
        console.error("Erro ao buscar usuários");
      }
    } catch (error) {
      console.error("Erro de conexão:", error);
    } finally {
      setLoading(false);
    }
  };

  // Filtro de busca simples
  const filteredUsers = users.filter(user => 
    user.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.objetivo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-dark-bg text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green border border-neon-green/20">
              <Users size={24} />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Base de Atletas</h1>
              <p className="text-gray-400 text-sm">Gerenciamento de usuários cadastrados</p>
            </div>
          </div>

          {/* Barra de Busca */}
          <div className="relative w-full md:w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Buscar atleta..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-card-bg border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-neon-green focus:outline-none transition-colors"
            />
          </div>
        </div>

        {/* Tabela */}
        <div className="bg-card-bg rounded-2xl border border-gray-800 overflow-hidden shadow-2xl">
          {loading ? (
            <div className="p-12 flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-neon-green"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-900/50 text-gray-400 text-xs uppercase tracking-wider border-b border-gray-800">
                    <th className="p-4 font-bold">ID</th>
                    <th className="p-4 font-bold">Nome</th>
                    <th className="p-4 font-bold">Perfil Físico</th>
                    <th className="p-4 font-bold">Objetivo</th>
                    <th className="p-4 font-bold">Nível</th>
                    <th className="p-4 font-bold">Data Cadastro</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {filteredUsers.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-800/30 transition-colors group">
                      <td className="p-4 text-gray-500 font-mono text-xs">#{user.id}</td>
                      <td className="p-4 font-bold text-white group-hover:text-neon-green transition-colors">
                        {user.nome}
                      </td>
                      <td className="p-4 text-sm text-gray-300">
                        {user.idade} anos • {user.peso}kg • {user.altura}cm
                      </td>
                      <td className="p-4">
                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-gray-800 border border-gray-700 text-gray-300">
                          {user.objetivo}
                        </span>
                      </td>
                      <td className="p-4 text-sm text-gray-400 capitalize">{user.nivel}</td>
                      <td className="p-4 text-xs text-gray-500 font-mono">
                        {new Date(user.created_at).toLocaleDateString('pt-BR')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {filteredUsers.length === 0 && (
                <div className="p-8 text-center text-gray-500">
                  Nenhum atleta encontrado.
                </div>
              )}
            </div>
          )}
        </div>
        
        <div className="mt-4 text-right text-xs text-gray-600">
          Total de registros: <span className="text-neon-green">{filteredUsers.length}</span>
        </div>
      </div>
    </div>
  );
}