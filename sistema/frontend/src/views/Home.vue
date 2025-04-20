<template>
  <v-app>
    <!-- Barra superior -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Sistema Escolar</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Avatar com menu suspenso ativado corretamente -->
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

    <!-- Menu lateral -->
    <v-navigation-drawer app>
      <v-list nav dense>
        <v-list-item to="/home/dashboard" link>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item to="/home/usuario" link>
          <v-list-item-title>Cadastro de Usuário</v-list-item-title>
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
import { useHomeLogic } from '../composables/useHomeLogic.js'
const { user, initials, menuAberto, logout } = useHomeLogic()
</script>