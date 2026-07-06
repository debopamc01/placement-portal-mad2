import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '@/views/LoginView.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import RegisterView from '@/views/RegisterView.vue';
import CompanyDashboard from '@/views/CompanyDashboard.vue';
import StudentDashboard from '@/views/StudentDashboard.vue';
import PlacementDriveView from '@/views/PlacementDriveView.vue';
import ApplicationView from '@/views/ApplicationView.vue';

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
    {
      path: '/placement-drive/:id',
      name: 'placement-drive-view',
      component: PlacementDriveView,
    },
    {
      path: '/applications/:id',
      name: 'application-view',
      component: ApplicationView,
    },
  ],
});

export default router;
