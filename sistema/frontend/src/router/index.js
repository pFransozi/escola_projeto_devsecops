import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import CadastroUsuario from '../views/CadastroUsuario.vue'
import CadastroProfessor from '../views/CadastroProfessor.vue'
import CadastroEstudante from '../views/CadastroEstudante.vue'
import Login from '../views/Login.vue'
import Callback from '../views/Callback.vue'

const routes = [
  { path: '/', redirect: '/login' },

  { 
    path: '/login', 
    name: 'Login', 
    component: Login 
  },

  { 
    path: '/callback', 
    name: 'Callback', 
    component: Callback 
  },

  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/cadastro-usuario',
    name: 'CadastroUsuario',
    component: CadastroUsuario,
    meta: { requiresAuth: true }
  },
  {
    path: '/cadastro-professor',
    name: 'CadastroProfessor',
    component: CadastroProfessor,
    meta: { requiresAuth: true }
  },
  {
    path: '/cadastro-estudante',
    name: 'CadastroEstudante',
    component: CadastroEstudante,
    meta: { requiresAuth: true }
  },
  // adicione aqui outras rotas protegidas, sempre com meta.requiresAuth se precisar
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('idToken')
  const precisaAuth = to.matched.some(r => r.meta.requiresAuth)

  // Se rota protegida e sem token, redireciona para login
  if (precisaAuth && !token) {
    return next({ name: 'Login' })
  }
  // Se for para /login mas já estiver logado, vai ao dashboard
  if (to.name === 'Login' && token) {
    return next({ name: 'Dashboard' })
  }
  next()
})

export default router
