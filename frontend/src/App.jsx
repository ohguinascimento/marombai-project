import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard'; // <--- Importe aqui
import AdminUsers from './pages/AdminUsers'; // <--- ADICIONE ESTA LINHA

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Onboarding />} />
        <Route path="/dashboard" element={<Dashboard />} /> {/* <--- Nova Rota */}
        <Route path="/admin" element={<AdminUsers />} /> {/* <--- ADICIONE ESTA LINHA */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;