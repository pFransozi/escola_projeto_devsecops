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

const userId = localStorage.getItem('userId')
if (userId) {
  axios.defaults.headers.common['X-User-Id'] = userId
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

createApp(App).use(router).use(vuetify).mount('#app')
