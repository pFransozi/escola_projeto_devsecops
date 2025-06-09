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
import { useRouter } from 'vue-router'
import axios from 'axios'                   // ← volte a importar o axios global
import { scheduleTokenCheck, parseJwt, setToken } from '../utils/auth'
// import { authClient } from '../utils/authClient'
import { api } from '../utils/api'

const router = useRouter()
const erro = ref('')

// Chave para salvar o usuário
const USER_KEY = 'user'

onMounted(async () => {
  try {
    // 1) Lê o "code" da query string
    const params = new URLSearchParams(window.location.search)
    const code = params.get('code')
    if (!code) {
      erro.value = 'Código de autorização não encontrado na URL.'
      return
    }

    // 2) Recupera o PKCE verifier
    const codeVerifier = sessionStorage.getItem('pkce_verifier')
    if (!codeVerifier) {
      erro.value = 'Code verifier não encontrado. Tente login novamente.'
      return
    }
    sessionStorage.removeItem('pkce_verifier')

    // 3) Troca o code por tokens no back-end
    //    Capturamos a resposta em `res`
    const res = await api.post('/api/auth/callback', {
      code,
      code_verifier: codeVerifier
    })

    // 4) Armazena o ID Token e agenda expiração
    const idToken = res.data.id_token
    setToken(idToken)
    scheduleTokenCheck()

    // 5) Injeta o header Authorization nas próximas requisições
    axios.defaults.headers.common['Authorization'] = `Bearer ${idToken}`

    // 6) Decodifica o JWT para pegar nome, sobrenome e email
    const payload = parseJwt(idToken)
    const givenName = payload.given_name || ''
    const familyName = payload.family_name || ''
    const email = payload.email || ''

    localStorage.setItem(
      USER_KEY,
      JSON.stringify({ nome: givenName, ultimo_nome: familyName, email })
    )

    // 7) Limpa a query string e navega para /home
    window.history.replaceState(null, '', window.location.pathname)
    router.replace('/home')

  } catch (e) {
    console.error('Erro no Callback.vue:', e)
    erro.value = 'Falha ao processar o callback de autenticação.'
  }
})
</script>
