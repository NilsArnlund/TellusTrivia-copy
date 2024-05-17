<template>
    <div>
      <div v-for="(message, index) in chatMessagesObject" :key="index" :class="[message.user === 'Server' ? 'chat-end' : 'chat-start']">
        <div v-if="message.user !== 'Server'" class="flex items-center">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img :src="getProfilePicture(message.user)" alt="Profile Picture" />
            </div>
          </div>
          <div>
            <div class="chat-header text-white">
              {{ message.user }}
            </div>
            <div :class="{'chat-bubble': true, 'chat-bubble-success': message.message === 'Connected to the lobby'}">
              {{ message.message }}
            </div>
          </div>
        </div>
        <div v-else class="flex justify-end mt-2">
          <div class="chat-bubble chat-bubble-warning">
            {{ message.message }}
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
<script>
  export default {
    name: 'ChatComponent',
    props: {
      chatMessagesObject: {
        type: Array,
        required: false
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
        // Format profile picture to correct format 
        getProfilePicture(username) {
            return 'data:image/jpeg;base64,' + (this.profilePictures[username] || '');
        },
    }
  };
  </script>
  
  
    