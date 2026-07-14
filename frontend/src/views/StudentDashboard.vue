<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import PlacementDriveTable from '@/components/PlacementDriveTable.vue';
import CompaniesTable from '@/components/CompaniesTable.vue';

const router = useRouter();
const authStore = useAuthStore();

const errorMessage = ref('');
const successMessage = ref('');

const allPlacementDrives = ref([]);

const companies = ref([]);

const appliedPlacementDrives = computed(() =>
  allPlacementDrives.value.filter((pd) => pd.has_applied),
);

const unappliedPlacementDrives = computed(() =>
  allPlacementDrives.value.filter((pd) => !pd.has_applied),
);

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function loadPlacementDrives() {
  errorMessage.value = '';
  allPlacementDrives.value = [];
  try {
    const response = await fetch('/api/student/placement-drives', {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    allPlacementDrives.value = data.data.placement_drives;
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

    loadPlacementDrives();
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
    alert('Export in progress. Exported file will be emailed once available.');
  } catch (error) {
    errorMessage.value = error;
    console.log(error);
  }
}

async function fetchCompanies() {
  errorMessage.value = '';

  try {
    const url = '/api/student/companies';
    const response = await fetch(url, {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    companies.value = data.data.companies;
  } catch (error) {
    errorMessage.value = error;
    console.log(error);
  }
}

async function viewCompany(companyId) {
  router.push(`/companies/${companyId}`);
}
onMounted(() => {
  authStore.loadUser();
  fetchCompanies();
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
    <div>
      <CompaniesTable :companies="companies" :actions="['view']" @view="viewCompany" />
    </div>
    <div class="card mt-4">
      <div class="card-header d-flex justify-content-between">
        <h4>Available Placement Drives</h4>
      </div>
      <PlacementDriveTable
        :placement-drives="unappliedPlacementDrives"
        :show-application-status="true"
        :show-placement-drive-status="false"
        :show-company="true"
        :actions="['view', 'apply']"
        @apply="applyToPlacementDrive"
        @view="viewPlacementDrive"
      />
    </div>
    <div class="card mt-4">
      <div class="card-header d-flex justify-content-between">
        <h4>Application History</h4>
        <button class="btn btn-primary" @click="exportApplications">Export to CSV</button>
      </div>
      <PlacementDriveTable
        :placement-drives="appliedPlacementDrives"
        :show-application-status="true"
        :show-placement-drive-status="false"
        :show-company="true"
        :actions="['view', 'apply']"
        @view="viewPlacementDrive"
      />
    </div>
  </div>
</template>
