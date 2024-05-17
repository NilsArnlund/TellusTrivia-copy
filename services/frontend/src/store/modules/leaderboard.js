import axios from 'axios';


const actions = {
    async getTop20() {
        let {data} = await axios.get('/leaderboard/');
        return data
    },
    // eslint-disable-next-line no-unused-vars
    async getUserTop20({commit}, username) {
        let { data } = await axios.get(`/leaderboard/${username}`);
        return data;
    },
    async getMeTop10() {
        let { data } = await axios.get(`/leaderboard/me`);
        return data;
    },
    async getTodaysTop10() {
        let { data } = await axios.get(`/leaderboard/today`);
        return data;
    }
};

export default {
  actions,
};