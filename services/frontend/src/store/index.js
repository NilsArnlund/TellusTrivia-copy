import { createStore } from "vuex";

import users from './modules/users';
import lobby from './modules/lobby';
import leaderboard from './modules/leaderboard'

export default createStore({
  modules: {
    users,
    lobby,
    leaderboard,
  }
});