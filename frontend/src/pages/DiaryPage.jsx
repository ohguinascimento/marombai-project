import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Calendar } from 'lucide-react';

export default function DiaryPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 font-sans">
      {/* Header com Botão Voltar */}
      <header className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="p-2 bg-gray-800 rounded-full text-gray-400 hover:text-white transition-colors"
        >
          <ChevronLeft size={24} />
        </button>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Calendar className="text-neon-green" /> Diário de Treino
        </h1>
      </header>

      {/* Conteúdo Placeholder */}
      <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
        <div className="p-6 bg-gray-900 rounded-full border border-gray-800">
            <Calendar size={48} className="text-gray-600" />
        </div>
        <h2 className="text-xl font-bold text-gray-300">Histórico em Construção</h2>
        <p className="text-gray-500 max-w-xs">Em breve você poderá visualizar todo o seu histórico de treinos e evolução aqui.</p>
      </div>
    </div>
  );
}