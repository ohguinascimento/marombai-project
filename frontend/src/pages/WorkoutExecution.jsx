import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, CheckCircle2, Clock, Zap, Timer, Star } from 'lucide-react';

export default function WorkoutExecution() {
  const location = useLocation();
  const navigate = useNavigate();
  const { treino, treinoId, userId } = location.state || {};

  const [currentIndex, setCurrentIndex] = useState(0);
  const [startTime] = useState(Date.now());
  const [seconds, setSeconds] = useState(0);
  const [completedExercises, setCompletedExercises] = useState([]);

  const [isResting, setIsResting] = useState(false);
  const [isFinishing, setIsFinishing] = useState(false);
  const [esforco, setEsforco] = useState(7);
  const [restTime, setRestTime] = useState(0);

  // Carrega a preferência de som (padrão é true)
  const [soundEnabled] = useState(() => localStorage.getItem('marombai_sound_enabled') !== 'false');

  // Função para gerar um bipe sintetizado via Web Audio API
  const playBeep = (frequency = 440, duration = 0.1) => {
    try {
      const context = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = context.createOscillator();
      const gainNode = context.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(context.destination);

      oscillator.type = 'sine';
      oscillator.frequency.value = frequency;

      oscillator.start();
      gainNode.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + duration);
      oscillator.stop(context.currentTime + duration);
    } catch (e) {
      console.error("Erro ao reproduzir áudio:", e);
    }
  };

  // Cronômetro do descanso
  useEffect(() => {
    let timer;
    if (isResting && restTime > 0) {
      // Toca o bipe se estiver nos últimos 3 segundos
      if (soundEnabled && restTime <= 3) {
        // Frequência mais alta (880Hz) no último segundo, mais baixa (440Hz) nos outros
        playBeep(restTime === 1 ? 880 : 440);
      }
      timer = setInterval(() => setRestTime(t => t - 1), 1000);
    } else if (isResting && restTime === 0) {
      skipRest();
    }
    return () => clearInterval(timer);
  }, [isResting, restTime]);

  // Cronômetro do treino
  useEffect(() => {
    const interval = setInterval(() => setSeconds(s => s + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  if (!treino) return <div className="p-10 text-white">Carregando treino...</div>;

  const exercicios = treino.exercicios || [];
  const currentEx = exercicios[currentIndex];

  const formatTime = (s) => {
    const min = Math.floor(s / 60);
    const sec = s % 60;
    return `${min}:${sec.toString().padStart(2, '0')}`;
  };

  const handleNext = () => {
    const time = parseInt(currentEx.descanso) || 60;
    setRestTime(time);
    setIsResting(true);
  };

  const skipRest = () => {
    setIsResting(false);
    setCurrentIndex(prev => prev + 1);
  };

  const handleFinish = async () => {
    const duracao = Math.floor((Date.now() - startTime) / 60000);
    
    const payload = {
      user_id: userId,
      workout_plan_id: treinoId,
      duracao_minutos: duracao,
      esforco_percebido: esforco,
      detalhes_exercicios: exercicios // Aqui salvaríamos as cargas reais se tivéssemos inputs
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/workout/finish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        alert("🔥 Treino Finalizado! Monstro!");
        navigate('/dashboard');
      }
    } catch (error) {
      console.error("Erro ao finalizar treino:", error);
    }
  };

  if (isFinishing) {
    return (
      <div className="min-h-screen bg-black text-white p-6 flex flex-col items-center justify-center font-sans animate-fade-in">
        <div className="text-neon-green mb-6">
          <CheckCircle2 size={80} />
        </div>
        <h2 className="text-3xl font-black uppercase italic mb-2">Treino Concluído!</h2>
        <p className="text-gray-400 text-center mb-10">Como você avalia a intensidade de hoje?</p>
        
        <div className="w-full max-w-xs space-y-6">
          <div className="flex justify-between text-neon-green font-black text-4xl font-mono">
            <span>{esforco}</span>
            <span className="text-xs text-gray-500 self-end mb-2 uppercase">Escala de Esforço</span>
          </div>
          
          <input 
            type="range" min="1" max="10" step="1"
            value={esforco}
            onChange={(e) => setEsforco(parseInt(e.target.value))}
            className="w-full h-3 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-neon-green"
          />
          
          <div className="flex justify-between text-[10px] text-gray-600 font-bold uppercase">
            <span>Leve</span>
            <span>Moderado</span>
            <span>Insano</span>
          </div>
        </div>

        <div className="mt-12 w-full max-w-xs space-y-3">
          <button 
            onClick={handleFinish}
            className="w-full bg-neon-green text-black font-bold py-5 rounded-2xl shadow-[0_0_30px_rgba(0,255,148,0.2)]"
          >
            CONFIRMAR E SALVAR
          </button>
          <button 
            onClick={() => setIsFinishing(false)}
            className="w-full text-gray-500 text-xs font-bold py-2 uppercase tracking-widest"
          >
            Voltar
          </button>
        </div>
      </div>
    );
  }

  if (isResting) {
    const nextEx = exercicios[currentIndex + 1];
    return (
      <div className="min-h-screen bg-black text-white p-6 flex flex-col items-center justify-center font-sans animate-fade-in">
        <div className="text-neon-green mb-6 animate-pulse">
          <Clock size={80} />
        </div>
        <h2 className="text-2xl font-bold text-gray-500 uppercase tracking-widest mb-2">Descanso</h2>
        <div className="text-9xl font-black text-white mb-12 font-mono">
          {restTime}<span className="text-3xl text-neon-green">s</span>
        </div>
        
        {nextEx && (
          <div className="text-center mb-12 bg-gray-900/50 p-6 rounded-3xl border border-gray-800 w-full max-w-sm">
            <p className="text-xs text-gray-500 uppercase font-bold mb-2">Próximo Exercício</p>
            <p className="text-2xl font-bold text-white mb-1">{nextEx.nome}</p>
            <p className="text-neon-green font-bold">{nextEx.series} • {nextEx.carga}</p>
          </div>
        )}

        <button 
          onClick={skipRest}
          className="bg-white text-black font-bold py-5 px-12 rounded-2xl shadow-[0_0_30px_rgba(255,255,255,0.1)] active:scale-95 transition-all"
        >
          PULAR DESCANSO
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-6 flex flex-col font-sans">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <button onClick={() => navigate(-1)} className="text-gray-400"><ChevronLeft size={30}/></button>
        <div className="flex items-center gap-2 bg-gray-900 px-4 py-2 rounded-full border border-gray-800">
          <Timer size={18} className="text-neon-green" />
          <span className="font-mono font-bold text-neon-green">{formatTime(seconds)}</span>
        </div>
        <div className="w-10"></div>
      </div>

      {/* Progresso Visual */}
      <div className="flex gap-1 mb-10">
        {exercicios.map((_, i) => (
          <div key={i} className={`h-1 flex-1 rounded-full ${i <= currentIndex ? 'bg-neon-green' : 'bg-gray-800'}`}></div>
        ))}
      </div>

      {/* Exercício Atual */}
      <div className="flex-1 flex flex-col items-center justify-center text-center space-y-6">
        <div className="w-64 h-64 bg-gray-900 rounded-3xl border-2 border-neon-green/30 overflow-hidden shadow-[0_0_50px_rgba(0,255,148,0.1)]">
          <img src="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400" className="w-full h-full object-cover" alt="Execução" />
        </div>
        
        <div>
          <h2 className="text-3xl font-black uppercase italic tracking-tighter italic">{currentEx.nome}</h2>
          <p className="text-neon-green font-bold text-xl mt-2">{currentEx.series} • {currentEx.carga}</p>
        </div>

        <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800 w-full max-w-sm">
          <h4 className="text-xs font-bold text-gray-500 uppercase mb-3 text-left flex items-center gap-2">
            <Zap size={14} /> Dica de Execução
          </h4>
          <p className="text-sm text-gray-300 text-left leading-relaxed">
            {currentEx.dica_execucao || "Mantenha a postura ereta e controle a fase excêntrica do movimento por 3 segundos."}
          </p>
        </div>
      </div>

      {/* Controles Inferiores */}
      <div className="mt-auto pt-8 flex gap-4">
        {currentIndex > 0 && (
           <button 
           onClick={() => setCurrentIndex(currentIndex - 1)}
           className="flex-1 bg-gray-900 text-white font-bold py-5 rounded-2xl border border-gray-800"
         >
           ANTERIOR
         </button>
        )}
        
        {currentIndex < exercicios.length - 1 ? (
          <button 
            onClick={handleNext}
            className="flex-[2] bg-white text-black font-bold py-5 rounded-2xl shadow-[0_0_20px_rgba(255,255,255,0.2)]"
          >
            PRÓXIMO EXERCÍCIO
          </button>
        ) : (
          <button 
            onClick={() => setIsFinishing(true)}
            className="flex-[2] bg-neon-green text-black font-bold py-5 rounded-2xl shadow-[0_0_30px_rgba(0,255,148,0.4)]"
          >
            FINALIZAR TREINO
          </button>
        )}
      </div>
    </div>
  );
}