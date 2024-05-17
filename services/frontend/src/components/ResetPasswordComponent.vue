<template>
  <div class="card-body items-center text-center">        
    <div class="form-control">
      <form @submit.prevent="resetPassword">
        <label class="input input-warning w-full max-w-xs bg-transparent text-white flex items-center gap-2 input-group mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70">
            <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
            <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
          </svg>
          <input type="text" class="grow" v-model="email" placeholder="Email" />
        </label>
        <button class="btn btn-warning hover:btn-outline" type="submit">Recover</button>
      </form>
    </div>

    <div v-if="successMessage" class="text-green-500 mt-2">
      {{ successMessage }}
    </div>
  
    <div v-if="errorMessage" class="text-red-500 mt-2">
      {{ errorMessage }}
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
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    ...mapActions(['resetPass']),
    // Method that sends an email containing a new password to the user
    async resetPassword() {
      try {
        const response = await this.resetPass(this.email);
        if (response.status === 200) {
          this.successMessage = 'Password reset successful.';
          this.errorMessage = ''; 
        } else {
          if (response.data && response.data.detail === "No user found for email: apa@hej.se") {
            this.errorMessage = 'Email not found in database.';
          } else {
            this.errorMessage = 'An error occurred. Please try again later.';
          }
          this.successMessage = ''; 
        }
      } catch (error) {
        console.error('Error resetting password:', error);
        this.errorMessage = 'An error occurred. Please try again later.';
        this.successMessage = '';
      }
    },
    backToLogin() {
      this.$emit('backToLogin');
    }
  }
};
</script>

  