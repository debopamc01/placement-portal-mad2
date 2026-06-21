<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

async function logout() {
  await authStore.logout();
  router.push('/login');
}
</script>

<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between">
      <h1>Admin Dashboard</h1>

      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <hr />

    <div v-if="authStore.user">
      <p>
        <strong>Email:</strong>
        {{ authStore.user.email }}
      </p>

      <p>
        <strong>Role:</strong>
        {{ authStore.user.role }}
      </p>
    </div>
  </div>
</template>
