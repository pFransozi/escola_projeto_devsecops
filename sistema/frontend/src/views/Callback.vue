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
import { onMounted, ref } from 'vue'
import { useRouter }      from 'vue-router'
import axios              from 'axios'

const router = useRouter()
const erro   = ref('')

const ID_TOKEN_KEY = 'token'
const USER_KEY     = 'user'

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

onMounted(() => {
  try {
    const hash = window.location.hash
    if (!hash.startsWith('#')) {
      erro.value = 'Nenhum token de autenticação encontrado.'
      return
    }

    const params  = new URLSearchParams(hash.slice(1))
    const idToken = params.get('id_token')
    if (!idToken) {
      erro.value = 'ID Token não retornado pelo Cognito.'
      return
    }

    // Salva o token e configura o axios
    localStorage.setItem(ID_TOKEN_KEY, idToken)
    axios.defaults.headers.common['Authorization'] = `Bearer ${idToken}`

    // Decodifica o JWT para extrair nome e sobrenome
    const payload      = parseJwt(idToken)
    const givenName    = payload.given_name  || ''
    const familyName   = payload.family_name || ''
    const email        = payload.email       || ''

    // Salva o usuário no localStorage
    localStorage.setItem(USER_KEY, JSON.stringify({
      nome:        givenName,
      ultimo_nome: familyName,
      email
    }))

    // Limpa o hash da URL
    window.history.replaceState(null, '', window.location.pathname)

    // Redireciona para a Home
    router.replace('/home')

  } catch (e) {
    console.error('Erro no Callback.vue:', e)
    erro.value = 'Falha ao processar o callback de autenticação.'
  }
})
</script>
