<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="pa-6" width="400" elevation="10">
      <!-- Título -->
      <v-card-title class="text-h5 justify-center mb-4">
        Entrar no Sistema
      </v-card-title>

      <v-form @submit.prevent="loginLocal" ref="form" lazy-validation>
        <v-text-field v-model="usuario" label="Usuário" prepend-icon="mdi-account" :rules="[rules.required]"
          required></v-text-field>

        <v-text-field v-model="senha" label="Senha" prepend-icon="mdi-lock" type="password" :rules="[rules.required]"
          required></v-text-field>

        <v-btn type="submit" color="primary" class="mt-4" block :loading="carregandoLocal">
          Entrar
        </v-btn>

        <v-alert v-if="erroLocal" type="error" class="mt-4" dense>
          {{ erroLocal }}
        </v-alert>
      </v-form>

      <!-- Separador visual -->
      <v-divider class="my-4"></v-divider>

      <!-- Botão de login via Cognito -->
      <v-btn color="orange darken-2" class="mt-2" block :loading="carregandoCognito" @click="loginCognito">
        <v-icon left>mdi-aws</v-icon>
        Entrar com Cognito
      </v-btn>

      <v-alert v-if="erroCognito" type="error" class="mt-4" dense>
        {{ erroCognito }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const usuario = ref('')
const senha = ref('')
const erroLocal = ref('')
const erroCognito = ref('')
const carregandoLocal = ref(false)
const carregandoCognito = ref(false)

const rules = {
  required: (v) => !!v || 'Este campo é obrigatório',
}

const router = useRouter()
const form = ref(null)

const domain = import.meta.env.VITE_COGNITO_DOMAIN
const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
const redirectUri = import.meta.env.VITE_REDIRECT_URI
const apiUrl = import.meta.env.VITE_API_URL

const existingToken = localStorage.getItem('token')
if (existingToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${existingToken}`
}

async function loginLocal() {
  // Limpa erros
  erroLocal.value = ''
  // Valida o formulário antes de disparar
  const valid = await form.value.validate()
  if (!valid) {
    return
  }

  carregandoLocal.value = true
  try {
    // Supondo que o back-end devolva { token: "...", user: { ... } }
    const res = await axios.post(`${apiUrl}/login`, {
      usuario: usuario.value,
      senha: senha.value,
    })

    const { token, user } = res.data
    // Armazena o token e o usuário no localStorage
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))

    // Ajusta o header do axios daqui pra frente
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

    // Redireciona para a página principal
    router.push('/home')
  } catch (err) {
    erroLocal.value = 'Usuário ou senha inválidos'
    console.error('Erro no loginLocal():', err)
  } finally {
    carregandoLocal.value = false
  }
}

function loginCognito() {
  erroCognito.value = ''
  carregandoCognito.value = true

  const loginUrl =
    `https://${domain}/login` +
    `?client_id=${clientId}` +
    `&response_type=token` +
    `&scope=openid+email+profile` + 
    `&redirect_uri=${encodeURIComponent(redirectUri)}`

  window.location.href = loginUrl
}

function parseHash(hash) {
  if (!hash || hash.length < 1) {
    return {}
  }
  // Remove o “#” inicial
  const fragment = hash.substring(1)
  const pairs = fragment.split('&')
  const result = {}
  for (const pair of pairs) {
    const [key, value] = pair.split('=')
    if (key && value !== undefined) {
      result[key] = decodeURIComponent(value)
    }
  }
  return result
}

async function trataCallbackCognito() {
  const hash = window.location.hash
  const params = parseHash(hash)

  if (!params.id_token && !params.access_token) {
    carregandoCognito.value = false
    return
  }

  try {
    const token = params.id_token || params.access_token
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

    const me = await axios.get(`${apiUrl}/me`)
    localStorage.setItem('user', JSON.stringify(me.data.user))

    window.history.replaceState(null, '', window.location.pathname)

    router.push('/home')
  } catch (err) {
    console.error('Erro ao tratar callback do Cognito:', err)
    erroCognito.value = 'Falha ao autenticar via Cognito'
    carregandoCognito.value = false
  }
}

onMounted(() => {
  trataCallbackCognito()
})
</script>

<!-- <style scoped>
</style> -->
