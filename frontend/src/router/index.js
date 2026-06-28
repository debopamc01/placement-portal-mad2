import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '@/views/LoginView.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import RegisterView from '@/views/RegisterView.vue';
import CompanyDashboard from '@/views/CompanyDashboard.vue';
import StudentDashboard from '@/views/StudentDashboard.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      redirect: '/login',
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },

    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/company',
      name: 'company',
      component: CompanyDashboard,
    },
    {
      path: '/student',
      name: 'student',
      component: StudentDashboard,
    },
  ],
});

export default router;
