// utilizado para uma conexao pura com o backend para poder obter o token, 
// que será utilizado nas demais conexoes.

import axios from 'axios';

export const authClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL
  // NÃO adicionamos interceptors aqui
});
