<template>
  <article>
    <header class="row s12 form-heading">
      <img src="../assets/logo.jpg" alt="">
      <h4>Register to Carbonara</h4>
    </header>
    <section class="row s12 form-section">
      <form class="col s12 m6 offset-m3 card-panel" method="post">
        <div class='row'>
          <div class='input-field col s12'>
            <input v-validate="'required'" class='validate' type='text' name='firstName' v-model="first_name" id='firstName' />
            <label for='firstName'>Enter your first name</label>
          </div>
          <div class='input-field col s12'>
            <input v-validate="'required'" class='validate' type='text' name='lastName' v-model="last_name" id='lastName' />
            <label for='lastName'>Enter your last name</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field col s12">
            <input v-validate="'required|email'" class="validate" type="email" name="email" v-model="email" autocomplete="false" />
            <label for="email">Enter your email</label>
            <span class="red-text" v-show="errors.has('email')">{{ errors.first('email') }}</span>
          </div>
        </div>
        <div class="row">
          <div class="input-field col s12">
            <input class="validate" type="password" name="password" v-model="password" autocomplete="false" />
            <label for="password">Enter your password</label>
          </div>
        </div>
        <div class='row'>
          <div class='input-field col s12'>
            <input class='validate' type='password' name='confirm-password' v-model="confirmPassword" autocomplete="false" />
            <label for='confirm-password'>Confirm your password</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field button-container col s12">
            <button type="submit" name="btn_login" class="waves-effect waves-light btn" v-on:click="register">Register</button>
          </div>
        </div>
      </form>
    </section>
    <footer class="row">
      <router-link to="/login">
        <h6 class="blue-text">
          <b>Already registered? Login</b>
        </h6>
      </router-link>
    </footer>
  </article>
</template>

<script>
  import usersApi from '../api/users.js'
  import router from '../router.js'
  
  export default {
    name: 'register-form',
    data() {
      return {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    },
    methods: {
      verifyEmail: function(){
        return true;
        // return usersApi.verifyEmail(email);
      },
      register: function(event) {
        event.preventDefault();
        let email = this.email;
        let pass = this.password;
        //if (!verifyEmail()) {
        //  Materialize.toast("Email validation failed", 3000, "rounded");
        //  return;
        //}
        if (this.password === this.confirmPassword && this.password.length >= 6 && this.password.length <= 20) {
          usersApi.register(
              this.first_name,
              this.last_name,
              this.email,
              this.password
            )
            .then(function(response) {
              console.debug(response);
              usersApi.login(email, pass);
              Materialize.toast('Thanks, you\'ve successfully registered to Carbonara!', 3000, 'rounded');
              router.push({
                path: '/dashboard'
              })
            })
            .catch(function(error) {
              Materialize.toast('Sorry, something went wrong!', 3000, 'rounded');
              console.log(error);
            })
        } else if (this.password === this.confirmPassword) {
          this.password = '';
          this.confirmPassword = '';
          Materialize.toast('Password must contain between 8 and 20 characters', 3000, 'rounded');
        } else {
          this.password = '';
          this.confirmPassword = '';
          Materialize.toast('Passwords don\'t correspond', 3000, 'rounded');
        }
      }
    },
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
