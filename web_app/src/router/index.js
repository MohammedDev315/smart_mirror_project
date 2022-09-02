import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TrainingView from '../views/TrainingView.vue'
import SettingView from '../views/SettingView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/training',
    name: 'training',
    component: TrainingView
  },  
  {
    path: '/setting',
    name: 'setting',
    component: SettingView
  },


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
