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
    localStorage.clear()
    menuAberto.value = false
    router.push('/login')
  }

  return { user, initials, menuAberto, logout }
}
