import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import ForgotPasswordForm from './components/ForgotPasswordForm'
import Dashboard from './components/Dashboard/Dashboard'
import User from './components/User/User'
import Upload from './components/Upload'
import Binary from './components/Binary/Binary'
import Procedure from './components/Procedure/Procedure'

import store from './store'
import usersApi from './api/users.js'

const routes = [
    { path: '/login', component: LoginForm },
    { path: '/register', component: RegisterForm },
    { path: '/forgotPassword', component: ForgotPasswordForm, alias: '/changePassword' },
    { path: '/', component: Dashboard },
    { path: '/user/:username', component: User },
    { path: '/dashboard', component: Dashboard, alias: '/home' },
    { path: '/upload', component: Upload },
    { path: '/binary/:md5', component: Binary },
    { path: '/binary/:md5/:offset', component: Procedure }
]

const router = new VueRouter({
    routes
})

function reLoginUser(next) {
    // User credentials are saved but need to be loaded
    store.commit('login',  {
        access_token: localStorage.getItem('access_token'),
        username: localStorage.getItem('username')
    })
    usersApi.retrieveNotifications()
    next()
}

import axiosClients from './api/axiosClients'
import users from './api/users.js';
const normalAxios = axiosClients.normalAxios

function oAuthLogin(query, next) {
    localStorage.setItem('access_token', query.access_token)
    localStorage.setItem('username', query.username)
    normalAxios.defaults.headers.common.Authorization = 'Bearer ' + localStorage.getItem('access_token')
    store.commit('login',  {
        access_token: localStorage.getItem('access_token'),
        username: localStorage.getItem('username')
    })
    usersApi.retrieveNotifications()
    next('/')
}

router.beforeEach((to, from, next) => {
    if (to.path === '/register' || to.path === '/login' || to.path === '/forgotPassword') next();
    else if (to.path === '/oauth') oAuthLogin(to.query, next);
    else if (!localStorage.getItem('logged_in')) router.push({ path: '/login', query: {redirect: to.path}});
    // User credentials are saved but need to be loaded
    else if (store.state.User.username == "") {
        reLoginUser(next);
    }
    else next();
})

export default router
