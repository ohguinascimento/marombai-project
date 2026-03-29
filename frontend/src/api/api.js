import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log("🔌 MarombAI API Base URL:", API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor de Requisição: Adiciona o Token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('marombai_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de Resposta: Lida com expiração de token (401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.clear(); // Limpa tudo em caso de token inválido
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;