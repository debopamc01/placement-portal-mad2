<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import PlacementDriveTable from '@/components/PlacementDriveTable.vue';
import NavBar from '@/components/NavBar.vue';

const router = useRouter();
const authStore = useAuthStore();

const errorMessage = ref('');
const successMessage = ref('');
const loading = ref(false);

const placementDrives = ref([]);
const jobTitle = ref('');
const jobDescription = ref('');
const eligibilityCriteria = ref('');
const applicationDeadline = ref('');

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
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load placement drives';
  }
}
function resetForm() {
  jobTitle.value = '';
  jobDescription.value = '';
  eligibilityCriteria.value = '';
  applicationDeadline.value = '';

  errorMessage.value = '';
  successMessage.value = '';
}
async function closePlacementDrive() {}
async function reopenPlacementDrive() {}
async function editPlacementDrive() {}
async function deletePlacementDrive() {}
async function viewPlacementDrive(placementDriveId) {
  router.push({
    path: `/placement-drives/${placementDriveId}`,
  });
}
onMounted(() => {
  authStore.loadUser();
  loadPlacementDrives();
});
</script>

<template>
  <div class="container mt-5">
    <NavBar :title="'Company Dashboard'" />

    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">Placement Drives</h5>
        <button class="btn btn-outline-primary" @click="router.push('/placement-drives/create')">
          Create New Placement Drive
        </button>
      </div>
      <PlacementDriveTable
        :placement-drives="placementDrives"
        :actions="['close', 'reopen', 'edit', 'view']"
        @close="closePlacementDrive"
        @reopen="reopenPlacementDrive"
        @edit="editPlacementDrive"
        @delete="deletePlacementDrive"
        @view="viewPlacementDrive"
      />
    </div>
  </div>
</template>
