<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import PlacementDriveDetails from '@/components/PlacementDriveDetails.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const errorMessage = ref('');

const placementDrive = ref(null);

const allowedActions = computed(() => {
  const role = authStore.user?.role?.toLowerCase();

  switch (role) {
    case 'admin':
      return ['approve', 'decline', 'close', 'reopen', 'edit', 'delete'];
    case 'company':
      return ['close', 'reopen', 'edit', 'delete'];
    case 'student':
      return ['apply'];
    default:
      return [];
  }
});

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function fetchPlacementDriveDetails(placementDriveId) {
  errorMessage.value = '';
  try {
    const userRole = authStore.user.role.toLowerCase();
    const url = `/api/${userRole}/placement-drives/${placementDriveId}`;
    const response = await fetch(url, {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    placementDrive.value = data.data.placement_drive;
    console.log(placementDrive.value);
  } catch (error) {}
}
onMounted(async () => {
  await authStore.loadUser();
  await fetchPlacementDriveDetails(route.params.id);
});
</script>
<template>
  <h2 class="text-center mt-3">Placement Drive Details</h2>
  <PlacementDriveDetails
    v-if="placementDrive"
    :placement-drive="placementDrive"
    mode="view"
    :show-applications-count="true"
    :allowed-actions="allowedActions"
  />

  <div v-else-if="errorMessage" class="alert alert-danger">
    {{ errorMessage }}
  </div>

  <div v-else class="text-center mt-5">Loading...</div>
</template>
