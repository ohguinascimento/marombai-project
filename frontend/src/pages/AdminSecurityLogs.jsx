import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, ShieldAlert, CheckCircle2, XCircle, Clock, Globe, Monitor, BarChart3, Search, Download } from 'lucide-react';
import api from '../api/api.js';

export default function AdminSecurityLogs() {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const { data } = await api.get('/admin/security-logs');
        setLogs(data);
      } catch (error) {
        console.error("Erro ao carregar logs:", error);
        alert("Erro ao carregar logs de segurança.");
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  // Filtro de busca (E-mail ou IP)
  const filteredLogs = logs.filter(log => 
    (log.email && log.email.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (log.ip_address && log.ip_address.includes(searchTerm))
  );

  // Lógica para agrupar dados por dia (Últimos 7 dias)
  const statsByDay = {};
  filteredLogs.forEach(log => {
    const date = new Date(log.created_at).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
    if (!statsByDay[date]) statsByDay[date] = { date, success: 0, failed: 0 };
    if (log.status === 'success') statsByDay[date].success++;
    else if (log.status === 'failed' || log.status === 'user_not_found') statsByDay[date].failed++;
  });

  const chartData = Object.values(statsByDay).reverse().slice(-7);
  const maxVal = Math.max(...chartData.map(d => Math.max(d.success, d.failed)), 1);

  // Função para exportar os logs filtrados para CSV
  const exportToCSV = () => {
    const headers = ['ID', 'Evento', 'Email', 'Status', 'IP Address', 'User Agent', 'Data'];
    const rows = filteredLogs.map(log => [
      log.id,
      log.action === 'request' ? 'SOLICITACAO' : 'CONFIRMACAO',
      log.email,
      log.status,
      log.ip_address || '0.0.0.0',
      `"${log.user_agent?.replace(/"/g, '""')}"`, // Aspas duplas para evitar quebra por vírgulas no UA
      new Date(log.created_at).toLocaleString('pt-BR')
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `marombai_logs_${new Date().toISOString().split('T')[0]}.csv`);
    link.click();
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return <CheckCircle2 size={16} className="text-neon-green" />;
      case 'failed': return <XCircle size={16} className="text-red-500" />;
      default: return <ShieldAlert size={16} className="text-yellow-500" />;
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center text-neon-green font-black italic">
      AUDITANDO SEGURANÇA...
    </div>
  );

  return (
    <div className="min-h-screen bg-dark-bg text-white p-6 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
        <div className="flex items-center gap-4 w-full">
          <button onClick={() => navigate(-1)} className="p-2 bg-gray-900 rounded-xl text-gray-400 hover:text-white transition-colors">
            <ChevronLeft size={24} />
          </button>
          <h1 className="text-2xl font-bold uppercase italic tracking-tighter">Logs de Segurança</h1>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            onClick={exportToCSV}
            disabled={filteredLogs.length === 0}
            className="flex items-center gap-2 px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-xs font-bold text-gray-300 hover:text-neon-green hover:border-neon-green transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            <Download size={16} /> EXPORTAR CSV
          </button>

          <div className="relative w-full md:w-80">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Buscar por e-mail ou IP..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-card-bg border border-gray-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-neon-green focus:outline-none transition-colors text-white"
            />
          </div>
        </div>
      </div>

      {/* Resumo Visual (Gráfico) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 animate-fade-in">
        <div className="lg:col-span-2 bg-card-bg border border-gray-800 rounded-3xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-[10px] text-gray-500 uppercase font-black tracking-widest flex items-center gap-2">
              <BarChart3 size={14} className="text-neon-green" /> Atividade de Reset (Últimos 7 dias)
            </h3>
            <div className="flex gap-4">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-neon-green rounded-full shadow-[0_0_5px_#00FF94]"></div>
                <span className="text-[10px] text-gray-400 font-bold uppercase">Sucesso</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-red-500 rounded-full shadow-[0_0_5px_#EF4444]"></div>
                <span className="text-[10px] text-gray-400 font-bold uppercase">Falha</span>
              </div>
            </div>
          </div>

          <div className="flex items-end justify-between h-32 gap-4 px-2">
            {chartData.map((day, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
                <div className="w-full flex items-end justify-center gap-1 h-full">
                  <div 
                    className="w-full max-w-[8px] bg-neon-green rounded-t-sm transition-all duration-700 ease-out"
                    style={{ height: `${(day.success / maxVal) * 100}%` }}
                  ></div>
                  <div 
                    className="w-full max-w-[8px] bg-red-500 rounded-t-sm transition-all duration-700 ease-out"
                    style={{ height: `${(day.failed / maxVal) * 100}%` }}
                  ></div>
                </div>
                <span className="text-[8px] text-gray-600 font-bold">{day.date}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-neon-green p-6 rounded-3xl text-black flex flex-col justify-between shadow-[0_0_30px_rgba(0,255,148,0.1)]">
          <div>
            <p className="text-[10px] uppercase font-black opacity-60">Eventos Filtrados</p>
            <p className="text-4xl font-black">{filteredLogs.length}</p>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between text-xs font-bold border-b border-black/10 pb-1">
              <span>Taxa de Sucesso</span>
              <span>{filteredLogs.length > 0 ? ((filteredLogs.filter(l => l.status === 'success').length / filteredLogs.length) * 100).toFixed(1) : 0}%</span>
            </div>
            <p className="text-[9px] opacity-50 italic mt-2">Monitoramento ativo contra ataques.</p>
          </div>
        </div>
      </div>

      <div className="bg-card-bg rounded-3xl border border-gray-800 overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-900/50 text-[10px] text-gray-500 uppercase font-black tracking-widest border-b border-gray-800">
                <th className="px-6 py-4">Evento</th>
                <th className="px-6 py-4">E-mail</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">IP / Origem</th>
                <th className="px-6 py-4">Data</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/50">
              {filteredLogs.map((log) => (
                <tr key={log.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4">
                    <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                      log.action === 'request' ? 'bg-blue-500/10 text-blue-400' : 'bg-purple-500/10 text-purple-400'
                    }`}>
                      {log.action === 'request' ? 'SOLICITAÇÃO' : 'CONFIRMAÇÃO'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-300">{log.email}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 text-xs uppercase font-bold">
                      {getStatusIcon(log.status)}
                      <span className={log.status === 'success' ? 'text-neon-green' : 'text-gray-500'}>
                        {log.status}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col gap-1">
                      <div className="flex items-center gap-1 text-[10px] text-gray-400">
                        <Globe size={10} /> {log.ip_address || '0.0.0.0'}
                      </div>
                      <div className="flex items-center gap-1 text-[10px] text-gray-500 truncate max-w-[150px]">
                        <Monitor size={10} /> {log.user_agent}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 text-xs text-gray-400 font-mono">
                      <Clock size={12} /> {new Date(log.created_at).toLocaleString('pt-BR')}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredLogs.length === 0 && <div className="p-12 text-center text-gray-500 text-sm">Nenhum evento corresponde à sua busca.</div>}
        </div>
      </div>
    </div>
  );
}