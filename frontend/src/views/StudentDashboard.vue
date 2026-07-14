<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import PlacementDriveTable from '@/components/PlacementDriveTable.vue';

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
async function applyToPlacementDrive(placementDriveId) {
  errorMessage.value = '';
  try {
    const url = '/api/student/applications';
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ placement_drive_id: placementDriveId }),
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = 'Unable to apply to the placement drive';
      return;
    }

    const placementDrive = placementDrives.value.find(
      (placementDrive) => placementDrive.id === placementDriveId,
    );
    if (placementDrive) {
      placementDrive.has_applied = true;
      placementDrive.application_status = data.data.JobApplication.status;
    }
  } catch (error) {
    errorMessage.value = error;
    console.log(error);
  }
}
async function viewPlacementDrive(placementDriveId) {
  router.push(`/placement-drives/${placementDriveId}`);
}
async function exportApplications() {
  errorMessage.value = '';

  try {
    const url = '/api/student/export';
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      errorMessage.value = 'Unable to export applications';
      return;
    }
    alert("Export in progress. Exported file will be emailed once available.")
  } catch (error) {
    errorMessage.value = error;
    console.log(error);
  }
}
onMounted(() => {
  authStore.loadUser();
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
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h4>Applied Placement Drives</h4>
        <button class="btn btn-primary" @click="exportApplications">
          Export to CSV
        </button>
      </div>
      <PlacementDriveTable
        :placement-drives="placementDrives"
        :show-application-status="true"
        :show-placement-drive-status="false"
        :show-company="true"
        :actions="['view', 'apply']"
        @apply="applyToPlacementDrive"
        @view="viewPlacementDrive"
      />
    </div>
  </div>
</template>
