<template>
  <article>
    <header class="row form-heading">
      <img src="/static/dist/logo.jpg" alt="">
      <h4>Login to Carbonara</h4>
    </header>
    <section class="row form-section">
      <form class="col s12 m6 offset-m3 card-panel" method="post">
        <div class="row">
          <div class="input-field col s12">
            <input v-validate="'required|email'" class="validate" type="email" name="email" v-model="email" />
            <label for="email">Enter your email</label>
            <span class="red-text" v-show="errors.has('email')">{{ errors.first('email') }}</span>
          </div>
        </div>
        <div class="row">
          <div class="input-field col s12">
            <input v-validate="'required'" class="validate" type="password" name="password" v-model="password" />
            <label for="password">Enter your password</label>
            <span class="red-text" v-show="errors.has('password')">{{ errors.first('password') }}</span>
          </div>
        </div>
        <div class="row">
          <div class="col s12">
            <label style="float: right;">
                    <router-link to="/forgotPassword">
                      <h6 class="pink-text">
                        <b>Forgot Password?</b>
                      </h6>
                    </router-link>
                  </label>
          </div>
        </div>
        <div class="row">
          <div class="input-field button-container col s12">
            <button type="submit" name="btn_login" class="waves-effect waves-light btn" v-on:click="login">Login</button>
          </div>
        </div>
      </form>
    </section>
    <footer class="row">
      <div class="col s12 m6 offset-m3 center-align">
        <a class="oauth-container btn darken-4 white black-text" href="/users/google-oauth/" style="text-transform:none">
          <div class="left">
            <img width="20px" style="margin-top:7px; margin-right:8px;" alt="Google &quot;G&quot; Logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
          </div>
          Login with Google
        </a>
      </div>
      <br>
      <div class="col s12">
        <router-link to="/register">
          <h6 class="blue-text">
            <b>Create an account</b>
          </h6>
        </router-link>
      </div>
    </footer>
  </article>
</template>

<script>
  import usersApi from '../api/users.js'
  
  export default {
    name: 'login-form',
    data() {
      return {
        email: '',
        password: ''
      }
    },
    methods: {
      login: function(event) {
        event.preventDefault();
        usersApi.login(this.email, this.password, this.$route.query.redirect)
      }
    },
    created: function() {
      // Check if user is already logged in
      let access_token = localStorage.getItem('access_token')
      if (access_token !== null) {
        this.$store.commit('login', {
          access_token: localStorage.getItem('access_token'),
          username: localStorage.getItem('username')
        })
        this.$router.push({
          path: '/'
        })
      }
  
      // Update breadcrumbs
      this.$store.commit('updateBreadcrumbs', {
        breadcrumb: null
      })
    }
  }
</script>

<style lang="scss">
  .form-heading {
    margin-top: 64px;
    display: flex;
    flex-direction: column;
    align-items: center;
    img {
      border-radius: 50%;
      width: 100px;
      height: 100px;
    }
    h4 {
      text-align: center;
    }
  }
  
  .form-section {
    padding-left: 16px;
    padding-right: 16px;
    form {
      padding: 48px !important;
      padding-top: 32px !important;
      padding-bottom: 32px !important;
    }
    .button-container {
      display: flex;
      justify-content: center;
    }
  }
  
  #githubBtnCenterText {
    text-align: center;
  }
  
  footer {
    a {
      color: black;
    }
    .oauth-container {
      margin: 8px 0;
      min-width: 180px;
    }
    h6 {
      text-align: center;
    }
  }
</style>
