<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <v-card class="pa-4">
          <div class="text-h5">Usuários</div>
          <div class="text-h3">{{ stats.users }}</div>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card class="pa-4">
          <div class="text-h5">Professores</div>
          <div class="text-h3">{{ stats.professores }}</div>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card class="pa-4">
          <div class="text-h5">Secretários</div>
          <div class="text-h3">{{ stats.secretarios }}</div>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card class="pa-4">
          <div class="text-h5">Administradores</div>
          <div class="text-h3">{{ stats.admins }}</div>
        </v-card>
      </v-col>
      <!-- Novo card de Alunos -->
      <v-col cols="3">
        <v-card class="pa-4">
          <div class="text-h5">Estudantes</div>
          <div class="text-h3">{{ stats.estudantes }}</div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import axios from 'axios'

const stats = reactive({
  users: 0,
  admins: 0,
  secretarios: 0,
  professores: 0,
  estudantes: 0      // inicializa
})

async function fetchDashboard() {
  try {
    const res = await axios.get(import.meta.env.VITE_API_URL + '/dashboard')
    Object.assign(stats, res.data)  // inclui também stats.alunos
  } catch (err) {
    console.error('Erro ao carregar dashboard:', err)
  }
}

onMounted(fetchDashboard)
</script>
