<template>
  <div class="hero min-h-screen" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');">
    <div class="hero-content text-center">
      <div class="card bg-base">
        <figure>
          <img src="../assets/logos/logo_transparent.png" />
        </figure>
        <div class="h-screen flex">
          <!-- Left column: Profile picture and user info -->
          <div class="w-1/2 p-6 flex flex-col justify-start items-center">
            <button class="btn btn-warning btn-outline btn-rounded w-1/2" @click="createLobby">
              <i class="fas fa-plus mr-2"></i>Create Game
            </button>
            <form @submit.prevent="submit" class="flex flex-row gap-2 mt-10">
              <input v-model="roomID" type="text" id="room-id" class="input input-warning w-1/2 bg-transparent border border-warning rounded-md px-3 py-2 text-white" placeholder="Room ID" required>
              <button class="btn btn-warning btn-outline btn-rounded w-1/2" type="submit">Enter</button>
            </form>
            <!-- Error message for invalid lobby ID -->
            <div v-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
            <div class="flex gap-2 mt-10">
              <button class="btn btn-warning btn-outline btn-rounded" @click="routeToLeaderboard">
                Leaderboard
              </button>
              <button class="btn btn-warning btn-outline btn-rounded" @click="routeToProfile">
                Profile
              </button>
            </div>
          </div>

          <!-- Right column: Leaderboard component -->
          <div class="w-1/2 p-6">
            <h1 class="text-white mb-4">TODAY'S TOP SCORERS:</h1>
            <LeaderboardComponent :data="leaderboardData" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// Import Vue Router's useRouter function
import { useRouter } from 'vue-router';
import { mapActions } from 'vuex';
import LeaderboardComponent from '@/components/LeaderboardComponent.vue';


export default {
  name: 'HomeView',
  components: {
    LeaderboardComponent
  },
  data() {
    return {
      roomID: null,
      leaderboardData: [],
    };
  },
  async mounted() {
    await this.getTop();
  },
  methods: {
    ...mapActions(['createLobbyID', 'verifyLobbyID', 'getTodaysTop10']),
    // Get top 10 leaderboard entries created on todays date
    async getTop() {
      try {
          this.leaderboardData = await this.getTodaysTop10();
      }
      catch (error) {
          console.error('error:', error);
          }
      },
    // Create a new game lobby
    async createLobby() {
      try {
        this.roomID = await this.createLobbyID();
        this.onRoomFormSubmit()
      }
      catch (error) {
          console.error('error:', error);
          this.showErrorMessage = true;
        }
    },
    // Join a game lobby using an existing lobbyID
    async submit() {
      try {
        let validID = await this.verifyLobbyID(this.roomID);
        if (validID) {
          this.onRoomFormSubmit()
        }
        else {
          this.roomID = '';
          this.errorMessage = 'Invalid Lobby ID. Please try again.';
        }
      }
      catch (error) {
          console.error('error:', error);
          this.showErrorMessage = true;
        }
    },
    // Reroutes the user to the entered lobbyID
    onRoomFormSubmit() {
      this.$router.push({ path: `/lobby/${this.roomID}` });
    },
  },
  setup() {
    const router = useRouter();

    const routeToLeaderboard = () => {
      router.push('/leaderboard'); 
    };

    const routeToProfile = () => {
      router.push('/profile')
    };

    return {
      routeToLeaderboard,
      routeToProfile,
    };
  },
};
</script>

