import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, User, Volume2, VolumeX, Save, LogOut, Bell, Lock, RefreshCcw, Eye, EyeOff } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL;

export default function SettingsPage() {
  const navigate = useNavigate();
  const userId = localStorage.getItem('marombai_user_id');
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);
  const [showPass, setShowPass] = useState({
    current: false,
    new: false,
    confirm: false
  });
  
  // Estado para preferências do App
  const [soundEnabled, setSoundEnabled] = useState(() => {
    return localStorage.getItem('marombai_sound_enabled') !== 'false';
  });

  // Estado para dados do Perfil
  const [profile, setProfile] = useState({
    nome: '',
    peso: '',
    altura: '',
    idade: '',
    objetivo: ''
  });

  // Estado para campos de senha
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${API_URL}/user/${userId}/dashboard`);
        if (response.ok) {
          const data = await response.json();
          setProfile({
            nome: data.user.nome,
            peso: data.user.peso,
            altura: data.user.altura,
            idade: data.user.idade,
            objetivo: data.user.objetivo
          });
        }
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      } finally {
        setLoading(false);
      }
    };
    if (userId) fetchUserData();
  }, [userId]);

  const handleSave = async () => {
    setSaving(true);
    try {
      // 1. Salva preferências locais
      localStorage.setItem('marombai_sound_enabled', soundEnabled.toString());
      localStorage.setItem('marombai_user_nome', profile.nome);

      // 2. Salva dados no Backend
      const response = await fetch(`${API_URL}/user/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      });

      if (response.ok) {
        alert("Configurações salvas com sucesso!");
        navigate('/dashboard');
      }
    } catch (error) {
      alert("Erro ao salvar configurações.");
    } finally {
      setSaving(false);
    }
  };

  const handleUpdatePassword = async () => {
    if (!passwordData.currentPassword || !passwordData.newPassword) {
      alert("Preencha a senha atual e a nova senha.");
      return;
    }
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert("As novas senhas não coincidem!");
      return;
    }

    setChangingPassword(true);
    try {
      const response = await fetch(`${API_URL}/user/${userId}/password`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          old_password: passwordData.currentPassword,
          new_password: passwordData.newPassword
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Senha alterada com sucesso!");
        setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      } else {
        alert(data.detail || "Erro ao alterar senha.");
      }
    } catch (error) { alert("Erro de conexão."); }
    finally { setChangingPassword(false); }
  };

  if (loading) return <div className="min-h-screen bg-dark-bg flex items-center justify-center text-neon-green">Carregando...</div>;

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 font-sans">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <button onClick={() => navigate(-1)} className="p-2 bg-gray-900 rounded-xl text-gray-400">
          <ChevronLeft size={24} />
        </button>
        <h1 className="text-2xl font-bold">Configurações</h1>
      </div>

      <div className="space-y-8">
        {/* Seção Perfil */}
        <section>
          <div className="flex items-center gap-2 mb-4 text-gray-500 uppercase text-xs font-bold tracking-widest">
            <User size={14} /> Perfil do Atleta
          </div>
          <div className="bg-card-bg rounded-2xl border border-gray-800 p-4 space-y-4">
            <div>
              <label className="text-[10px] text-gray-500 block mb-1">NOME</label>
              <input 
                className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 text-sm focus:border-neon-green outline-none"
                value={profile.nome}
                onChange={(e) => setProfile({...profile, nome: e.target.value})}
              />
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-[10px] text-gray-500 block mb-1">PESO (KG)</label>
                <input 
                  type="number"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 text-sm focus:border-neon-green outline-none"
                  value={profile.peso}
                  onChange={(e) => setProfile({...profile, peso: e.target.value})}
                />
              </div>
              <div>
                <label className="text-[10px] text-gray-500 block mb-1">ALTURA (CM)</label>
                <input 
                  type="number"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 text-sm focus:border-neon-green outline-none"
                  value={profile.altura}
                  onChange={(e) => setProfile({...profile, altura: e.target.value})}
                />
              </div>
              <div>
                <label className="text-[10px] text-gray-500 block mb-1">IDADE</label>
                <input 
                  type="number"
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 text-sm focus:border-neon-green outline-none"
                  value={profile.idade}
                  onChange={(e) => setProfile({...profile, idade: e.target.value})}
                />
              </div>
            </div>
          </div>
        </section>

        {/* Seção Alterar Senha */}
        <section>
          <div className="flex items-center gap-2 mb-4 text-gray-500 uppercase text-xs font-bold tracking-widest">
            <Lock size={14} /> Segurança
          </div>
          <div className="bg-card-bg rounded-2xl border border-gray-800 p-4 space-y-4">
            <div>
              <label className="text-[10px] text-gray-500 block mb-1">SENHA ATUAL</label>
              <div className="relative">
                <input 
                  type={showPass.current ? "text" : "password"}
                  className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 pr-10 text-sm focus:border-neon-green outline-none"
                  value={passwordData.currentPassword}
                  onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                  placeholder="******"
                />
                <button onClick={() => setShowPass({...showPass, current: !showPass.current})} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">
                  {showPass.current ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] text-gray-500 block mb-1">NOVA SENHA</label>
                <div className="relative">
                  <input 
                    type={showPass.new ? "text" : "password"}
                    className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 pr-10 text-sm focus:border-neon-green outline-none"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                    placeholder="******"
                  />
                  <button onClick={() => setShowPass({...showPass, new: !showPass.new})} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">
                    {showPass.new ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>
              <div>
                <label className="text-[10px] text-gray-500 block mb-1">CONFIRMAR</label>
                <div className="relative">
                  <input 
                    type={showPass.confirm ? "text" : "password"}
                    className="w-full bg-dark-bg border border-gray-700 rounded-lg p-3 pr-10 text-sm focus:border-neon-green outline-none"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                    placeholder="******"
                  />
                  <button onClick={() => setShowPass({...showPass, confirm: !showPass.confirm})} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">
                    {showPass.confirm ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>
            </div>
            <button 
              onClick={handleUpdatePassword}
              disabled={changingPassword}
              className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-white text-xs font-bold rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {changingPassword ? "ATUALIZANDO..." : "ATUALIZAR SENHA"}
              <RefreshCcw size={12} className={changingPassword ? "animate-spin" : ""} />
            </button>
          </div>
        </section>

        {/* Seção Preferências do App */}
        <section>
          <div className="flex items-center gap-2 mb-4 text-gray-500 uppercase text-xs font-bold tracking-widest">
            <Bell size={14} /> Aplicativo
          </div>
          <div className="bg-card-bg rounded-2xl border border-gray-800 overflow-hidden">
            <button 
              onClick={() => setSoundEnabled(!soundEnabled)}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-800/30 transition-colors"
            >
              <div className="flex items-center gap-3">
                {soundEnabled ? <Volume2 className="text-neon-green" size={20} /> : <VolumeX className="text-gray-500" size={20} />}
                <span className="text-sm">Bipes de Descanso</span>
              </div>
              <div className={`w-10 h-5 rounded-full relative transition-colors ${soundEnabled ? 'bg-neon-green' : 'bg-gray-700'}`}>
                <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${soundEnabled ? 'left-6' : 'left-1'}`}></div>
              </div>
            </button>
          </div>
        </section>

        {/* Botão Salvar */}
        <button 
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-neon-green text-black font-bold py-4 rounded-xl flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(0,255,148,0.2)] active:scale-95 transition-all disabled:opacity-50"
        >
          <Save size={20} />
          {saving ? "SALVANDO..." : "SALVAR ALTERAÇÕES"}
        </button>
      </div>
    </div>
  );
}