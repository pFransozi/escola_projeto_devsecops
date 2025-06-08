import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// Carrega do .env
const domain       = import.meta.env.VITE_COGNITO_DOMAIN      
const clientId     = import.meta.env.VITE_COGNITO_CLIENT_ID  
const logoutUri    = import.meta.env.VITE_LOGOUT_REDIRECT_URI

export function useHomeLogic() {
  const router = useRouter()
  const menuAberto = ref(false)

  const user = ref(
    JSON.parse(localStorage.getItem('user')) || {
      nome: '',
      ultimo_nome: '',
      tipo: ''
    }
  )

  const initials =
    (user.value.nome  ? user.value.nome.charAt(0)       : '') +
    (user.value.ultimo_nome ? user.value.ultimo_nome.charAt(0) : '')

  function logout() {
    // 1. Limpa todos os tokens e dados do usuário no front
    localStorage.removeItem('idToken')
    localStorage.removeItem('accessToken')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']

    // 2. Monta a URL de logout do Cognito (observe o caminho "/logout")
    const logoutUrl =
      `https://${domain}/logout?` +
      `client_id=${clientId}` +
      `&logout_uri=${encodeURIComponent(logoutUri)}`

    // 3. Redireciona para o Hosted UI do Cognito, encerrando a sessão lá
    window.location.href = logoutUrl
  }

  return { user, initials, menuAberto, logout }
}
