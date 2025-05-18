import { ref } from 'vue'
import { useRouter } from 'vue-router'

export function useHomeLogic() {
  const router = useRouter()
  const menuAberto = ref(false)

  const user = ref(JSON.parse(localStorage.getItem('user')) || {
    nome: '',
    ultimo_nome: '',
    tipo: ''
  })

  const initials = user.value.nome[0] + user.value.ultimo_nome[0]

  function logout() {
  localStorage.removeItem('user')
  localStorage.removeItem('userId')
  router.push({ name: 'Login' })
}


  return { user, initials, menuAberto, logout }
}
