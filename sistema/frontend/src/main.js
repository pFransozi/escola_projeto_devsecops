/**
 * Ponto de entrada da aplicação Vue.
 * Configura o axios, Vuetify (incluindo Labs) e inicializa o app com router.
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import axios from 'axios'

// Axios: define baseURL e interceptor de autenticação
axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// Labs (para usar VDataTable e outros componentes alfa)
import * as labsComponents from 'vuetify/labs/components'

const vuetify = createVuetify({
  components: {
    // componentes estáveis
    ...components,
    // componentes Labs (inclui VDataTable)
    ...labsComponents,
  },
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
})

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
