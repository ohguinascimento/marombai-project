import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Lock, ArrowRight, Eye, EyeOff, CheckCircle2, AlertCircle } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL;

export default function ResetPasswordConfirm() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      alert("As senhas não coincidem!");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/reset-password/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        // Redireciona após 3 segundos para o usuário ler a mensagem de sucesso
        setTimeout(() => navigate('/login'), 3000);
      } else {
        alert(data.detail || "Erro ao redefinir senha.");
      }
    } catch (error) {
      console.error("Erro na redefinição:", error);
      alert("Erro de conexão com o servidor.");
    } finally {
      setLoading(false);
    }
  };

  // Caso o link seja acessado sem o token na URL
  if (!token) {
    return (
      <div className="min-h-screen bg-dark-bg text-white flex items-center justify-center p-6">
        <div className="text-center bg-card-bg p-8 rounded-3xl border border-gray-800 shadow-2xl max-w-sm">
          <AlertCircle size={48} className="text-red-500 mx-auto mb-4" />
          <h1 className="text-xl font-bold mb-2">Link Inválido</h1>
          <p className="text-gray-400 mb-6 text-sm">Este link de recuperação está incompleto ou expirado.</p>
          <button onClick={() => navigate('/login')} className="text-neon-green font-bold underline text-sm">Voltar para o Login</button>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-dark-bg text-white flex items-center justify-center p-6">
        <div className="text-center animate-fade-in">
          <CheckCircle2 size={80} className="text-neon-green mx-auto mb-6 drop-shadow-[0_0_15px_rgba(0,255,148,0.4)]" />
          <h1 className="text-3xl font-bold mb-4 italic uppercase">Senha Alterada!</h1>
          <p className="text-gray-400">Sua nova senha foi salva. Redirecionando você para o login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg text-white flex items-center justify-center p-6 font-sans">
      <div className="w-full max-w-md bg-card-bg p-8 rounded-3xl border border-gray-800 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2 italic uppercase">Nova Senha</h1>
          <p className="text-gray-400">Crie uma nova credencial segura para seu acesso.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="text-xs text-gray-500 uppercase tracking-wider font-bold block mb-2">Nova Senha</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-dark-bg border border-gray-700 rounded-xl pl-12 pr-12 py-4 text-white focus:border-neon-green focus:outline-none transition-colors"
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

          <div>
            <label className="text-xs text-gray-500 uppercase tracking-wider font-bold block mb-2">Confirmar Nova Senha</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
              <input
                type={showPassword ? "text" : "password"}
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className={`w-full bg-dark-bg border rounded-xl pl-12 pr-4 py-4 text-white focus:outline-none transition-colors
                  ${confirmPassword && password !== confirmPassword ? 'border-red-500' : 'border-gray-700 focus:border-neon-green'}`}
                placeholder="******"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-neon-green text-black font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-[0_0_15px_rgba(0,255,148,0.3)] disabled:opacity-50 uppercase italic"
          >
            {loading ? 'Processando...' : 'Redefinir Senha'} <ArrowRight size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}