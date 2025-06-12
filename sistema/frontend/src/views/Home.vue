<template>
  <v-app>
    <!-- Barra superior (mantida igual) -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Sistema Escolar</v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- Menu do usuário (mantido igual) -->
      <v-menu v-model="menuAberto" location="bottom right">
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar color="secondary">
              <span>{{ initials }}</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>{{ user.nome }} {{ user.ultimo_nome }}</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
            <v-list-item-title>Sair</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Menu lateral de navegação -->
    <v-navigation-drawer app>
      <v-list nav dense>
        <v-list-item to="/home/dashboard" link>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/usuario" link>
          <v-list-item-title>Cadastro de Usuário</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/professor" link>
          <v-list-item-title>Cadastro de Professor</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/estudante" link>
          <v-list-item-title>Cadastro de Estudante</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/atividade" link>
          <v-list-item-title>Cadastro de Atividade</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/disciplina" link>
          <v-list-item-title>Cadastro de Disciplina</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/turma" link>
          <v-list-item-title>Cadastro de Turma</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/noticia" link>
          <v-list-item-title>Cadastro de Notícia</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/atividade-escolar" link>
          <v-list-item-title>Cadastro de Atividade Escolar</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/aula" link>
          <v-list-item-title>Cadastro de Aula</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/prova" link>
          <v-list-item-title>Cadastro de Prova</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Conteúdo principal -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { useHomeLogic } from '../composables/useHomeLogic.js'
const { user, initials, menuAberto, logout } = useHomeLogic()

onMounted(() => {
  user.value = JSON.parse(localStorage.getItem('user'))
})
</script>
