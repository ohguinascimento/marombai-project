import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, ArrowRight, RefreshCcw, Eye, EyeOff, Send } from 'lucide-react';
import api from '../api/api.js';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const url = isResetting ? '/auth/reset-password' : '/auth/login';
      const payload = isResetting 
        ? { email: email.trim().toLowerCase() }
        : { email: email.trim().toLowerCase(), password };

      const { data } = await api.post(url, payload);

      if (isResetting) {
        alert("Link de recuperação enviado! Verifique seu e-mail (simulado no terminal do backend).");
        setIsResetting(false);
        setPassword('');
        return;
      }

      // Salva sessão
      localStorage.setItem('marombai_token', data.access_token);
      localStorage.setItem('marombai_user_id', data.user.id);
      localStorage.setItem('marombai_user_nome', data.user.nome);
      localStorage.setItem('marombai_user_role', data.user.role);
      navigate('/dashboard');

    } catch (error) {
      console.error("Erro de login:", error);
      alert(error.response?.data?.detail || "Erro ao tentar realizar a operação.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg text-white flex items-center justify-center p-6 font-sans">
      <div className="w-full max-w-md bg-card-bg p-8 rounded-3xl border border-gray-800 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">{isResetting ? 'Recuperar Senha' : 'Bem-vindo de Volta'}</h1>
          <p className="text-gray-400">{isResetting ? 'Enviaremos um link de recuperação para seu e-mail.' : 'Entre para acessar seus treinos'}</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="text-xs text-gray-500 uppercase tracking-wider font-bold block mb-2">Email</label>
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-dark-bg border border-gray-700 rounded-xl pl-12 pr-4 py-4 text-white focus:border-neon-green focus:outline-none transition-colors"
                placeholder="seu@email.com"
              />
            </div>
          </div>

          {!isResetting && (
            <div>
            <label className="text-xs text-gray-500 uppercase tracking-wider font-bold block mb-2">{isResetting ? 'Nova Senha' : 'Senha'}</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-dark-bg border border-gray-700 rounded-xl pl-12 pr-4 py-4 text-white focus:border-neon-green focus:outline-none transition-colors"
                placeholder="******"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-neon-green text-black font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-[0_0_15px_rgba(0,255,148,0.3)] disabled:opacity-50"
          >
            {loading ? 'Processando...' : (isResetting ? 'Enviar Link de Recuperação' : 'Acessar Conta')} {isResetting ? <Send size={20} /> : <ArrowRight size={20} />}
          </button>
        </form>

        <div className="mt-6 text-center">
          {!isResetting && (
            <button onClick={() => setIsResetting(true)} className="text-xs text-gray-500 hover:text-white mb-4 block w-full">
              Esqueci minha senha
            </button>
          )}
          {isResetting && (
            <button onClick={() => setIsResetting(false)} className="text-xs text-gray-500 hover:text-white mb-4 block w-full">
              Voltar para o Login
            </button>
          )}
          <button onClick={() => navigate('/')} className="text-sm text-gray-500 hover:text-white">
            Não tem conta? <span className="text-neon-green font-bold">Criar agora</span>
          </button>
        </div>
      </div>
    </div>
  );
}