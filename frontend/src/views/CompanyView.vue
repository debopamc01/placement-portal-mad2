<script setup>
import { computed, ref, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/auth';

import CompanyDetails from '@/components/CompanyDetails.vue';
import PlacementDriveTable from '@/components/PlacementDriveTable.vue';
import NavBar from '@/components/NavBar.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const props = defineProps({
  mode: {
    type: String,
    default: 'view',
    // Options: view | edit
  },

  editProfilePermission: {
    type: Boolean,
    default: false,
  },

  navBarTitle: {
    type: String,
    default: 'Company View',
  },
});

const mode = ref(props.mode);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const company = ref(null);
const placementDrives = ref([]);

const userRole = computed(() => authStore.user?.role?.toLowerCase());

async function fetchCompany() {
  errorMessage.value = '';

  try {
    let url = '';

    if (userRole.value === 'company') {
      url = '/api/company/profile';
    } else {
      url = `/api/${userRole.value}/companies/${route.params.id}`;
    }

    const response = await fetch(url, {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    company.value = data.data.company;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to fetch company';
  }
}

async function fetchPlacementDrives() {
  errorMessage.value = '';

  try {
    let url = '';

    if (userRole.value === 'company') {
      url = '/api/company/placement-drives';
    } else {
      url = `/api/${userRole.value}/companies/${route.params.id}/placement-drives`;
    }

    const response = await fetch(url, {
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
    errorMessage.value = 'Unable to fetch placement drives';
  }
}

async function saveCompany(updatedCompany) {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/company/profile', {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedCompany),
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    company.value = data.data.company;
    successMessage.value = 'Company profile updated successfully';
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to update company profile';
  }
}

function goBack() {
  router.back();
}

async function editCompany() {
  mode.value = 'edit';
}

function viewPlacementDrive(id) {
  router.push(`/placement-drives/${id}`);
}

const allowedActions = computed(() => {
  switch (userRole.value) {
    case 'admin':
      return ['approve', 'reject', 'blacklist'];
    default:
      return [];
  }
});

async function modifyCompanyApprovalStatus(action) {
  const actions = ['approve', 'reject', 'blacklist'];
  if (!actions.includes(action)) {
    console.error(`Action should be one of ${actions}, but is ${action}`);
    return;
  }
  const url = `/api/admin/company/${company.value.id}/${action}`;

  try {
    const response = await fetch(url, { method: 'POST', credentials: 'include' });
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    company.value.approval_status = data.data.status;

    if (company) {
      fetchPlacementDrives();
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} company`;
  }
}

watchEffect(async () => {
  loading.value = true;

  await authStore.loadUser();

  await fetchCompany();
  await fetchPlacementDrives();

  loading.value = false;
});
</script>

<template>
  <div class="container mt-4">
  <NavBar :title="navBarTitle" />

  <div v-if="successMessage" class="alert alert-success">
    {{ successMessage }}
  </div>

  <div v-if="errorMessage" class="alert alert-danger">
    {{ errorMessage }}
  </div>

  <template class="card shadow-sm mb-4" v-if="company">
    <CompanyDetails
      :company="company"
      :mode="mode"
      :allowedActions="allowedActions"
      @approve="modifyCompanyApprovalStatus('approve')"
      @reject="modifyCompanyApprovalStatus('reject')"
      @blacklist="modifyCompanyApprovalStatus('blacklist')"
      @save="saveCompany"
      @back="goBack"
      @edit="editCompany"
    />
  </template>

  <div v-else-if="loading" class="text-center mt-5">Loading...</div>

  <div v-if="company && userRole !== 'company'">
    <div class="card shadow-sm mt-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">Placement Drives</h5>
      </div>
      <PlacementDriveTable
        :placement-drives="placementDrives"
        :actions="['view']"
        @view="viewPlacementDrive"
      />
    </div>
  </div>
  </div>
</template>
