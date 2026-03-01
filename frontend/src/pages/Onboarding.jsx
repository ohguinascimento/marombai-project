import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Dumbbell, Activity, Apple, Scale, Calendar, Brain } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const totalSteps = 5;

  // Estado completo com todos os campos
  const [formData, setFormData] = useState({
    nome: '',
    idade: '',
    genero: 'masculino',
    peso: '',
    altura: '',
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

  const handleFinish = async () => {
    setIsLoading(true); // Mostra o loading

    // --- 1. LIMPEZA E CONVERSÃO DOS DADOS ---
    // O formulário HTML salva tudo como texto ("string").
    // O Python exige números (int/float). Aqui fazemos a conversão:
    const payload = {
      ...formData,
      idade: parseInt(formData.idade) || 0,       // "25" vira 25
      peso: parseFloat(formData.peso) || 0.0,     // "80.5" vira 80.5
      altura: parseInt(formData.altura) || 0,     // "180" vira 180
      frequencia: parseInt(formData.frequencia) || 3 // Garante inteiro
    };

    console.log("🚀 Enviando payload formatado:", payload);

    try {
      // Cria uma promessa de delay mínimo de 1.5 segundos para UX
      const minDelay = new Promise(resolve => setTimeout(resolve, 1500));
      
      // Executa a requisição e o delay em paralelo
      const [response] = await Promise.all([
        fetch('http://127.0.0.1:8000/gerar-treino', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload), // Enviamos o 'payload' limpo, não o 'formData' sujo
      }),
        minDelay
      ]);

      const data = await response.json();

      if (response.ok && data.status === 'sucesso') {
        console.log("✅ Sucesso! Resposta:", data);

        // Navega para o Dashboard levando o treino
        navigate('/dashboard', { state: { treinoData: data.treino } });
      } else {
        console.error("❌ Erro no Backend:", data);
        // Mostra o erro exato que o Python devolveu (ajuda muito no debug)
        alert(`Erro de Validação: ${JSON.stringify(data.detail || data.mensagem)}`);
      }

    } catch (error) {
      console.error("❌ Erro de Conexão:", error);
      alert("Erro fatal de conexão. Verifique se o terminal do Python está aberto.");
    } finally {
      setIsLoading(false);
    }
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
    <div className="min-h-screen bg-dark-bg text-white flex flex-col items-center justify-center p-6 font-sans relative">

      {/* --- TELA DE LOADING (OVERLAY) --- */}
      {isLoading && (
        <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex flex-col items-center justify-center animate-fade-in">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-neon-green mb-6 shadow-[0_0_30px_#00FF94]"></div>
          <h2 className="text-2xl font-bold text-white animate-pulse">
            Montando seu Treino...
          </h2>
          <div className="flex items-center gap-2 mt-4 text-gray-400">
            <Brain size={18} className="text-purple-500" />
            <p>A IA está analisando sua biomecânica 🧬</p>
          </div>
        </div>
      )}

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
              <h2 className="text-2xl font-bold">Sobre você</h2>
            </div>

            <div className="space-y-5">
              {/* Nome */}
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider font-bold">Como quer ser chamado?</label>
                <input
                  type="text"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none transition-colors mt-2 placeholder-gray-600"
                  placeholder="Seu nome ou apelido"
                />
              </div>

              {/* Idade */}
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider font-bold">Idade</label>
                <input
                  type="number"
                  value={formData.idade}
                  onChange={(e) => setFormData({ ...formData, idade: e.target.value })}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-2 placeholder-gray-600"
                  placeholder="Anos"
                />
              </div>

              {/* Sexo Biológico */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs text-gray-500 uppercase tracking-wider font-bold">Sexo Biológico</label>
                  <span className="text-[10px] text-gray-600 bg-gray-900 px-2 py-1 rounded border border-gray-800">
                    *Cálculo metabólico IA
                  </span>
                </div>

                <div className="flex gap-3">
                  {['Masculino', 'Feminino'].map((sexo) => (
                    <button
                      type="button"
                      key={sexo}
                      onClick={() => setFormData({ ...formData, genero: sexo.toLowerCase() })}
                      className={`flex-1 py-4 rounded-xl border text-sm font-bold transition-all
                          ${formData.genero === sexo.toLowerCase()
                          ? 'border-neon-green bg-neon-green text-black shadow-[0_0_15px_rgba(0,255,148,0.2)]'
                          : 'border-gray-700 bg-dark-bg text-gray-400 hover:border-gray-500 hover:bg-gray-800'}`}
                    >
                      {sexo}
                    </button>
                  ))}
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

            <div className="grid grid-cols-2 gap-4 mt-8">
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider font-bold">Peso (kg)</label>
                <input
                  type="number"
                  value={formData.peso}
                  onChange={(e) => setFormData({ ...formData, peso: e.target.value })}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-2 text-xl"
                  placeholder="0.0"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase tracking-wider font-bold">Altura (cm)</label>
                <input
                  type="number"
                  value={formData.altura}
                  onChange={(e) => setFormData({ ...formData, altura: e.target.value })}
                  className="w-full bg-dark-bg border border-gray-700 rounded-xl p-4 text-white focus:border-neon-green focus:outline-none mt-2 text-xl"
                  placeholder="000"
                />
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
              {[
                { id: 'hipertrofia', label: 'Hipertrofia', desc: 'Ganhar massa muscular e volume' },
                { id: 'emagrecimento', label: 'Emagrecimento', desc: 'Queimar gordura e definir o corpo' },
                { id: 'forca', label: 'Força Pura', desc: 'Aumentar as cargas máximas' },
                { id: 'condicionamento', label: 'Condicionamento', desc: 'Melhorar resistência e saúde' }
              ].map((obj) => (
                <button
                  key={obj.id}
                  onClick={() => setFormData({ ...formData, objetivo: obj.id })}
                  className={`p-4 rounded-xl border flex items-center justify-between transition-all group text-left
                     ${formData.objetivo === obj.id
                      ? 'border-neon-green bg-neon-green/5 shadow-[0_0_15px_rgba(0,255,148,0.1)]'
                      : 'border-gray-700 bg-dark-bg hover:border-gray-500 hover:bg-gray-800'}`}
                >
                  <div>
                    <span className={`font-bold block ${formData.objetivo === obj.id ? 'text-neon-green' : 'text-white'}`}>
                      {obj.label}
                    </span>
                    <span className="text-xs text-gray-500 mt-1">{obj.desc}</span>
                  </div>
                  {formData.objetivo === obj.id && <div className="w-3 h-3 bg-neon-green rounded-full shadow-[0_0_10px_#00FF94]"></div>}
                </button>
              ))}
            </div>

            <div className="mt-6">
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block font-bold">Nível de Experiência</label>
              <div className="flex gap-2">
                {['Iniciante', 'Intermediário', 'Avançado'].map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setFormData({ ...formData, nivel: lvl.toLowerCase() })}
                    className={`flex-1 py-3 rounded-xl border text-sm font-bold transition-all
                        ${formData.nivel === lvl.toLowerCase()
                        ? 'border-neon-green bg-neon-green text-black'
                        : 'border-gray-700 bg-dark-bg text-gray-400 hover:border-gray-500 hover:bg-gray-800'}`}
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
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-3 block font-bold">Dias de treino na semana: <span className="text-neon-green text-lg ml-2">{formData.frequencia}x</span></label>
              <input
                type="range" min="1" max="7"
                value={formData.frequencia}
                onChange={(e) => setFormData({ ...formData, frequencia: parseInt(e.target.value) })}
                className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-neon-green"
              />
              <div className="flex justify-between text-xs text-gray-600 mt-2 px-1">
                <span>1 dia</span><span>Todos os dias</span>
              </div>
            </div>

            {/* Local */}
            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block font-bold">Onde vai treinar?</label>
              <div className="flex gap-2">
                {['Academia', 'Em Casa', 'Ao Ar Livre'].map((loc) => (
                  <button
                    key={loc}
                    onClick={() => setFormData({ ...formData, local: loc.toLowerCase() })}
                    className={`flex-1 py-2 rounded-lg border text-xs font-bold transition-all
                        ${formData.local === loc.toLowerCase()
                        ? 'border-neon-green text-neon-green bg-neon-green/10'
                        : 'border-gray-700 bg-dark-bg text-gray-500 hover:border-gray-500'}`}
                  >
                    {loc}
                  </button>
                ))}
              </div>
            </div>

            {/* Lesões */}
            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-3 block font-bold">Possui alguma lesão/dor?</label>
              <div className="flex flex-wrap gap-2">
                {['Ombro', 'Joelho', 'Lombar', 'Punho', 'Tornozelo', 'Quadril'].map((item) => (
                  <SelectChip key={item} field="lesoes" value={item} label={item} />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Passo 5: Saúde */}
        {step === 5 && (
          <div className="animate-fade-in space-y-6">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gray-800/50 rounded-xl text-neon-green"><Apple size={24} /></div>
              <h2 className="text-2xl font-bold">Saúde & Nutrição</h2>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block font-bold">Estilo Alimentar</label>
              <select
                className="w-full bg-dark-bg border border-gray-700 rounded-xl p-3 text-white focus:border-neon-green focus:outline-none cursor-pointer appearance-none"
                value={formData.dieta}
                onChange={(e) => setFormData({ ...formData, dieta: e.target.value })}
              >
                <option value="onivoro">Onívoro (Come de tudo)</option>
                <option value="vegetariano">Vegetariano (Sem carnes)</option>
                <option value="vegano">Vegano (Zero origem animal)</option>
                <option value="flexivel">Dieta Flexível (Foco nos macros)</option>
                <option value="cetogenica">Cetogênica (Baixo carboidrato)</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block font-bold">Condições de Saúde</label>
              <div className="flex flex-wrap gap-2">
                <SelectChip field="restricoes" value="diabetes" label="Diabetes" />
                <SelectChip field="restricoes" value="hipertensao" label="Hipertensão" />
                <SelectChip field="restricoes" value="lactose" label="Intol. Lactose" />
                <SelectChip field="restricoes" value="gluten" label="Intol. Glúten" />
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wider mb-2 block font-bold">Suplementos</label>
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
            disabled={isLoading}
            className="bg-neon-green text-black font-bold py-3 px-8 rounded-xl flex items-center gap-2 hover:opacity-90 transition-all shadow-[0_0_15px_rgba(0,255,148,0.3)] hover:shadow-[0_0_25px_rgba(0,255,148,0.5)] transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {step === totalSteps ? 'Gerar Meu Plano' : 'Continuar'} <ChevronRight size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}