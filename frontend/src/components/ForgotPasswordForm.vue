<template>
  <article>
    <header class="row form-heading">
      <img src="../assets/logo.jpg" alt="">
      <h4>Forgot password?</h4>
    </header>
    <section class="row form-section">
      <form class="col s12 m4 offset-m4 card-panel" method="post">
        <div class="row">
          <div class="input-field col s12">
            <input v-validate="'required|email'" class="validate" type="email" name="email" v-model="email" />
            <label for="email">Enter your email</label>
            <span class="red-text" v-show="errors.has('email')">{{ errors.first('email') }}</span>
          </div>
        </div>
        <div class="row">
          <div class="input-field button-container col s12">
            <button type="submit" name="btn_forgotPassword" class="waves-effect waves-light btn" v-on:click="changePassword">Change password</button>
          </div>
        </div>
      </form>
    </section>
    <footer class="row">
      <router-link to="/login">
        <h6 class="blue-text">
          <b>Back to login</b>
        </h6>
      </router-link>
    </footer>
  </article>
</template>

<script>
  import usersApi from '../api/users.js'
  
  export default {
    name: 'forgotPassword-form',
    data() {
      return {
        email: ''
      }
    },
    methods: {
      changePassword: function(event) {
        event.preventDefault();
        // TODO
      }
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
  
  footer {
    h6 {
      text-align: center;
    }
  }
</style>