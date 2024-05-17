<template>
  <div class="hero min-h-screen" style="background-image: url(https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);">

  <div class="hero-content text-center">
    
        <div class="card w-96 bg-base">
          <figure>
            <img src="../assets/logos/logo_transparent.png"/>
          </figure>

          <div v-if="!currentComponent">
            <div class="card-body items-center text-center">            
              <div class="form-control">
                <form @submit.prevent="submit">
                  <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-4">
                    
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" /></svg>
                    <input type="text" class="grow" v-model="username" placeholder="Username" />
                  </label>
                  <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
                    <input type="password" class="grow" v-model="password" placeholder="••••••••" />
                  </label>
                  <!-- Error message for unsuccessful login -->
                  <div v-if="showErrorMessage" class="text-red-500 mb-2">
                    Wrong username or password.
                  </div>
                  <button class="btn btn-warning btn-outline " type="submit">Sign in</button>
                </form>
              </div>

              <ul class="menu menu-horizontal">
                <li><a class="link text-white link-hover hover:link-warning" @click="showComponent('register')">Register</a></li>
                <li><a class="link text-white link-hover hover:link-warning" @click="showComponent('resetPassword')">Forgot password?</a></li>
              </ul>
            </div>
          </div>
          <!-- Dynamic component rendering -->
          <component :is="currentComponent" v-if="currentComponent" @backToLogin="backToLogin"></component>
        </div> 
      
    
  </div>
</div>
</template>



<script>
import Register from '../components/RegisterComponent.vue';
import ResetPassword from '../components/ResetPasswordComponent.vue';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: '',
      currentComponent: null,
      showErrorMessage: false,
    };
  },
  // Components that are able to be toggled using buttons in login view
  components: {
    Register,
    ResetPassword
  },
  methods: {
    ...mapActions(['signIn']),
    async submit() {
      const User = new FormData();
      User.append('username', this.username);
      User.append('password', this.password);
      try {
        await this.signIn(User);
        this.$router.push('/home');
      }
      catch (error) {
          console.error('Login error:', error);
          this.showErrorMessage = true;
        }
    },
    showComponent(componentName) {
      this.currentComponent = componentName;
    },
    backToLogin() {
      this.currentComponent = null; // Hide the dynamic component
    }
  }
}

</script>

<style>
</style>