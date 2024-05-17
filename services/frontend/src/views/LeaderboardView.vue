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
                <form @submit.prevent="submit" class="mb-2">
                    <input v-model="username" type="text" placeholder="Search for username..." id="leaderboard_username" class="input input-warning w-full max-w-xs bg-transparent text-white">
                    <button class="btn btn-warning btn-outline" type="submit" id="leaderboard-submit">Enter</button>
                </form>
                <div v-if="showErrorMessage" class="error-message" style="color: red;">
                    Leaderboard search for that user gave no results.
                </div>
                <LeaderboardComponent :data="leaderboardData" @usernameClicked="submitClicked" />
            </div>
        </div>
    </div>
</template>


    
<script>

import { mapActions } from 'vuex';
import LeaderboardComponent from '@/components/LeaderboardComponent';

export default {
name: 'LeaderboardView',
components: {
    LeaderboardComponent
},
data() {
    return {
        leaderboardData: [],
        username: null,
        showErrorMessage: false
    };
  },
async mounted() {
    await this.getTop();
},
methods: {
    ...mapActions(['getTop20', 'getUserTop20']),
    // Method that gets the top20 all time leaderboard entries
    async getTop() {
        this.showErrorMessage = false;
        try {
            this.leaderboardData = await this.getTop20();
        }
        catch (error) {
            console.error('error:', error);
            this.showErrorMessage = true;
        }
    },
    async submit() {
        this.showErrorMessage = false;
        if (!this.username) {
            return this.getTop();
        }
        try {
            this.leaderboardData = await this.getUserTop20(this.username);
        }
        catch (error) {
            console.error('error:', error);
            this.showErrorMessage = true;
        }
    },
    async submitClicked(username) {
        this.showErrorMessage = false;

        try {
            this.leaderboardData = await this.getUserTop20(username);
        }
        catch (error) {
            console.error('error:', error);
            this.showErrorMessage = true;
        }
    }
}

};
</script>