import axios from 'axios';

const state = {
  user: null,
  id: null, 
  authenticated: !!localStorage.getItem('token'),
  tokenExpiry: null
};

const getters = {
  isAuthenticated: state => state.authenticated,
  stateUser: state => state.user,
  stateId: state => state.id,
  tokenExpiry: state => state.tokenExpiry
};

const actions = {
  async createUser({dispatch}, form) {
    await axios.post('users/create_user', form);
    let UserForm = new FormData();
    UserForm.append('username', form.username);
    UserForm.append('password', form.password);
    await dispatch('signIn', UserForm);
  },
  async signIn({ dispatch, commit }, user) {
    try {
      await axios.post('users/sign_in', user);
      localStorage.setItem("token", "JWT");
      commit('signin');
      commit('setTokenExpiry', Date.now() + 60 * 20000);

      await dispatch('viewMe');
    } catch (error) {
      console.error('Sign in error:', error);
    }
  },
  // eslint-disable-next-line no-unused-vars
  async refreshAccessToken({ commit }) {
    try {
      await axios.get('refresh');
      commit('setTokenExpiry', Date.now() + 60 * 20000);

    } catch (error) {
      console.error('Access token refresh error:', error);
    }
  },
  async viewMe({commit}) {
    let {data} = await axios.get('users/me');
    await commit('setUser', data.username, data.id);
    return data;
  },
  async logOut({commit}) {
    let user = null;
    localStorage.removeItem("token");
    commit('logout', user);
  },
  async profilePictureMe() {
    let response = await axios.get('/users/getProfilePicture/me')
    return response.data
  },
  // eslint-disable-next-line no-unused-vars
  async profilePictureUser({commit}, username) {
    let response = await axios.get(`/users/getUserProfilePicture/${username}`)
    return response.data
  },
  // eslint-disable-next-line no-unused-vars
  async uploadProfilePic({commit}, formData) {
    try {
        await axios.post('/users/uploadProfilePicture', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        alert('Profile picture uploaded successfully');
    } catch (error) {
        console.error('Error uploading profile picture:', error);
        alert('Failed to upload profile picture');
    }
  },
  // eslint-disable-next-line no-unused-vars
  async changePassword({commit}, newPassword) {
    return await axios.put("/users/changePassword", newPassword)
  },
  // eslint-disable-next-line no-unused-vars
  async resetPass({ commit }, email) {
    try {
      const response = await axios.put(`/users/resetPassword?email=${email}`);
      return response;
    } catch (error) {
      console.error('Error resetting password:', error);
      throw error;
    }
  }

};

const mutations = {
  setUser(state, username, id) {
    state.user = username;
    state.id = id;
  },
  signin(state) {
    state.authenticated = true;
  },
  logout(state, user){
    state.user = user;
  },
  setTokenExpiry(state, expiry) {
    state.tokenExpiry = expiry;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};