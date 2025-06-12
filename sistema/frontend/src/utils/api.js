import axios from 'axios';

export const api = axios.create({
  baseURL: '/',            // ou '/api' se você tiver roteamento proxy configurado
  withCredentials: true
});

// interceptor de request (já existente)
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status;
    let msg;

    if (status === 403) {
      msg = 'Você não tem permissão para este recurso.';
    } else if (status === 404) {
      msg = 'Recurso não encontrado.';
    } else if (status === 400) {
      msg = error.response.data.message || 'Dados inválidos.';
    } else if (status >= 500) {
      msg = 'Erro interno do servidor.';
    } else {
      msg = error.response.data.message || 'Ocorreu um erro inesperado.';
    }

    window.dispatchEvent(new CustomEvent('http-error', { detail: msg }));
    return Promise.reject(error);
  }
);

api.interceptors.response.use(response => {
  const method = response.config.method;
  const successMsg = response.data.message;

  // apenas criar, atualizar ou deletar
  if (['post','put','delete'].includes(method) && successMsg) {
    window.dispatchEvent(new CustomEvent('http-success', { detail: successMsg }));
  }
  return response;
}, error => Promise.reject(error));