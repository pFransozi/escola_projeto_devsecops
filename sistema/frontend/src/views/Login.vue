<template>
  <button @click="loginCognito">Entrar com Cognito</button>
</template>

<script setup>
const domain      = import.meta.env.VITE_COGNITO_DOMAIN;
const clientId    = import.meta.env.VITE_COGNITO_CLIENT_ID;
const redirectUri = import.meta.env.VITE_REDIRECT_URI;

function loginCognito() {
  const loginUrl = 
    `https://${domain}/login` +
    `?client_id=${clientId}` +
    `&response_type=token` +
    `&scope=openid+email` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}`;
  window.location.href = loginUrl;
}
</script>
