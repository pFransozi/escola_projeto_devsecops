<template>
  <v-app>
    <!-- Barra superior, navegação lateral e demais componentes existentes -->
    <router-view />

    <!-- Snackbar global de erros HTTP -->
    <v-snackbar
      v-model="showError"
      :timeout="6000"
      top
      right
      elevation="2"
    >
      {{ errorMsg }}
      <template #action>
        <v-btn icon @click="showError = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Snackbar global de sucessos HTTP -->
    <v-snackbar
      v-model="showSuccess"
      :timeout="4000"
      top
      right
      color="success"
      elevation="2"
    >
      {{ successMsg }}
      <template #action>
        <v-btn icon @click="showSuccess = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, onUnmounted } from 'vue';
import { getToken, scheduleTokenCheck } from './utils/auth';

const showError = ref(false);
const errorMsg = ref('');
const showSuccess = ref(false);
const successMsg = ref('');

function handleHttpError(event) {
  errorMsg.value = event.detail;
  showError.value = true;
}

function handleHttpSuccess(event) {
  successMsg.value = event.detail;
  showSuccess.value = true;
}

onMounted(() => {
  // Inicializa token e checagem periódica
  const token = getToken();
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    scheduleTokenCheck();
  }

  // Registra listeners para mensagens globais
  window.addEventListener('http-error', handleHttpError);
  window.addEventListener('http-success', handleHttpSuccess);
});

onUnmounted(() => {
  window.removeEventListener('http-error', handleHttpError);
  window.removeEventListener('http-success', handleHttpSuccess);
});
</script>
