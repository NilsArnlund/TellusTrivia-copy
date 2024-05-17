import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import './app.css';
import store from './store';

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // FastAPI backend


axios.interceptors.response.use(undefined, function (error) {
    if (error) {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
       try {
        store.dispatch('refreshAccessToken')
       }
       catch {
        store.dispatch('logOut');
        return router.push('/login')
      }
      }
    }
  });


app.use(router);
app.use(store);
app.mount("#app");
