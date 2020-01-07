import qs from 'query-string'

import axiosClients from './axiosClients'
import store from '../store'
import router from '../router'
import utils from '../utils'

const normalAxios = axiosClients.normalAxios
const anonymousAxios = axiosClients.anonymousAxios
const CLIENT_ID = '***'

function login(email, password, redirect) {
    let req = qs.stringify({
        grant_type: 'password',
        client_id: CLIENT_ID,
        username:email,
        password:password
    });
    
    anonymousAxios({
        method: 'POST',
        url: '/users/o/token/',
        data: req
    })
    .then(function(response) {
        console.debug(response);
        store.commit('login', {
            access_token: response.data.access_token,
            username: email
        });
        router.push({ path: redirect || '/' })
        normalAxios.defaults.headers.common.Authorization = 'Bearer ' + localStorage.getItem('access_token')
        retrieveNotifications()
    })
    .catch(function(error) {
        Materialize.toast('Sorry, something went wrong!', 3000, 'rounded');
        console.log(error);
    })
}

function verifyEmail(email) {
    normalAxios({
      method: 'GET',
      url: 'https://apilayer.net/api/check?access_key=' + access_key + '&email=' + email
    })
    .then(function(response) {
        console.debug(response);
        return response.format_valid && !response.disposable && !response.free
    })
    .catch(function(error) {
        Materialize.toast('Error on email validation', 3000, 'rounded');
        console.log(error);
    })
}
  
function register(first_name, last_name, email, password) {
    let req = qs.stringify({
        first_name:first_name,
        last_name:last_name,
        email: email,
        password:password
    });

    return anonymousAxios({
        method: 'POST',
        url: '/users/profile/',
        // TODO: Is this needed ?
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data: req
    })
}

function logout() {
    let req = qs.stringify({
        client_id: CLIENT_ID,
        token: localStorage.getItem('access_token')
    });

    normalAxios({
        method: 'POST',
        url: '/users/o/revoke-token/',
        data: req
    })
    .then(function(response) {
        store.commit('logout')
        router.push({ path: '/login/' })

        delete normalAxios.defaults.headers.common.Authorization
    })
    .catch(function(err) {
        console.log(err)
    })
}

function userInfo(username) {
    normalAxios({
        url: '/users/profile/' + username + '/'
    })
    .then(function (response) {
        store.commit('loadUserInfo', response.data)
    })
    .catch(function (error) {
        console.log(error)  
    });
}

function validateToken(access_token){
    normalAxios({
        method: 'HEAD',
        url: '/users/validate-token/',
    })
    .then(function(response) {
        console.log(response);
    })
    .catch(function(error) {
        console.log(error);
    })
}

function retrieveProfileImg(email) {
    return normalAxios({
        url: '/users/profile/' + email 
    })
}

function changeProfileImg(img){
    let req = qs.stringify({img:img})
    normalAxios({
        method: 'POST',
        url: '/users/change-profile-image/',
        data:req
    })
    .then(function(response) {
        console.log(response);
    })
    .catch(function(error) {
        console.log(error);
    })
}
function editProfile(email,first_name,last_name,bio){   
    let req = qs.stringify({
        email: email,
        first_name: first_name,
        last_name: last_name,
        bio: bio        
    })
    normalAxios({
        method: 'POST',
        url: '/users/profile/' + email + '/modify-profile/',
        data:req
    })
    .then(function(response) {
        console.log(response);
    })
    .catch(function(error) {
        console.log(error);
    })
}

function retrieveNotifications() {
    normalAxios({
        method: 'GET',
        url: '/users/profile/' + localStorage.getItem('username') + '/notifications/'
    })
    .then(function(res) {
        res.data.forEach(e => {
            e.link = utils.createLinkForVote(e)
            e.content = utils.createContentForVote(e)
        });
        store.commit('loadNotificationList', res.data)
    })
    .catch(function(error) {
        console.log(error);
    })
}

export default {
    login,
    register,
    logout,
    userInfo,
    validateToken,
    retrieveProfileImg,
    editProfile,
    retrieveNotifications
}
