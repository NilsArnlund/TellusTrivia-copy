<template>
  <div class="min-h-screen" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');">
      <div class="">
      <div class="h-screen flex">
        <!-- Left column Round timer and connected users -->
        <div class="w-1/5 p-1 text-center">
          <span :class="{ 'text-gray-600': !showTimer, 'text-white': showTimer }" class="countdown text-6xl">
            <span :style="{ '--value': showTimer ? timerGuess : 0 }"></span>
          </span>
          <div v-show="isUsersObjectNotEmpty">
            <UsersListComponent :data="usersObject" :profilePictures="profilePictures"/>
          </div>
        </div>

        <!-- Middle column -->
        <div class="w-3/5 h-full flex flex-col">
          <div class="outline outline-warning outline-1 h-1/2 p-1">
            <!-- Show RoundOver/GameStart/GameOverComponent else Show the round Image in the upper half of middle column-->
            <div v-if="isRoundOverObjectNotEmpty">
              <RoundOverComponent :data="roundOverObject" :timerRoundOver="timerRoundOver" :profilePictures="profilePictures" :currentCorrect="currentCorrect"/>
            </div>
            <div v-show="!gameStarted">
              <GameStartComponent :timerGameStart="timerGameStart" :toggleStart="toggleStart" :roomID="roomID"/>
            </div>
            <div v-if="gameOverObject" class="text-center">
              <GameOverComponent :data="gameOverObject" :profilePictures="profilePictures" :currentCorrect="currentCorrect"/>
              <button class="btn btn-warning btn-outline mt-4" @click="$router.push('/home')">Exit game</button>
              <span v-show="isRoomLeader">
                <button class="btn btn-warning btn-outline ml-4 mt-4" @click="restartGame">Play again</button>
              </span>
            </div>
            <!-- Display start and guess buttons on top of the image and map -->
            <div class="buttons-container">
              <button class="btn btn-warning" @click="startGame" v-show="!toggleStart && isRoomLeader">Start!</button>
              <button class="btn btn-warning" v-show="selectedCountry !== null && toggleStart" @click="userGuessed(selectedCountry)">
                Guess
              </button>
            </div>
            <div class="image-container" @wheel="zoomImage">
              <img :src="pictureUrl" alt="Random Picture" v-show="!isRoundOverObjectNotEmpty && gameStarted && !gameOverObject" class="zoomable-image"/>
            </div>
            

          </div>

          <!-- Map component in lower half of middle col -->
          <div class="outline outline-warning outline-1 h-1/2 p-1">
            <div class="h-full" :class="{ 'map-disabled': !isUserAlive || !gameStarted || timerRoundOver }">
              <MapComponent ref="mapComponent" @country-selected="handleCountrySelected" />
            </div>
          </div>
        </div>

        <!-- Right column chatComponent -->
        <div class="w-1/5 p-1 overflow-hidden" style="display: flex; flex-direction: column; height: 100vh;">
          <div ref="chatContainer" style="flex-grow: 1; overflow-y: auto;">
            <ChatComponent :profilePictures="profilePictures" :chatMessagesObject="chatMessages"/>
          </div>

          <!-- Form at the bottom -->
          <form @submit.prevent="onMessageFormSubmit" id="message-form">
            <div style="margin-top: 2;">
              <input v-model="message" type="text" id="message" placeholder="Enter your message" class="input input-warning max-w-52 bg-transparent text-white items-center gap-2 input-group mb-2">
              <button type="submit" class="btn btn-warning btn-outline">Send</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import MapComponent from '@/components/MapComponent.vue';
import UsersListComponent from '@/components/UsersListComponent.vue';
import RoundOverComponent from '@/components/RoundOverComponent.vue';
import GameStartComponent from '@/components/GameStartComponent.vue';
import GameOverComponent from '@/components/GameOverComponent.vue'
import ChatComponent from '@/components/ChatComponent.vue'
import countryCodeData from '../assets/countryCodes.json';

