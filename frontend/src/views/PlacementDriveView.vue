<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import PlacementDriveDetails from '@/components/PlacementDriveDetails.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const errorMessage = ref('');

const placementDrive = ref(null);

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function openEditModal(placementDriveId) {}
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
  <PlacementDriveDetails
    v-if="placementDrive"
    :placement-drive="placementDrive"
    :can-edit="false"
    @edit="openEditModal"
  />

  <div
    v-else-if="errorMessage"
    class="alert alert-danger"
  >
    {{ errorMessage }}
  </div>

  <div
    v-else
    class="text-center mt-5"
  >
    Loading...
  </div>
</template>
