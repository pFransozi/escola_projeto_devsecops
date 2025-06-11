// Arquivo: sistema/frontend/src/utils/api.js

import axios from 'axios';

// 1. A criação e exportação original da instância 'api' é mantida
export const api = axios.create({
  baseURL: '/',
  withCredentials: true
});

// 2. Adicionamos o interceptador diretamente na constante 'api' que já foi exportada
api.interceptors.request.use(
  config => {
    // Pega o token do localStorage a cada requisição
    const token = localStorage.getItem('token');
    if (token) {
      // Se o token existir, anexa ao cabeçalho de autorização
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // Apenas repassa o erro
    return Promise.reject(error);
  }
);