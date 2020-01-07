import axios from 'axios'

import router from '../router'
import store from '../store'

const BASE_URL = __API_HOST__;

const anonymousAxios = axios.create({
  baseURL: BASE_URL
})

const normalAxios = axios.create({
  baseURL: BASE_URL
});

let access_token = localStorage.getItem('access_token') != null ? 'Bearer ' + localStorage.getItem('access_token') : null
if (access_token != null)
  normalAxios.defaults.headers.common.Authorization = access_token

normalAxios.interceptors.response.use(function (response) {
  return response;
}, function (error) {
  // Catching not allowed error
  // Here differentation among expired token and not provided token should be made
  if (error.response.status === 403 || error.response.status == 401) {
      console.debug('Credentials missing, redirecting user to login')
      store.commit('logout')
      router.push({ path: '/login' })
      delete normalAxios.defaults.headers.common.Authorization
  } 
  return Promise.reject(error);
});

export default {
  anonymousAxios,
  normalAxios
}