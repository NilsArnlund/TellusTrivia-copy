<template>
  <div class="text-center text-white">
    <figure>
      <img src="../assets/logos/logo_transparent.png" />
    </figure>
    <p style="font-size: large;">Correct guess was: <span style="color: green; font-weight: bold;">{{ currentCorrect }}</span></p>
    <span class="countdown text-6xl">
      <span :style="{ '--value': timerRoundOver }"></span>
    </span>
    <table class="table w-1/2 mx-auto">
      <thead>
        <tr class="text-white">
          <th></th>
          <th>User</th>
          <th>Score</th>
          <th>Guess</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index" :class="{ 'alive': item.is_alive }" style="align-items: center;">
          <td class="large-text">
            <div class="flex items-center gap-3">
              <div class="avatar">
                <div class="mask mask-squircle w-12 h-12">
                  <img :src="'data:image/jpeg;base64,' + profilePictures[item.username]" alt="Profile Picture" />
                </div>
              </div>
            </div>
          </td>
          <td>{{ item.username }}</td>
          <td>{{ item.score }}</td>
          <td>{{ getCountry(item.current_guess) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
  <script>

  import countryCodeData from '../assets/countryCodes.json';
  
  export default {
    name: 'RoundOverComponent',
    props: {
      data: {
        type: Object,
        required: true
      },
      timerRoundOver: {
        type: Number,
        required: false
      },
      profilePictures: {
        type: Object,
        required: false
      },
      currentCorrect: {
        type: String,
        required: false
      }
    },
    data() {
      return {
      };
    },
    methods: {
      // Set the correct format of loaded picture
      getProfilePicture(username) {
            return 'data:image/jpeg;base64,' + (this.profilePictures[username] || '');
        },
      // Convert country code to country name
      getCountry(countryCode) {
        return countryCodeData[countryCode]
      }
    },
  };
  </script>

<style>
.alive {
  background-color: green;
}
</style>
  