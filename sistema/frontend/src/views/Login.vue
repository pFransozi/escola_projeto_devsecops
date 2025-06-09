<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="pa-6" width="400" elevation="10">
      <v-card-title class="text-h5 justify-center mb-4">
        Entrar no Sistema
      </v-card-title>

      <!-- ===== LOGIN LOCAL ===== -->
      <v-form @submit.prevent="loginLocal" ref="form" lazy-validation>
        <v-text-field v-model="usuario" label="Usuário" prepend-icon="mdi-account" :rules="[rules.required]" required />
        <v-text-field v-model="senha" label="Senha" prepend-icon="mdi-lock" type="password" :rules="[rules.required]"
          required />
        <v-btn type="submit" color="primary" class="mt-4" block :loading="carregandoLocal">
          Entrar
        </v-btn>
        <v-alert v-if="erroLocal" type="error" class="mt-4" dense>
          {{ erroLocal }}
        </v-alert>
      </v-form>

      <!-- ===== DIVISOR ===== -->
      <v-divider class="my-4" />

      <!-- ===== LOGIN COGNITO ===== -->
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import pkceChallenge from 'pkce-challenge'
import { api } from '../utils/api'

const usuario = ref('')
const senha = ref('')
const erroLocal = ref('')
const carregandoLocal = ref(false)
const erroCognito = ref('')
const carregandoCognito = ref(false)
const form = ref(null)

const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL
const domain = import.meta.env.VITE_COGNITO_DOMAIN
const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
const redirectUri = import.meta.env.VITE_REDIRECT_URI

const rules = {
  required: v => !!v || 'Este campo é obrigatório'
}

async function loginLocal() {
  erroLocal.value = ''
  // validação do form (exemplo com vee-validate)
  if (!(await form.value.validate())) return

  carregandoLocal.value = true
  
  try {
    // 1) Faz POST via cookie-based API
    const res = await api.post('/api/auth/login', {
      username: usuario.value,
      password: senha.value
    })

    const { access_token, user } = res.data

    // 1) armazena o JWT
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(user))

    // 2) configura axios para enviar o token em todos os requests
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

    router.push('/home')
  } catch (err) {
    console.error('Erro no loginLocal():', err)
    // Mensagem vinda do backend (por exemplo "Credenciais inválidas")
    erroLocal.value = err.response?.data?.error || 'Usuário ou senha inválidos'
  } finally {
    carregandoLocal.value = false
  }
}

// ===== LOGIN COGNITO PKCE =====
async function loginCognito() {
  erroCognito.value = ''
  carregandoCognito.value = true

  // gera code_verifier + code_challenge
  const { code_verifier, code_challenge } = await pkceChallenge()
  sessionStorage.setItem('pkce_verifier', code_verifier)

  const loginUrl =
    `https://${domain}/oauth2/authorize?` +
    `client_id=${clientId}` +
    `&response_type=code` +
    `&scope=openid+email+profile` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&code_challenge_method=S256` +
    `&code_challenge=${code_challenge}`

  window.location.href = loginUrl
}
</script>
