<template>
    <div class="card-body items-center text-center">        
        <div class="form-control">
        <form @submit.prevent="submit">
            <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" /><path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" /></svg>
            <input type="text" class="grow" v-model="email" placeholder="Email" />
            </label>
            <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" /></svg>
            <input type="text" class="grow" v-model="username" placeholder="Username" />
            </label>
            <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
            <input type="password" class="grow" v-model="password" placeholder="Password" />
            </label>
            <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
            <input type="password" class="grow" v-model="repeatPassword" placeholder="Repeat password" />
            </label>
            <div v-if="!isFormValid" class="text-red-500 mb-2">
              {{ validationError }}
            </div>
            <div v-if="showErrorMessage" class="text-red-500 mb-2">
              Something went wrong. Please try again later.
            </div>
            <button class="btn btn-warning hover:btn-outline" type="submit">Sign up</button>
        </form>
        </div>
        
        <ul class="menu menu-horizontal">
          <li><a class="link text-white link-hover hover:link-warning" @click="backToLogin()">Login</a></li>
        </ul>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';

  export default {
    data() {
      return {
        email: '',
        username: '',
        password: '',
        repeatPassword: '',
        isFormValid: true,
        validationError: '',
        showErrorMessage: false,
      };
    },
    methods: {
      ...mapActions(['createUser']),
      async submit() {
        if (!this.validateForm()) {
          return;
        }

        const user = {
          username: this.username,
          password: this.password,
          email: this.email
        };

        try {
          await this.createUser(user);
          console.log('Registration successful:');
          this.$router.push('/home');
        } catch (error) {
          console.error('Registration error:', error);
          this.showErrorMessage = true;
        }
      },
      backToLogin() {
        this.$emit('backToLogin');
      },
      // Validates parameters in the register form
      validateForm() {
        if (!this.email.includes('@')) {
          this.validationError = 'Please enter a valid email address';
          this.isFormValid = false;
          return false;
        }
        if (this.username.length < 3) {
          this.validationError = 'Username must be at least 3 characters long';
          this.isFormValid = false;
          return false;
        }
        if (this.password !== this.repeatPassword) {
          this.validationError = 'Passwords do not match';
          this.isFormValid = false;
          return false;
        }
        if (this.password.length <  6) {
          this.validationError = 'Password must be at least 6 characters long';
          this.isFormValid = false;
          return false;
        }
        this.isFormValid = true;
        this.validationError = '';
        return true;
      }
    }
  };
  </script>
  