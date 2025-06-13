/**
 * Ponto de entrada da aplicação Vue.
 * Configura o axios, Vuetify e inicializa o app com router.
 */

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

/**
 * Define a URL base para todas as requisições axios.
 * A variável VITE_API_URL deve estar definida em .env.
 */
axios.defaults.baseURL = import.meta.env.VITE_API_URL

/**
 * Interceptor de requisições axios:
 * adiciona header Authorization com o token armazenado.
 * @param {import('axios').AxiosRequestConfig} config 
 * @returns {import('axios').AxiosRequestConfig}
 */
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

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
