<template>
  <div id="app">
    <navbar></navbar>
    <main>
      <router-view></router-view>
    </main>
    <bottombar></bottombar>
  </div>
</template>

<script>
import Navbar from './elements/Navbar'
import Bottombar from './elements/Bottombar'

import LoginForm from './LoginForm'
import Dashboard from './Dashboard/Dashboard'
import User from './User/User'
import RegisterForm from './RegisterForm'
import ForgotPasswordForm from './ForgotPasswordForm'

import usersApi from '../api/users.js'

export default {
  name: 'app',
  components: {
    Navbar,
    Bottombar
  },
  mounted() {
    let access_token = localStorage.getItem("access_token");
    if (access_token !== undefined){
      usersApi.validateToken(access_token);
    }
  }
}
</script>

<style lang="scss">
body {
  background-color: rgb(247, 249, 248);
}

main {
  min-height: 80vh;
}

// Materialize theme changes
.collection{
  border:none;
}

a {
  color: #26a69a;
}
</style>
