<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="pa-6" width="400" elevation="10">
      <!-- Título -->
      <v-card-title class="text-h5 justify-center mb-4">
        Entrar no Sistema
      </v-card-title>

      <v-form @submit.prevent="loginLocal" ref="form" lazy-validation>
        <v-text-field
          v-model="usuario"
          label="Usuário"
          prepend-icon="mdi-account"
          :rules="[rules.required]"
          required
        />

        <v-text-field
          v-model="senha"
          label="Senha"
          prepend-icon="mdi-lock"
          type="password"
          :rules="[rules.required]"
          required
        />

        <v-btn
          type="submit"
          color="primary"
          class="mt-4"
          block
          :loading="carregandoLocal"
        >
          Entrar
        </v-btn>

        <v-alert v-if="erroLocal" type="error" class="mt-4" dense>
          {{ erroLocal }}
        </v-alert>
      </v-form>

      <!-- Separador visual -->
      <v-divider class="my-4" />

      <!-- Botão de login via Cognito -->
      <v-btn
        color="orange darken-2"
        class="mt-2"
        block
        :loading="carregandoCognito"
        @click="loginCognito"
      >
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

// Estado
const usuario           = ref('')
const senha             = ref('')
const erroLocal         = ref('')
const carregandoLocal   = ref(false)
const erroCognito       = ref('')
const carregandoCognito = ref(false)
const form              = ref(null)

// Validação
const rules = {
  required: v => !!v || 'Este campo é obrigatório'
}

// Router e ambiente
const router      = useRouter()
const apiUrl      = import.meta.env.VITE_API_URL
const domain      = import.meta.env.VITE_COGNITO_DOMAIN
const clientId    = import.meta.env.VITE_COGNITO_CLIENT_ID
const redirectUri = import.meta.env.VITE_REDIRECT_URI

// Configura Axios se já houver ID Token
const existing = localStorage.getItem('token')
if (existing) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${existing}`
}

// Login local (backend)
async function loginLocal() {
  erroLocal.value = ''
  if (!(await form.value.validate())) return

  carregandoLocal.value = true
  try {
    const res = await axios.post(`${apiUrl}/login`, {
      usuario: usuario.value,
      senha:   senha.value
    })
    const { token, user } = res.data
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    router.push('/home')
  } catch (err) {
    console.error('Erro no loginLocal():', err)
    erroLocal.value = 'Usuário ou senha inválidos'
  } finally {
    carregandoLocal.value = false
  }
}

// Login via Cognito Hosted UI
function loginCognito() {
  erroCognito.value       = ''
  carregandoCognito.value = true

  const loginUrl =
    `https://${domain}/login` +
    `?client_id=${clientId}` +
    `&response_type=token` +
    `&scope=openid+email+profile` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}`
  window.location.href = loginUrl
}
</script>
