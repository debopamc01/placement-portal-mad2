<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import PlacementDriveTable from '@/components/PlacementDriveTable.vue';
import { modifyPlacementDriveStatus } from '@/common/apiFunctions';
import StatusBadge from '@/components/StatusBadges.vue';

const router = useRouter();
const authStore = useAuthStore();

const companies = ref([]);
const errorMessage = ref('');
const placementDrives = ref([]);

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function loadCompanies() {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/admin/companies', {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    companies.value = data.data.companies;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load companies';
  }
}
async function modify_company(companyId, action) {
  const actions = ['approve', 'reject', 'blacklist'];
  if (actions.indexOf(action) === -1) {
    console.error(`Action should be one of ${actions}, but is ${action}`);
    return;
  }
  const url = `/api/admin/company/${companyId}/${action}`;

  try {
    const response = await fetch(url, { method: 'POST', credentials: 'include' });
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    const company = companies.value.find((company) => company.id === companyId);

    if (company) {
      company.approval_status = data.data.status;
      loadPlacementDrives();
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} company`;
  }
}
async function loadPlacementDrives() {
  errorMessage.value = '';
  try {
    const response = await fetch('/api/admin/placement-drives', {
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

async function modifyPlacementDrive(placementDriveId, action) {
  try {
    const userRole = authStore.user.role.toLowerCase();
    const newPlacementDrive = await modifyPlacementDriveStatus(userRole, placementDriveId, action);
    const existingPlacementDrive = placementDrives.value.find(
      (pd) => pd.id === newPlacementDrive.id,
    );
    if (existingPlacementDrive) Object.assign(existingPlacementDrive, newPlacementDrive);
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} placement drive`;
  }
}

async function viewPlacementDrive(placementDriveId) {
  router.push(`/placement-drives/${placementDriveId}`);
}

async function viewCompany(companyId) {
  router.push(`/companies/${companyId}`);
}
onMounted(() => {
  authStore.loadUser();
  loadCompanies();
  loadPlacementDrives();
});
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
    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0"><i class="fas fa-briefcase"></i> Companies</h5>
      </div>
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Website</th>
            <th>Approval Status</th>
            <th>Placement Drives</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.id }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.email }}</td>
            <td>
              <a :href="company.website" target="_blank">
                {{ company.website }}
              </a>
            </td>
            <td>
              <StatusBadge :status="company.approval_status" :font-size="'fs-7'" />
            </td>
            <td>{{ company.placement_drive_ids.length }}</td>
            <td>
              <button
                class="btn btn-sm btn-light dropdown-toggle"
                type="button"
                aria-expanded="false"
                data-bs-toggle="dropdown"
              >
                Actions
              </button>
              <ul class="dropdown-menu">
                <li>
                  <button class="dropdown-item" @click="viewCompany(company.id)">
                    View Details
                  </button>
                </li>
                <li v-if="company.approval_status !== 'approved'">
                  <button
                    class="dropdown-item text-success"
                    @click="modify_company(company.id, 'approve')"
                  >
                    Approve
                  </button>
                </li>
                <li v-if="company.approval_status !== 'rejected'">
                  <button
                    class="dropdown-item text-warning"
                    @click="modify_company(company.id, 'reject')"
                  >
                    Reject
                  </button>
                </li>
                <li v-if="company.approval_status !== 'blacklisted'">
                  <button
                    class="dropdown-item text-danger"
                    @click="modify_company(company.id, 'blacklist')"
                  >
                    Blacklist
                  </button>
                </li>
              </ul>
            </td>
          </tr>
          <tr v-if="companies.length === 0">
            <td colspan="7" class="text-center text-muted">No companies found</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mt-5">
      <div class="card shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">Placement Drives</h5>
        </div>
        <PlacementDriveTable
          :placement-drives="placementDrives"
          :actions="['approve', 'decline', 'reopen', 'close', 'delete', 'view']"
          :show-company="true"
          @approve="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'approve')"
          @decline="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'decline')"
          @close="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'close')"
          @reopen="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'reopen')"
          @view="viewPlacementDrive"
        />
      </div>
    </div>
  </div>
</template>
