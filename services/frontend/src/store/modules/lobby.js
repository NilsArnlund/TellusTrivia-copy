import axios from 'axios';

const actions = {
  async createLobbyID() {
    let {data} = await axios.get('/sockets/lobbyID');
    return data
  },
  // eslint-disable-next-line no-unused-vars
  async verifyLobbyID({commit}, lobbyID) {
      // Send lobbyID as a query parameter in the URL
      let { data } = await axios.get('/sockets/verify_lobbyID', {
          params: {
              lobby_id: lobbyID
          }
      });
      return data.exists;
  },
  // eslint-disable-next-line no-unused-vars
  async getGameStates({commit}, lobbyID) {
    let { data } = await axios.get('/sockets/get_game_states_data', {
      params: {
          lobby_id: lobbyID
      }
    });
    return data;
  },
  // eslint-disable-next-line no-unused-vars
  async getGameStatesEndOfRound({commit}, lobbyID) {
    let { data } = await axios.get('/sockets/get_game_states_data_end_of_round', {
      params: {
          lobby_id: lobbyID
      }
    });
    return data;
  }
};



export default {
  actions,
};