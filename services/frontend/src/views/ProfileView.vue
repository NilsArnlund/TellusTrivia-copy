<template>
    <div class="hero min-h-screen" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');">
      <div class="hero-content text-center">
        <div class="card bg-base">
          <figure>
            <button class="btn btn-warning btn-outline" style="width: 80px; margin-left: 5%;" @click="$router.push('/home')">
                Home
            </button>
            <img src="../assets/logos/logo_transparent_cropped.png" />
          </figure>
          <div class="h-screen flex">
            <!-- Left column: Profile picture and user info -->
            <div class="w-1/2 p-1 items-center">
              <div class="card bg-base items-center">
                <div class="flex">
                  <!-- Profile picture -->
                  <div class="w-1/2 p-1">
                    <img :src="'data:image/jpeg;base64,' + profilePictureData" alt="Profile Picture" class="profile-picture" />
                  </div>
                  <!-- User information -->
                  <div class="w-1/2 p-2 py-10">
                    <p class="text-white">{{ username }}</p>
                    <p class="text-white">{{ email }}</p>
                    <p class="text-white"><strong>Member since:</strong> {{ formatDate(createdAt) }}</p>
                  </div>
                </div>
                <div>
                  <input type="file" class="file-input file-input-bordered file-input-ghost file-input-warning w-full max-w-xs text-white" @change="handleFileChange" />
                  <button class="btn btn-warning btn-outline mt-2" @click="uploadProfilePicture">Upload</button>
                </div>
                <button class="btn btn-warning btn-outline mt-2" @click="logout">Log out</button>
                <div class="mt-2">
                  <button class="btn btn-warning btn-outline" @click="togglePasswordChangeForm">
                    {{ showPasswordChangeForm ? 'Hide Form' : 'Change Password' }}
                  </button>
                  <!-- Password change form -->
                  <div v-if="showPasswordChangeForm" class="mt-2 flex flex-col">
                    <form @submit.prevent="changePassword">
                      <input type="password" v-model="currentPassword" placeholder="Current Password" class="input input-warning w-full max-w-s bg-transparent text-white" required />
                      <input type="password" v-model="newPassword" placeholder="New Password" class="input input-warning w-full max-w-s bg-transparent text-white mt-2" required />
                      <input type="password" v-model="confirmPassword" placeholder="Confirm New Password" class="input input-warning w-full max-w-s bg-transparent text-white mt-2" required />
                      <button type="submit" class="btn btn-warning btn-outline mt-2">Change Password</button>
                    </form>
                    <div v-if="successMessage" class="text-green-500 mt-2">
                      {{ successMessage }}
                    </div>
                    <div v-if="errorMessage" class="text-red-500 mt-2">
                      {{ errorMessage }}
                    </div>
                  </div>
                </div>
                <div v-if="showErrorMessage" class="text-red-500 mt-2">
                  You have no leaderboard entries
                </div>
              </div>
            </div>
  
            <!-- Right column: Leaderboard component -->
            <div class="w-1/2 p-1">
              <LeaderboardComponent :data="leaderboardData" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  import LeaderboardComponent from '@/components/LeaderboardComponent';
  
  export default {
    name: 'ProfileView',
    components: {
      LeaderboardComponent
    },
    data() {
      return {
        leaderboardData: [],
        username: null,
        profilePictureData: null,
        email: null,
        createdAt: null,
        showErrorMessage: false,
        showPasswordChangeForm: false,
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
        successMessage: '',
        errorMessage: ''
      };
    },
    async mounted() {
      await this.getProfilePicture();
      await this.getTop();
      await this.getUserData();
    },
    methods: {
      ...mapActions(['getMeTop10', 'profilePictureMe', 'viewMe', 'uploadProfilePic', 'changePassword']),
      // Method to get this users top 10 results
      async getTop() {
        this.showErrorMessage = false;
        try {
          this.leaderboardData = await this.getMeTop10();
          console.log(this.leaderboardData)
        }
        catch (error) {
          console.error('error:', error);
          this.showErrorMessage = true;
        }
      },
      // Method to fetch the profile picture data of each leaderboard entry
      async getProfilePicture() {
        try {
          this.profilePictureData = await this.profilePictureMe();
        } catch (error) {
          console.error('Error fetching profile picture data:', error);
        }
      },
      // Method to get this users profile information
      async getUserData() {
        try {
          let data = await this.viewMe();
          this.username = data.username;
          this.email = data.email;
          this.createdAt = data.created_at;
  
        } catch (error) {
          console.error('Error fetching profile picture data:', error);
        }
      },
      // Method to upload a profile picture, only accepts images
      async uploadProfilePicture() {
        if (!this.profilePicture) {
          alert('Please select a file first!');
          return;
        }
  
        const formData = new FormData();
        formData.append('file', this.profilePicture);
        await this.uploadProfilePic(formData);
        this.getProfilePicture();
      },
      handleFileChange(event) {
        let file = event.target.files[0];
        const allowedImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (allowedImageTypes.includes(file.type)) {
          this.profilePicture = file;
        } else {
          window.alert('Please upload a valid image file (JPEG, PNG, or GIF).');
        }
      },
      async logout () {
        await this.$store.dispatch('logOut');
        this.$router.push('/login');
      },
      // Removes the time of a datetime object
      formatDate(datetime) {
        const date = new Date(datetime);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
      },
      togglePasswordChangeForm() {
        this.showPasswordChangeForm = !this.showPasswordChangeForm;
      },
      // Method that allows the user to change the password if the new pass fullfills criterias.
      async changePassword() {
        if (this.newPassword !== this.confirmPassword) {
          this.errorMessage = 'Passwords do not match.';
          this.successMessage = '';
          return;
        }

        if (this.newPassword.length < 5) {
            this.errorMessage = 'Password must be at least 5 characters long.';
            this.successMessage = '';
            return;
        }
  
        try {
          await this.changePassword(this.newPassword);
          this.successMessage = 'Password changed successfully.';
          this.errorMessage = '';
        } catch (error) {
          this.errorMessage = 'Password change failed. Please try again later.';
          this.successMessage = '';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .profile-picture {
    width: 150px; 
    height: 150px;
    border-radius: 10%;
  }
  </style>
  