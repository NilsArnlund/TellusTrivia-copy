<template>
  <div class="">
      <div class="grid grid-cols-2 gap-4" v-if="secondHalfData"> <!-- Create two columns -->
          <!-- First column -->
          <div class="overflow-x-auto">
              <table class="table">
                  <!-- Table head -->
                  <thead>
                      <tr class="text-white">
                          <th></th>
                          <th>User</th>
                          <th>Score</th>
                          <th>Date</th>
                      </tr>
                  </thead>
                  <tbody>
                      <!-- Loop through first half of  data -->
                      <tr v-for="(item, index) in firstHalfData" :key="index" class="text-white"> 
                          <td>{{ index + 1 }}</td>
                          <td class="large-text">
                              <div class="flex items-center gap-3">
                                  <div class="avatar">
                                      <div class="mask mask-squircle w-12 h-12">
                                          <img :src="'data:image/jpeg;base64,' + profilePictures[item.username]" alt="Profile Picture" />
                                      </div>
                                  </div>
                                  <div>
                                      <div @click="handleUsernameClick(item.username)"
                                            style="cursor: pointer; color: orange;" class="username">
                                          {{ item.username }}
                                      </div>
                                  </div>
                              </div>
                          </td>
                          <td class="large-text">{{ item.score }}</td>
                          <td>{{ formatDate(item.created_at) }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <!-- Second column -->
          <div class="overflow-x-auto" v-if="secondHalfData">
              <table class="table">
                  <!-- Table head -->
                  <thead>
                      <tr class="text-white">
                          <th></th>
                          <th>User</th>
                          <th>Score</th>
                          <th>Date</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(item, index) in secondHalfData" :key="index" class="text-white">
                        <td>{{ index + 11 }}</td> 
                          <td class="large-text">
                              <div class="flex items-center gap-3">
                                  <div class="avatar">
                                      <div class="mask mask-squircle w-12 h-12">
                                          <img :src="'data:image/jpeg;base64,' + profilePictures[item.username]" alt="Profile Picture" />
                                      </div>
                                  </div>
                                  <div>
                                      <div @click="handleUsernameClick(item.username)"
                                            style="cursor: pointer; color: orange;" class="username">
                                          {{ item.username }}
                                      </div>
                                  </div>
                              </div>
                          </td>
                          <td class="large-text">{{ item.score }}</td>
                          <td>{{ formatDate(item.created_at) }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
      <div class="grid gap-4" v-else>
        <div class="overflow-x-auto">
              <table class="table">
                  <!-- Table head -->
                  <thead>
                      <tr class="text-white">
                          <th></th>
                          <th>User</th>
                          <th>Score</th>
                          <th>Date</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(item, index) in firstHalfData" :key="index" class="text-white">
                        <td>{{ index + 1 }}</td>
                          <td class="large-text">
                              <div class="flex items-center gap-3">
                                  <div class="avatar">
                                      <div class="mask mask-squircle w-12 h-12">
                                          <img :src="'data:image/jpeg;base64,' + profilePictures[item.username]" alt="Profile Picture" />
                                      </div>
                                  </div>
                                  <div>
                                      <div @click="handleUsernameClick(item.username)"
                                            style="cursor: pointer; color: orange;" class="username">
                                          {{ item.username }}
                                      </div>
                                  </div>
                              </div>
                          </td>
                          <td class="large-text">{{ item.score }}</td>
                          <td>{{ formatDate(item.created_at) }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </div>
</template>
  
<script>
import { mapActions } from 'vuex';

export default {
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      profilePictures: {}
    };
  },
  computed: {
    // Split the data into two arrays: the first 10 entries and the rest
    firstHalfData() {
      return this.data.slice(0, 10);
    },
    secondHalfData() {
      // Return the rest of the entries from the data prop
      if (this.data.length > 10) {
        return this.data.slice(10);
      }
      else {
        return null
      }
    }
  },
  methods: {
    ...mapActions(['profilePictureUser']),
    async getUserProfilePic(username) {
      const profilePictureData = await this.profilePictureUser(username);
      this.profilePictures[username] = profilePictureData;
    },
    // Remove time part from date object
    formatDate(datetime) {
      const date = new Date(datetime);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); 
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    // Send username clicked to parent
    handleUsernameClick(username) {
      this.$emit('usernameClicked', username);
    }
  },
  watch: {
    // Watch for changes in data prop and fetch profile pictures for new users
    data: {
      immediate: true,
      handler(newData) {
        newData.forEach(item => {
          // Fetch profile picture for each user if it hasn't already been fetched
          if (!this.profilePictures[item.username]) {
            this.getUserProfilePic(item.username);
          }
        });
      }
    }
  }
};
</script>

<style>
th, td {
    font-size: 16px;
}

.large-text {
  font-size: 24px;
  font-weight: bold;
}

.username:hover {
  text-decoration: underline;
}
</style>