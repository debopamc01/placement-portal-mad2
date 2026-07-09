<script setup>
import { computed, ref, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import PlacementDriveDetails from '@/components/PlacementDriveDetails.vue';
import ApplicationsTable from '@/components/ApplicationsTable.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const errorMessage = ref('');
const successMessage = ref('');
const loading = ref(false);

const placementDrive = ref(null);
const applications = ref([]);

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

const props = defineProps({
  mode: {
    type: String,
    default: 'view',
    // supported options: create, edit, view
  },
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
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Error fetching placement drive';
  }
}

async function fetchApplications(placementDriveId) {
  errorMessage.value = '';
  try {
    const userRole = authStore.user.role.toLowerCase();
    const url = `/api/${userRole}/placement-drives/${placementDriveId}/applications`;
    const response = await fetch(url, {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    applications.value = data.data.applications;
  } catch (error) {
    console.error(error);
    errorMessage.value = `Error fetching applications for placement drive ${placementDriveId}`;
  }
}

async function updateApplicationStatus(applicationId, applicationAction) {
  if (!['shortlist', 'select', 'reject'].includes(applicationAction)) {
    alert('Incorrect application status');
    return;
  }
  errorMessage.value = '';
  try {
    const userRole = authStore.user.role.toLowerCase();
    const url = `/api/${userRole}/applications/${applicationId}/${applicationAction}`;
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    const application = applications.value.find((application) => application.id === applicationId);
    if (application) {
      application.status = data.data.application.status;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${applicationAction} the application`;
  }
}
async function viewApplicationDetails(applicationId) {
  errorMessage.value = '';
  try {
    router.push(`/applications/${applicationId}`);
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to view application with id: ${applicationId}`;
  }
}
async function createPlacementDrive(newDrive) {
  errorMessage.value = '';
  loading.value = true;
  try {
    const payload = {
      job_title: newDrive.job_title,
      description: newDrive.job_description,
      eligibility_criteria: newDrive.eligibility_criteria,
      application_deadline: new Date(newDrive.application_deadline).toISOString() ,
    };
    const response = await fetch('/api/company/placement-drives', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    placementDrive.value = data.data.placement_drive;

    successMessage.value = 'Placement drive created successfully';
    router.push(`/placement-drives/${placementDrive.value.id}`);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to create placement drive';
  } finally {
    loading.value = false;
  }
}

async function saveEditedPlacementDrive(drive) {
  errorMessage.value = '';
  loading.value = true;
  try {
    const payload = {
      job_title: drive.job_title,
      description: drive.job_description,
      eligibility_criteria: drive.eligibility_criteria,
      application_deadline: new Date(drive.application_deadline).toISOString(),
    };
    const url = `/api/company/placement-drives/${placementDrive.value.id}`;
    const response = await fetch(url, {
      method: 'PATCH',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    router.push(`/placement-drives/${placementDrive.value.id}`);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to edit placement drive';
  } finally {
    loading.value = false;
  }
}

function navigateToEditPage() {
  router.push(`/placement-drives/${placementDrive.value.id}/edit`);
}

watchEffect(async () => {
  if (!authStore.user) await authStore.loadUser();
  if (props.mode !== 'create') {
    await fetchPlacementDriveDetails(route.params.id);
    if (props.mode !== 'edit') {
      await fetchApplications(route.params.id);
    }
  }
});
</script>
<template>
  <h2 class="text-center mt-3">Placement Drive Details</h2>
  <PlacementDriveDetails
    v-if="mode === 'create'"
    :mode="mode"
    :loading="loading"
    @create="createPlacementDrive"
  />

  <PlacementDriveDetails
    v-else-if="placementDrive"
    :placement-drive="placementDrive"
    :mode="mode"
    :loading="loading"
    :show-applications-count="mode === 'view'"
    :allowed-actions="allowedActions"
    @save="saveEditedPlacementDrive"
    @edit="navigateToEditPage"
  />

  <div v-else-if="errorMessage" class="alert alert-danger">
    {{ errorMessage }}
  </div>

  <div v-else class="text-center mt-5">Loading...</div>

  <h3 class="text-center mt-2" v-if="mode === 'view'">Applications</h3>

  <ApplicationsTable
    v-if="placementDrive && mode === 'view'"
    :applications="applications"
    :actions="['view', 'shortlist', 'select', 'reject']"
    @shortlist="(applicationId) => updateApplicationStatus(applicationId, 'shortlist')"
    @select="(applicationId) => updateApplicationStatus(applicationId, 'select')"
    @reject="(applicationId) => updateApplicationStatus(applicationId, 'reject')"
    @view="(applicationId) => viewApplicationDetails(applicationId)"
  />
</template>
