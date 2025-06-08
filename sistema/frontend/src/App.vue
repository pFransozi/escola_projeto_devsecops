<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import axios from 'axios'
import { getToken, scheduleTokenCheck } from './utils/auth'


// Se existir token no storage, configura o Axios e agenda verificação
onMounted(() => {
  const token = getToken()
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    scheduleTokenCheck()
  }
})
</script>