import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = ({ allowedRoles = [] }) => {
  // Verifica se o token existe no localStorage
  const token = localStorage.getItem('marombai_token');
  const userRole = localStorage.getItem('marombai_user_role');

  if (!token) {
    // Se não houver token, redireciona para o login
    return <Navigate to="/login" replace />;
  }

  // Se a rota exige papéis específicos e o usuário não os possui
  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    return <Navigate to="/dashboard" replace />;
  }

  // Se estiver autenticado, renderiza as rotas filhas (Dashboard, Diário, etc)
  return <Outlet />;
};

export default ProtectedRoute;