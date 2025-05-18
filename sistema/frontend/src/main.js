import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import axios from 'axios'

// Base URL da sua API Flask
axios.defaults.baseURL = import.meta.env.VITE_API_URL

// Interceptor: adiciona Authorization: Bearer <idToken> em todas as requisições
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('idToken')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

// Caso você faça alguma requisição antes do interceptor estar registrado,
// seta o header padrão também aqui:
const token = localStorage.getItem('idToken')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi }
  }
})

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