export default {
  name: 'PingStatus',
  components: {
    MapComponent,
    UsersListComponent,
    RoundOverComponent,
    GameStartComponent,
    GameOverComponent,
    ChatComponent,
  },
  data() {
    return {
      roomID: '',
      clientID: null,
      ws: null,
      message: '',
      pictureUrl: null,
      selectedCountry: '',
      gameStarted: null,
      hasGuessed: null,
      usersObject: {},
      isUsersObjectNotEmpty: false,
      isUserAlive: true,
      isRoomLeader: false,
      roundOverObject: {},
      isRoundOverObjectNotEmpty: false,
      timerGuess: null,
      showTimer: false,
      timerRoundOver: null,
      timerGameStart: null,
      toggleStart: false,
      gameOverObject: null,
      profilePictures: {},
      currentCorrect: null,
      chatMessages: [],
    };
  },
  watch: {
    usersObject: {
        // Method that updates object regarding a user
        async handler(newData) {
            // Handle empty or undefined usersObject
            if (!newData || Object.keys(newData).length === 0) {
                this.isUsersObjectNotEmpty = false;
                return;
            }
            // Iterate through the usersObject
            this.isUsersObjectNotEmpty = true;
            for (const key in newData) {
                const userData = newData[key];
                // Check for the current user based on clientID
                if (key == this.clientID) {
                    this.isUserAlive = userData.is_alive;
                    this.isRoomLeader = userData.is_room_leader;
                }
                const username = userData.username;
                // Fetch profile picture if not already fetched
                if (!this.profilePictures[username]) {
                    await this.getUserProfilePic(username);
                }
            }            
        },
        immediate: true,
    },
  },
  methods: {
    ...mapActions(['viewMe', 'getGameStates', 'getGameStatesEndOfRound', 'profilePictureUser' ]),
    async getUserProfilePic(username) {
        const profilePictureData = await this.profilePictureUser(username);
        this.profilePictures[username] = profilePictureData;
    },
    // Method that zooms the image on mouse scroll
    zoomImage(event) {
      const image = event.target;
      if (event.deltaY < 0) {
        image.classList.add('zoomed');
      } else {
        image.classList.remove('zoomed');
      }
    },
    // Method that scrolls the chat container to bottom to see new messages as they appear
    scrollToBottom() {
      this.$refs.chatContainer.scrollTop = this.$refs.chatContainer.scrollHeight;
    },
    async getMessage() {
        try {            
            let response = await this.viewMe();
            this.clientID = response.id;
        } catch (error) {
            console.error('Error occurred while fetching data:', error);
            window.alert("Token expired!");
        }
    },
    async processMessage(event) {
      const d = JSON.parse(event.data);
      // check what d.type is and call the corresponding functions
      switch(d.type){
        // Pushes a message to the chatComponent
        case "message":
          this.chatMessages.push({user: d.player_id, message: d.msg});
          this.$nextTick(() => {
            this.scrollToBottom();
          });
          break;
        // Pushes that a user has connected to the chatComponent and updates gameStates object
        case "connected":
          this.chatMessages.push({user: d.player_id, message: d.msg});
          this.$nextTick(() => {
            this.scrollToBottom();
          });
          this.usersObject = await this.getGameStates(this.roomID);
          break;
        // Starts the game
        case "start_game":
          this.toggleStart = true;
          this.$nextTick(() => {
            this.scrollToBottom();
          });
          break;
        // Starts a new round, loads data and resets variables
        case "start_round":
          this.$refs.mapComponent.resetMap(); // Reset map (Remove polygon and set default location)
          this.pictureUrl = d.picture; // Loads new picture
          this.hasGuessed = false;
          this.selectedCountry = null;
          this.$nextTick(() => {
            this.scrollToBottom();
          });
          break;
        // A client has made a guess, update  gameState object to show new information
        case "has_guessed":
          this.usersObject = await this.getGameStates(this.roomID);
          this.showTimer = true;
          break;
        // All users have guessed or timer ran out
        // Get the gameStates and gameStatesEndOfRound
        // Disable timer
        case "round_over":
          this.usersObject = await this.getGameStates(this.roomID);
          this.roundOverObject = await this.getGameStatesEndOfRound(this.roomID);
          this.showTimer = false;
          this.isRoundOverObjectNotEmpty = true;
          break;
        // Set what the correct guess what
        case "round_end":
          this.currentCorrect = countryCodeData[d.correct_guess];
          break;
        // All clients have died
        // Get game states and display the game score
        case "game_over":
          this.showTimer = false;
          this.usersObject = await this.getGameStates(this.roomID);
          this.gameOverObject = this.usersObject;
          this.selectedCountry = null;
          break;
        // Show round starting timer with the time gotten from server
        // When the timer reaches 0 start the game
        case "timer_round_start":
          this.timerGameStart = d.timer;
          if (d.timer == 0) {
            this.gameStarted = true;
          }
          break;
        // A client has guessed
        // Start timer to show the user how much time is left in the round
        case "timer_has_guessed":
          this.timerGuess = d.timer;
          break;
        // Show round over timer with time from server
        case "timer_round_over":
          this.timerRoundOver = d.timer;
          if (d.timer == 0) {
            this.isRoundOverObjectNotEmpty = false;
          }
          break;
        // The server has updated some critical game state data and requests that the clients update the object
        case "update_object":
          this.usersObject = await this.getGameStates(this.roomID);
          break;
        // Round timer has ran out
        // If this user has not already guessed send the current selected country as a guess
        case "times_up":
          if (this.hasGuessed == false) {
            this.userGuessed(this.selectedCountry);
          }
          break;
        // Game restarted by lobbyleader
        // Reset variables to allow for a seamless transition to new game
        case "restart_game":
          this.$refs.mapComponent.resetMap();
          this.usersObject = await this.getGameStates(this.roomID);
          this.gameStarted = false;
          this.hasGuessed = false;
          this.isUserAlive = true;
          this.timerRoundOver = null;
          this.timerGameStart = null;
          this.toggleStart = false;
          this.gameOverObject = null;

          break;
        // Get scores
        case "scores":
          this.usersObject = await this.getGameStates(this.roomID);
          break;
      }
      
    },
    // Method that connects the websocket to the room with this users clientID
    onRoomFormSubmit(roomID) {
      const wsURL = `ws://localhost:5000/ws/${roomID}/${this.clientID}`;
      this.ws = new WebSocket(wsURL);
      this.ws.onmessage = this.processMessage;
    },
    // Sends a message through the websocket
    onMessageFormSubmit() {
      if (this.ws) {
        this.ws.send(JSON.stringify({ type: "message", msg: this.message, player_id: this.clientID }));
        this.message = '';
      }
    },
    // Sends start game to server
    startGame() {
      if (this.ws) {
        this.ws.send(JSON.stringify({ type: "start_game"}));
      }
    },
    // Sends the clients guess to server
    userGuessed(guess) {
      this.hasGuessed = true;
      if (this.ws) {
        this.ws.send(JSON.stringify({ type: "user_guessed", player_id: this.clientID, current_guess: guess}));
      }
    },
    // Sends restart game to server
    restartGame() {
      if (this.ws) {
        this.ws.send(JSON.stringify({ type: "restart_game" }));
      }
    },
    // Updates selected country
    handleCountrySelected(countryCode) {
      this.selectedCountry = countryCode;
    },
  },
  mounted() {
    this.roomID = this.$route.params.roomID;
    this.getMessage().then(() => {
        // Once getMessage has completed, call onRoomFormSubmit with roomID
        this.onRoomFormSubmit(this.roomID);
    });
  },
  // Ensures that the socket gets disconnected when navigating from/ closing this view
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },
};

</script>

<style>
  .map-disabled {
      opacity: 0.5;
      pointer-events: none;
  }

  .image-container {
      height: 100%;
      width: 100%;
      overflow: hidden;
    }

  .zoomable-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.2s ease;
    transform-origin: center; 
  }

  .zoomable-image.zoomed {
    transform: scale(2);
  }

  .buttons-container {
    display: flex;
    justify-content: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1; /* Ensure the buttons are displayed on top of other content */
  }
</style>
