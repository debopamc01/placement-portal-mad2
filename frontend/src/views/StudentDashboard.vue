<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

import PlacementDriveTable from '@/components/PlacementDriveTable.vue';

const authStore = useAuthStore();

const errorMessage = ref('');

const placementDrives = ref([]);

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function loadPlacementDrives() {
  errorMessage.value = '';
  try {
    const response = await fetch('/api/student/placement-drives', {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    placementDrives.value = data.data.placement_drives;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load placement drives';
  }
}
onMounted(() => {
  loadPlacementDrives();
});
</script>

<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between">
      <h1>Student Dashboard</h1>

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
