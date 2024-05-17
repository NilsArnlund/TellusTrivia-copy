<template>
  <div class="text-center text-white">
    <figure>
      <img src="../assets/logos/logo_transparent.png" />
    </figure>
    <h1 class="text-white cursor-pointer">Room ID: 
      <span 
        :class="{ 'tooltip': copied }" 
        :style="{ color: 'orange', 'text-decoration': copied ? 'underline' : 'none' }" 
        :data-tooltip="copied ? 'Copied to clipboard' : ''"
        @click="copyRoomID">{{ roomID }}</span>
    </h1>
    <p v-show="!toggleStart">Waiting for lobby leader to start the game...</p>
    <p v-show="toggleStart">Game starting in...</p>
    <span class="countdown text-6xl" v-show="toggleStart">
      <span :style="{ '--value': timerGameStart }"></span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'GameStartComponent',
  props: {
    timerGameStart: {
      type: Number,
      required: false
    },
    toggleStart: {
      type: Boolean,
      required: false
    },
    roomID: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      copied: false
    };
  },
  methods: {
    // Method that allows a user to click the lobbyID and copy it to clipboard
    copyRoomID() {
      const el = document.createElement('textarea');
      el.value = this.roomID;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      
      this.copied = true;

      // Reset the copied state after 1 second
      setTimeout(() => {
        this.copied = false;
      }, 1000);
    },
  }
};
</script>


  