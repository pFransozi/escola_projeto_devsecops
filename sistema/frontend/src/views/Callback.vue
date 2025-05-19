<template>
  <div>Processando autenticação…</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter }    from 'vue-router';

const router = useRouter();

onMounted(() => {
  const hash = window.location.hash;
  if (hash.startsWith('#')) {
    const params = new URLSearchParams(hash.slice(1));
    const idToken     = params.get('id_token');
    const accessToken = params.get('access_token');

    if (idToken)     localStorage.setItem('idToken', idToken);
    if (accessToken) localStorage.setItem('accessToken', accessToken);
  }
  router.replace('/home'); // volta à rota home
});
</script>
