import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import LobbyView from '../views/LobbyView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import ProfileView from '../views/ProfileView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: {requiresAuth: true}
  },
  {
    path: '/lobby/:roomID',
    name: 'lobby',
    component: LobbyView,
    meta: {requiresAuth: true}
  },
  {
    path: '/leaderboard',
    name: 'leaderboard',
    component: LeaderboardView,
    meta: {requiresAuth: true}
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: {requiresAuth: true}
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach(async (to, _, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const tokenExpiry = store.getters.tokenExpiry;
    
    // Check if token has expired
    if (tokenExpiry && tokenExpiry < Date.now()) {
      try {
        // Refresh access token
        await store.dispatch('refreshAccessToken');
        next();
      } catch (error) {
        console.error('Failed to refresh access token:', error);
        next('/login');
      }
      return;
    }

    if (store.getters.isAuthenticated) {
      next();
      return;
    }
    
    next('/login'); 
  } else {
    next(); 
  }
});


export default router
