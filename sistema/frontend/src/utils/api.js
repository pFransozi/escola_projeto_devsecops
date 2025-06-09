import axios from 'axios'

export const api = axios.create({
  baseURL: '/',           // aqui o proxy do Nginx já está redirecionando /api → backend
  withCredentials: true
})
