import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Utensils, Zap, Target, Soup, Apple, Drumstick, Coffee } from 'lucide-react';

const iconMap = {
  'café da manhã': <Coffee size={20} className="text-yellow-400" />,
  'almoço': <Soup size={20} className="text-orange-400" />,
  'jantar': <Drumstick size={20} className="text-red-400" />,
  'lanche': <Apple size={20} className="text-green-400" />,
};

export default function DietPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const dieta = location.state?.dietData || null;

  if (!dieta) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-dark-bg text-white gap-4">
        <p className="text-gray-400">Nenhuma dieta encontrada.</p>
        <button 
          onClick={() => navigate('/')} 
          className="text-neon-green hover:underline font-bold"
        >
          Voltar para o início
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 font-sans">
      <header className="flex justify-between items-center mb-6">
        <button onClick={() => navigate(-1)} className="text-gray-400 hover:text-white">
          &larr; Voltar
        </button>
        <h1 className="text-xl font-bold">Seu Plano Nutricional</h1>
        <div className="w-12"></div>
      </header>

      <div className="space-y-6">
        {/* Card de Resumo */}
        <div className="bg-card-bg border border-gray-800 rounded-2xl p-5 space-y-3">
          <div className="flex items-center gap-2 text-blue-400">
            <Utensils size={18} />
            <span className="text-xs font-bold tracking-wider uppercase">Resumo da Dieta</span>
          </div>
          <h2 className="text-2xl font-bold">{dieta.titulo || "Dieta Personalizada"}</h2>
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-2 text-gray-400">
              <Target size={14} className="text-green-400" />
              <span>{dieta.objetivo}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-400">
              <Zap size={14} className="text-yellow-400" />
              <span>{dieta.kcal} Kcal</span>
            </div>
          </div>
        </div>

        {/* Lista de Refeições */}
        <div className="space-y-4">
          {dieta.refeicoes && dieta.refeicoes.map((refeicao, index) => (
            <div key={index} className="bg-card-bg rounded-xl border border-gray-800 p-5">
              <div className="flex items-center gap-3 mb-3">
                {iconMap[refeicao.nome.toLowerCase()] || <Utensils size={20} />}
                <h3 className="font-bold text-lg text-white">{refeicao.nome}</h3>
              </div>
              <ul className="space-y-2 list-inside">
                {refeicao.itens.map((item, itemIndex) => (
                  <li key={itemIndex} className="text-gray-300 flex items-start gap-2">
                    <span className="text-neon-green mt-1">&#8227;</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}