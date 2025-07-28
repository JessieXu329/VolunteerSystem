import { createRouter, createWebHistory } from 'vue-router';
import ActivityList from '../views/ActivityList.vue';
import SignUp from '../views/SignUp.vue';

const routes = [
  {
    path: '/',
    name: 'ActivityList',
    component: ActivityList
  },
  {
    path: '/signup/:id',
    name: 'SignUp',
    component: SignUp,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;