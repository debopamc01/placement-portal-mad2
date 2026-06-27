<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
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
    const response = await fetch('/api/company/placement-drives', {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    placementDrives.value = data.data.placement_drives;
  } catch (error) {}
}
onMounted(() => {
  loadPlacementDrives();
});
</script>

<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between">
      <h1>Company Dashboard</h1>

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

    <div>
      <table v-if="placementDrives.length" class="table table-striped table-hover">
        <thead>
          <tr>
          <th>Job Title</th>
          <th>Application Deadline</th>
          <th>Status</th>
          <th>Applications</th>
          <th>Actions</th>
        </tr>
        </thead>

        <tbody>
          <tr v-for="placementDrive in placementDrives" :key="placementDrive.id">
            <td>{{ placementDrive.job_title }}</td>
            <td>{{ placementDrive.application_deadline }}</td>
            <td>{{ placementDrive.status }}</td>
            <td>{{ placementDrive.application_ids }}</td>
            <td>{{ placementDrive.application_ids }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
