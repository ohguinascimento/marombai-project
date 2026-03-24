import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard'; // <--- Importe aqui
import AdminUsers from './pages/AdminUsers'; // <--- ADICIONE ESTA LINHA
import AdminWorkouts from './pages/AdminWorkouts'; // <--- IMPORTAR A NOVA PÁGINA
import AdminDiets from './pages/AdminDiets';
import DietPage from './pages/DietPage';
import DiaryPage from './pages/DiaryPage'; // <--- IMPORTAR A PAGINA DE DIARIO
import EvolutionPage from './pages/EvolutionPage'; // <--- IMPORTAR A PAGINA DE EVOLUCAO
import Login from './pages/Login';

function App() {
  // DEBUG: Se isso não aparecer no console (F12), o código não atualizou!
  console.log("🚀 App.jsx atualizado! Rotas registradas: /login, /dieta, /dietas, /treinos, /admin, /dashboard");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Onboarding />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} /> {/* <--- Nova Rota */}
        <Route path="/admin" element={<AdminUsers />} /> {/* <--- ADICIONE ESTA LINHA */}
        <Route path="/treinos" element={<AdminWorkouts />} /> {/* <--- NOVA ROTA */}
        <Route path="/dietas" element={<AdminDiets />} />
        <Route path="/dieta" element={<DietPage />} />
        <Route path="/diario" element={<DiaryPage />} /> {/* <--- NOVA ROTA DIARIO */}
        <Route path="/evolucao" element={<EvolutionPage />} /> {/* <--- NOVA ROTA EVOLUCAO */}
        
        {/* Rota Coringa (*) para capturar páginas não encontradas */}
        <Route path="*" element={
          <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
            <h1 className="text-2xl font-bold text-gray-500">404 | Página não encontrada</h1>
          </div>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;