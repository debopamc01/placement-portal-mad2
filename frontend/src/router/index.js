import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';

import AdminDashboard from '@/views/AdminDashboard.vue';
import CompanyDashboard from '@/views/CompanyDashboard.vue';
import StudentDashboard from '@/views/StudentDashboard.vue';

import PlacementDriveView from '@/views/PlacementDriveView.vue';
import CompanyView from '@/views/CompanyView.vue';
import StudentView from '@/views/StudentView.vue';
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
      path: '/register',
      name: 'register',
      component: RegisterView,
    },

    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminDashboard,
    },

    {
      path: '/student',
      name: 'student-dashboard',
      component: StudentDashboard,
    },

    {
      path: '/company',
      name: 'company-dashboard',
      component: CompanyDashboard,
    },

    {
      path: '/student/profile',
      name: 'student-profile',
      component: StudentView,
    },

    {
      path: '/students/:id',
      name: 'student-view',
      component: StudentView,
    },

    {
      path: '/company/profile',
      name: 'company-profile',
      component: CompanyView,
    },

    {
      path: '/companies/:id',
      name: 'company-view',
      component: CompanyView,
    },

    {
      path: '/placement-drives/create',
      name: 'placement-drive-create',
      component: PlacementDriveView,
      props: {
        mode: 'create',
      },
    },

    {
      path: '/placement-drives/:id',
      name: 'placement-drive-view',
      component: PlacementDriveView,
      props: {
        mode: 'view',
      },
    },

    {
      path: '/placement-drives/:id/edit',
      name: 'placement-drive-edit',
      component: PlacementDriveView,
      props: {
        mode: 'edit',
      },
    },

    {
      path: '/applications/:id',
      name: 'application-view',
      component: ApplicationView,
    },
  ],
});

export default router;