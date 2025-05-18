<template>
    <v-container class="fill-height d-flex justify-center align-center">
      <v-card class="pa-6" width="400" elevation="10">
        <v-card-title class="text-h5 justify-center mb-4">Entrar no Sistema</v-card-title>
  
        <v-form @submit.prevent="login">
          <v-text-field
            v-model="usuario"
            label="Usuário"
            prepend-icon="mdi-account"
            required
          ></v-text-field>
  
          <v-text-field
            v-model="senha"
            label="Senha"
            prepend-icon="mdi-lock"
            type="password"
            required
          ></v-text-field>
  
          <v-btn
            type="submit"
            color="primary"
            class="mt-4"
            block
            :loading="carregando"
          >
            Entrar
          </v-btn>
  
          <v-alert v-if="erro" type="error" class="mt-4">
            {{ erro }}
          </v-alert>
        </v-form>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const usuario = ref('')
  const senha = ref('')
  const erro = ref('')
  const carregando = ref(false)
  const router = useRouter()
  
  const login = async () => {
    erro.value = ''
    carregando.value = true
  
    try {
      const res = await axios.post(import.meta.env.VITE_API_URL + '/login', {
        usuario: usuario.value,
        senha: senha.value
      })
  
      const user = res.data.user
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('userId', user.id)
      router.push('/home')
      
    } catch (err) {
      erro.value = 'Usuário ou senha inválidos'
      console.error(err)
    } finally {
      carregando.value = false
    }
  }
  </script>
  