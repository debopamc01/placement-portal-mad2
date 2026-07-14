<script setup>
import { computed } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

defineProps({
  title: {
    type: String,
    required: true,
  },
});

const authStore = useAuthStore();
const router = useRouter();

const user = computed(() => authStore.user);

const dashboardLink = computed(() => {
  console.log(user.value);
  if (!user.value) return '/login';

  switch (user.value.role.toLowerCase()) {
    case 'student':
      return '/student';

    case 'company':
      return '/company';

    case 'admin':
      return '/admin';

    default:
      return '/login';
  }
});

const profileLink = computed(() => {
  if (!user.value) return null;

  switch (user.value.role.toLowerCase()) {
    case 'student':
      return `/students/${user.value.id}/profile`;

    case 'company':
      return `/companies/${user.value.id}`;

    default:
      return null;
  }
});

async function logout() {
  await authStore.logout();
  router.push('/login');
}
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary border rounded shadow-sm mb-4 px-3">
    <div class="container-fluid">
      <div class="d-flex align-items-center">
        <span class="navbar-brand mb-0 fw-bold"> Placement Portal </span>

        <span class="text-secondary ms-3"> | </span>

        <span class="fs-5 fw-semibold ms-3">
          {{ title }}
        </span>
      </div>

      <div v-if="user" class="d-flex align-items-center gap-3">
        <span class="text-muted">
          {{ user.email }}
        </span>

        <RouterLink :to="dashboardLink" class="btn btn-outline-secondary btn-sm">
          Dashboard
        </RouterLink>

        <RouterLink v-if="profileLink" :to="profileLink" class="btn btn-outline-primary btn-sm">
          View Profile
        </RouterLink>

        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>
