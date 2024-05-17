<template>
  <div>
    <table style="width: 100%;">
      <tbody>
        <tr v-for="(item, index) in data"
          :key="index"
          :class="{
            'bg-green-500': item.is_alive && item.has_guessed, // green background when alive and has guessed
            'bg-red-500': !item.is_alive, // red background when not alive
            'text-white': item.is_alive && !item.has_guessed // standard background when alive and not guessed
          }">
          <td>
            <div class="flex items-center gap-3">
              <div class="avatar">
                <div class="mask mask-squircle w-12 h-12">
                  <img :src="'data:image/jpeg;base64,' + profilePictures[item.username]" alt="Profile Picture" />
                </div>
              </div>
              <div>
                <div class="font-bold">{{item.username}}</div>
                <div class="font-bold">Score: {{ item.score }}</div>
              </div>
            </div>
          </td>
          <td>
            <div class="avatar">
              <div class="mask mask-squircle w-12 h-12">
                <img src="../assets/svgs/royal-crown-svgrepo-com.svg" alt="Crown SVG" v-show="item.is_room_leader"/>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

  
  <script>
  
  export default {
    name: 'UsersListComponent',
    props: {
      data: {
        type: Object,
        required: true
      },
      profilePictures: {
        type: Object,
        required: false
      }
    },
    data() {
      return {
      };
    },
    methods: {
      // Set the correct format of a loaded profilePicture
      getProfilePicture(username) {
            return 'data:image/jpeg;base64,' + (this.profilePictures[username] || '');
        },
    },
  };
  </script>