import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Dumbbell, Activity, Apple, Scale, Calendar } from 'lucide-react';

export default function Onboarding() {
  const [step, setStep] = useState(1);
  const totalSteps = 5;
  
  // Estado para armazenar todos os dados
  const [formData, setFormData] = useState({
    nome: '',
    idade: '',
    genero: 'masculino',
    peso: '',
    altura: '',
    bodyFat: '', 
    objetivo: 'hipertrofia',
    nivel: 'iniciante',
    frequencia: 3,
    local: 'academia',
    lesoes: [], 
    restricoes: [], 
    dieta: 'onivoro', 
    suplementos: [] 
  });

  // Função para marcar/desmarcar itens (Multi-Select)
  const toggleSelection = (field, value) => {
    setFormData(prev => {
      const list = prev[field];
      if (list.includes(value)) {
        return { ...prev, [field]: list.filter(item => item !== value) };
      } else {
        return { ...prev, [field]: [...list, value] };
      }
    });
  };

  const nextStep = () => { if (step < totalSteps) setStep(step + 1); };
  const prevStep = () => { if (step > 1) setStep(step - 1); };

  const handleFinish = () => {
    console.log("Dados prontos para envio:", formData);
    alert("Sucesso! Dados coletados (veja no Console F12). Próximo passo: Backend!");
  };

  // Componente visual de Botão Pequeno (Chip)
  const SelectChip = ({ field, value, label }) => (
    <button
      onClick={() => toggleSelection(field, value)}
      className={`px-4 py-2 rounded-full border transition-all text-sm font-medium
        ${formData[field].includes(value) 
          ? 'bg-neon-green text-black border-neon-green shadow-[0_0_10px_rgba(0,255,148,0.2)]' 
          : 'bg-transparent text-gray-400 border-gray-700 hover:border-gray-500'}`}
    >
      {label}
    </button>
  );

  return (
    <div className="min-h-screen bg-dark-bg text-white flex flex-col items-center justify-center p-6 font-sans">
      
      {/* Barra de Progresso */}
      <div className="w-full max-w-lg mb-8">
        <div className="flex justify-between text-xs text-gray-500 mb-2 font-bold tracking-wider">
          <span>PASSO {step} / {totalSteps}</span>
          <span>{Math.round((step / totalSteps) * 100)}%</span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <div 
            className="h-full bg-neon-green transition-all duration-500 ease-out shadow-[0_0_10px_#00FF94]"
            style={{ width: `${(step / totalSteps) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Card Principal */}
      <div className="w-full max-w-lg bg-card-bg p-8 rounded-3xl border border-gray-800 shadow-2xl relative overflow-hidden">
        
        {/* Passo 1: Identidade */}
        {step === 1 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Dumbbell size={24} /></div>
              <h2 className="text-2xl font-bold">Quem é você?</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider">Nome</label>
                <input 
                  type="text" 
                  value={formData.nome}
                  onChange={(e) => setFormData({...formData, nome: e.target.value})}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none transition-colors mt-1"
                  placeholder="Como quer ser chamado?"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-gray-500 uppercase tracking-wider">Idade</label>
                  <input 
                    type="number" 
                    value={formData.idade}
                    onChange={(e) => setFormData({...formData, idade: e.target.value})}
                    className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-1"
                    placeholder="Anos"
                  />
                </div>
                <div>
                  <label className="text-xs text-gray-500 uppercase tracking-wider">Gênero</label>
                  <select 
                    value={formData.genero}
                    onChange={(e) => setFormData({...formData, genero: e.target.value})}
                    className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-1 appearance-none cursor-pointer"
                  >
                    <option value="masculino">Masculino</option>
                    <option value="feminino">Feminino</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Passo 2: Medidas */}
        {step === 2 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Scale size={24} /></div>
              <h2 className="text-2xl font-bold">Suas Medidas</h2>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider">Peso (kg)</label>
                <input 
                  type="number" 
                  value={formData.peso}
                  onChange={(e) => setFormData({...formData, peso: e.target.value})}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-1"
                  placeholder="0.0"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider">Altura (cm)</label>
                <input 
                  type="number" 
                  value={formData.altura}
                  onChange={(e) => setFormData({...formData, altura: e.target.value})}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-1"
                  placeholder="000"
                />
              </div>
            </div>

            {/* Estimativa Visual de Gordura */}
            <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Estimativa de Gordura</label>
               <div className="grid grid-cols-3 gap-2">
                  {[10, 15, 20, 25, 30, 35].map((fat) => (
                    <button 
                      key={fat}
                      onClick={() => setFormData({...formData, bodyFat: fat})}
                      className={`h-20 rounded-lg border flex flex-col items-center justify-center gap-1 transition-all
                        ${formData.bodyFat === fat 
                          ? 'border-neon-green bg-neon-green/10 text-neon-green shadow-[inset_0_0_10px_rgba(0,255,148,0.1)]' 
                          : 'border-gray-700 bg-dark-bg text-gray-500 hover:border-gray-500'}`}
                    >
                      <span className="text-sm font-bold">{fat}%</span>
                    </button>
                  ))}
               </div>
            </div>
          </div>
        )}

        {/* Passo 3: Objetivo */}
        {step === 3 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Activity size={24} /></div>
              <h2 className="text-2xl font-bold">Qual seu foco?</h2>
            </div>

            <div className="grid grid-cols-1 gap-3">
              {['Hipertrofia', 'Emagrecimento', 'Força Pura', 'Condicionamento'].map((obj) => (
                 <button
                   key={obj}
                   onClick={() => setFormData({...formData, objetivo: obj.toLowerCase()})}
                   className={`p-4 rounded-xl border flex items-center justify-between transition-all group
                     ${formData.objetivo === obj.toLowerCase()
                       ? 'border-neon-green bg-neon-green/5 shadow-[0_0_15px_rgba(0,255,148,0.1)]' 
                       : 'border-gray-700 bg-dark-bg hover:border-gray-500'}`}
                 >
                   <span className={`font-bold ${formData.objetivo === obj.toLowerCase() ? 'text-neon-green' : 'text-white'}`}>
                     {obj}
                   </span>
                   {formData.objetivo === obj.toLowerCase() && <div className="w-3 h-3 bg-neon-green rounded-full shadow-[0_0_10px_#00FF94]"></div>}
                 </button>
              ))}
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Nível de Experiência</label>
               <div className="flex gap-2">
                  {['Iniciante', 'Intermediário', 'Avançado'].map((lvl) => (
                    <button 
                      key={lvl}
                      onClick={() => setFormData({...formData, nivel: lvl.toLowerCase()})}
                      className={`flex-1 py-3 rounded-xl border text-sm font-bold transition-all
                        ${formData.nivel === lvl.toLowerCase()
                          ? 'border-neon-green bg-neon-green text-black'
                          : 'border-gray-700 bg-dark-bg text-gray-400 hover:border-gray-500'}`}
                    >
                      {lvl}
                    </button>
                  ))}
               </div>
            </div>
          </div>
        )}

        {/* Passo 4: Rotina */}
        {step === 4 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
               <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Calendar size={24} /></div>
               <h2 className="text-2xl font-bold">Rotina & Limitações</h2>
            </div>
            
            {/* Dias por Semana */}
            <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-3 block">Dias de treino na semana: <span className="text-neon-green text-lg ml-2">{formData.frequencia}x</span></label>
               <input 
                 type="range" min="1" max="7" 
                 value={formData.frequencia}
                 onChange={(e) => setFormData({...formData, frequencia: parseInt(e.target.value)})}
                 className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-neon-green"
               />
               <div className="flex justify-between text-xs text-gray-600 mt-2 px-1">
                 <span>1 dia</span><span>Todos os dias</span>
               </div>
            </div>

            {/* Local */}
             <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Onde vai treinar?</label>
               <div className="flex gap-2">
                  {['Academia', 'Em Casa', 'Ao Ar Livre'].map((loc) => (
                    <button 
                      key={loc}
                      onClick={() => setFormData({...formData, local: loc.toLowerCase()})}
                      className={`flex-1 py-2 rounded-lg border text-xs font-bold transition-all
                        ${formData.local === loc.toLowerCase()
                          ? 'border-neon-green text-neon-green bg-neon-green/10'
                          : 'border-gray-700 bg-dark-bg text-gray-500'}`}
                    >
                      {loc}
                    </button>
                  ))}
               </div>
            </div>

            {/* Lesões */}
            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-3 block">Possui alguma lesão/dor?</label>
              <div className="flex flex-wrap gap-2">
                 {['Ombro', 'Joelho', 'Lombar', 'Punho', 'Tornozelo', 'Quadril'].map((item) => (
                    <SelectChip key={item} field="lesoes" value={item} label={item} />
                 ))}
              </div>
            </div>
          </div>
        )}

        {/* Passo 5: Saúde (Final) */}
        {step === 5 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
               <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Apple size={24} /></div>
               <h2 className="text-2xl font-bold">Saúde & Nutrição</h2>
            </div>

            <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Estilo Alimentar</label>
               <select 
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-3 text-white focus:border-neon-green focus:outline-none cursor-pointer"
                  value={formData.dieta}
                  onChange={(e) => setFormData({...formData, dieta: e.target.value})}
               >
                 <option value="onivoro">Onívoro (Come de tudo)</option>
                 <option value="vegetariano">Vegetariano</option>
                 <option value="vegano">Vegano</option>
                 <option value="flexivel">Dieta Flexível</option>
                 <option value="cetogenica">Cetogênica</option>
               </select>
            </div>

            <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Condições de Saúde</label>
               <div className="flex flex-wrap gap-2">
                  <SelectChip field="restricoes" value="diabetes" label="Diabetes" />
                  <SelectChip field="restricoes" value="hipertensao" label="Hipertensão" />
                  <SelectChip field="restricoes" value="lactose" label="Intol. Lactose" />
                  <SelectChip field="restricoes" value="gluten" label="Intol. Glúten" />
               </div>
            </div>

             <div>
               <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Suplementos</label>
               <div className="flex flex-wrap gap-2">
                  <SelectChip field="suplementos" value="whey" label="Whey" />
                  <SelectChip field="suplementos" value="creatina" label="Creatina" />
                  <SelectChip field="suplementos" value="cafeina" label="Pré-Treino" />
                  <SelectChip field="suplementos" value="vitaminas" label="Vitaminas" />
               </div>
            </div>
          </div>
        )}

        {/* Rodapé de Navegação */}
        <div className="flex justify-between mt-8 pt-6 border-t border-gray-800">
          <button 
            onClick={prevStep}
            className={`flex items-center gap-2 text-gray-400 hover:text-white transition-colors ${step === 1 ? 'invisible' : ''}`}
          >
            <ChevronLeft size={20} /> Voltar
          </button>
          
          <button 
            onClick={step === totalSteps ? handleFinish : nextStep}
            className="bg-neon-green text-black font-bold py-3 px-8 rounded-xl flex items-center gap-2 hover:opacity-90 transition-all shadow-[0_0_15px_rgba(0,255,148,0.3)] hover:shadow-[0_0_25px_rgba(0,255,148,0.5)] transform hover:-translate-y-1"
          >
            {step === totalSteps ? 'Gerar Meu Plano' : 'Continuar'} <ChevronRight size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}