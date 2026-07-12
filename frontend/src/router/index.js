import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import LoginView from '@/views/LoginView.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import RegisterView from '@/views/RegisterView.vue';
import CompanyDashboard from '@/views/CompanyDashboard.vue';
import StudentDashboard from '@/views/StudentDashboard.vue';
import PlacementDriveView from '@/views/PlacementDriveView.vue';
import ApplicationView from '@/views/ApplicationView.vue';
import StudentView from '@/views/StudentView.vue';
import CompanyView from '@/views/CompanyView.vue';

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
      path: '/placement-drives/create',
      name: 'create-placement-drive',
      component: PlacementDriveView,
      props: { mode: 'create' },
    },
    {
      path: '/placement-drives/:id',
      name: 'view-placement-drive',
      component: PlacementDriveView,
      props: { mode: 'view' },
    },
    {
      path: '/placement-drives/:id/edit',
      name: 'edit-placement-drive',
      component: PlacementDriveView,
      props: { mode: 'edit' },
    },
    {
      path: '/applications/:id',
      name: 'application-view',
      component: ApplicationView,
    },
    {
      path: '/profile',
      redirect: () => {
        const authStore = useAuthStore();
        const userRole = authStore.user?.role?.toLowerCase();
        if (userRole === 'student') return '/student/profile';
        else if (userRole === 'company') return '/company/profile';
        else return '/admin';
      },
    },
    {
      path: '/student/profile',
      name: 'student-profile',
      component: StudentView,
    },
    {
      path: '/company/profile',
      name: 'company-profile',
      component: CompanyView,
    },
    {
      path: '/companies/:id',
      name: 'view-company',
      component: CompanyView,
      props: { mode: 'view' },
      //TODO: update this
    },
    {
      path: '/dashboard',
      redirect: () => {
        const authStore = useAuthStore();
        const userRole = authStore.user?.role?.toLowerCase();
        switch (userRole) {
          case 'student':
            return '/student';

          case 'company':
            return '/company';

          case 'admin':
            return '/admin';

          default:
            return '/login';
        }
      },
    },
  ],
});

export default router;
