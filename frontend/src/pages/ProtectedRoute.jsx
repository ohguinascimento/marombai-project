import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
  // Verifica se o token existe no localStorage
  const token = localStorage.getItem('marombai_token');

  if (!token) {
    // Se não houver token, redireciona para o login
    // O 'replace' impede que o usuário volte para a página protegida ao clicar no botão 'Voltar'
    return <Navigate to="/login" replace />;
  }

  // Se estiver autenticado, renderiza as rotas filhas (Dashboard, Diário, etc)
  return <Outlet />;
};

export default ProtectedRoute;