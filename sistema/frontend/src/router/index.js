import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import CadastroUsuario from '../views/CadastroUsuario.vue'
import Login from '../views/Login.vue'

const routes = [
    
    {path:'/', redirect:'/login'},
    { path: '/login', component: Login },
    {
        path: '/home',
        component: Home,
        children: [
            { path: '', redirect: '/home/dashboard' },
            { path: 'dashboard', component: Dashboard },
            { path: 'usuario', component: CadastroUsuario },
        ]
    }
]

const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

export default router