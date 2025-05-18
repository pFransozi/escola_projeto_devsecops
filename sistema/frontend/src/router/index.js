import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import CadastroUsuario from '../views/CadastroUsuario.vue'
import Login from '../views/Login.vue'
import CadastroProfessor from '../views/CadastroProfessor.vue'
import CadastroEstudante from '../views/CadastroEstudante.vue'

const routes = [

    { path: '/', redirect: '/login' },
    { path: '/login',name:'Login', component: Login },
    {
        path: '/home',
        name: 'Home',
        component: Home,
        children: [
            { path: '', redirect: '/home/dashboard' },
            {
                path: 'dashboard'
                ,name:"Dashboard"
                , component: Dashboard
                , meta: { requiresAuth: true }
            },
            {
                path: 'usuario'
                ,name:'Usuários'
                , component: CadastroUsuario
                , meta: { requiresAuth: true }
            },
            {
                path: 'professor'
                ,name: 'Professores'
                ,component: CadastroProfessor
                ,meta: {requiresAuth: true}
            },
            {
                path: 'estudante'
                ,name: 'Estudantes'
                ,component: CadastroEstudante
                ,meta: {requiresAuth: true}
            }
        ]
    }
]

const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

// Guarda global antes de cada navegação
router.beforeEach((to, from, next) => {
    const userId = localStorage.getItem('userId')
    const precisaAuth = to.matched.some(r => r.meta.requiresAuth)
    
    if (precisaAuth && !userId) {
        // se vai para rota protegida e não há token, manda pra login
        return next({ name: 'Login' })
    }
    // se tenta ir ao login mas já está logado, redireciona ao dashboard
    if (to.name === 'Login' && userId) {
        return next({ name: 'Dashboard' })
    }
    next()
})

export default router