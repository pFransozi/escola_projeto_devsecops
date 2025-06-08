<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="pa-4" width="400" elevation="2">
      <v-card-text class="text-center">
        <div v-if="!erro">
          Processando autenticação…
          <v-progress-circular indeterminate class="mt-4"></v-progress-circular>
        </div>
        <v-alert v-else type="error" class="mt-4" dense>
          {{ erro }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
// Callback.vue
import { onMounted, ref } from 'vue'
import { useRouter }      from 'vue-router'
import axios              from 'axios'

// Captura o router e estado de erro
const router = useRouter()
const erro   = ref('')

// Chaves no localStorage
const ID_TOKEN_KEY     = 'idToken'
const ACCESS_TOKEN_KEY = 'accessToken'

// Função para decodificar JWT (ID Token)
function parseJwt(token) {
  const base64 = token.split('.')[1]
    .replace(/-/g, '+')
    .replace(/_/g, '/')
  const json = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  )
  return JSON.parse(json)
}

onMounted(async () => {
  try {
    const hash = window.location.hash
    if (!hash.startsWith('#')) {
      erro.value = 'Nenhum token de autenticação encontrado.'
      return
    }

    // Extrai tokens do fragmento
    const params      = new URLSearchParams(hash.slice(1))
    const idToken     = params.get('id_token')
    const accessToken = params.get('access_token')

    // Remove o hash da URL
    window.history.replaceState(null, '', window.location.pathname)

    if (idToken) {
      // Armazena o ID Token e configura o Axios
      localStorage.setItem(ID_TOKEN_KEY, idToken)
      axios.defaults.headers.common['Authorization'] = `Bearer ${idToken}`

      // Decodifica para obter nome e sobrenome
      const payload = parseJwt(idToken)
      localStorage.setItem('user', JSON.stringify({
        nome:        payload.given_name  || '',
        ultimo_nome: payload.family_name || '',
        email:       payload.email       || ''
      }))

    } else if (accessToken) {
      // Se preferir usar o UserInfo endpoint:
      localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
      const userInfo = await axios.get(
        `https://${import.meta.env.VITE_COGNITO_DOMAIN}/oauth2/userInfo`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      const { given_name, family_name, email } = userInfo.data
      localStorage.setItem('user', JSON.stringify({
        nome:        given_name,
        ultimo_nome: family_name,
        email
      }))
    }

    // Redireciona para a Home
    router.replace('/home')

  } catch (e) {
    console.error('Erro no callback:', e)
    erro.value = 'Falha ao processar autenticação.'
  }
})
</script>
