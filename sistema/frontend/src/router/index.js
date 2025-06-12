import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import CadastroUsuario from '../views/CadastroUsuario.vue'
import CadastroProfessor from '../views/CadastroProfessor.vue'
import CadastroEstudante from '../views/CadastroEstudante.vue'
import CadastroAtividade from '../views/CadastroAtividade.vue'
import CadastroDisciplina from '../views/CadastroDisciplina.vue'
import CadastroTurma from '../views/CadastroTurma.vue'
import CadastroNoticia from '../views/CadastroNoticia.vue'
import CadastroAtividadeEscolar from '../views/CadastroAtividadeEscolar.vue'
import CadastroAula from '../views/CadastroAula.vue'
import CadastroProva from '../views/CadastroProva.vue'
import Login from '../views/Login.vue'
import Callback from '../views/Callback.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/callback', name: 'Callback', component: Callback },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
    redirect: '/home/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
      },
      {
        path: 'usuario',
        name: 'CadastroUsuario',
        component: CadastroUsuario,
        meta: { requiresAuth: true }
      },
      {
        path: 'professor',
        name: 'CadastroProfessor',
        component: CadastroProfessor,
        meta: { requiresAuth: true }
      },
      {
        path: 'estudante',
        name: 'CadastroEstudante',
        component: CadastroEstudante,
        meta: { requiresAuth: true }
      },
      {
        path: 'atividade',
        name: 'CadastroAtividade',
        component: CadastroAtividade,
        meta: { requiresAuth: true }
      },
      {
        path: 'disciplina',
        name: 'CadastroDisciplina',
        component: CadastroDisciplina,
        meta: { requiresAuth: true }
      },
      {
        path: 'turma',
        name: 'CadastroTurma',
        component: CadastroTurma,
        meta: { requiresAuth: true }
      },
      {
        path: 'noticia',
        name: 'CadastroNoticia',
        component: CadastroNoticia,
        meta: { requiresAuth: true }
      },
      {
        path: 'atividade-escolar',
        name: 'CadastroAtividadeEscolar',
        component: CadastroAtividadeEscolar,
        meta: { requiresAuth: true }
      },
      {
        path: 'aula',
        name: 'CadastroAula',
        component: CadastroAula,
        meta: { requiresAuth: true }
      },
      {
        path: 'prova',
        name: 'CadastroProva',
        component: CadastroProva,
        meta: { requiresAuth: true }
      }
    ]
  },
  // Rota fallback para não autenticados ou caminhos não existentes
  { path: '/:catchAll(.*)', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Redirecionamentos de acordo com autenticação
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const precisaAuth = to.matched.some(r => r.meta.requiresAuth)
  if (precisaAuth && !token) {
    return next({ name: 'Login' })
  }
  if (to.name === 'Login' && token) {
    return next({ name: 'Dashboard' })
  }
  next()
})

export default router
