// src/utils/auth.js
import router from '../router'

const TOKEN_KEY = 'token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token){
  localStorage.setItem(TOKEN_KEY, token)
}

export function parseJwt(token) {
  const b64 = token.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')
  return JSON.parse(decodeURIComponent(atob(b64).split('').map(c=>
    '%' + ('00'+c.charCodeAt(0).toString(16)).slice(-2)
  ).join('')))
}

// Checa expiração e, se perto do fim (<2min), avisa ou redireciona
export function scheduleTokenCheck() {
  const token = getToken()
  if (!token) return
  
  const { exp } = parseJwt(token)
  const ms = exp * 1000 - Date.now()
  
  setTimeout(() => {
    alert('Sua sessão expirou. Por favor faça login novamente.')
    logout()
  }, Math.max(ms - 60_000, 0))

  // setTimeout(() => {
  //   alert('Sua sessão expirou. Por favor faça login novamente.')
  //   logout()
  // }, 10_000)
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem('user')
  // opcional: chamar Hosted UI logout do Cognito
  router.push({ name: 'Login' })
}
