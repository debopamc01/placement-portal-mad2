<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

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
async function createPlacementDrive() {
  loading.value = true;
  try {
    const payload = {
      job_title: jobTitle.value,
      description: jobDescription.value,
      eligibility_criteria: eligibilityCriteria.value,
      application_deadline: applicationDeadline.value,
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
    const newDrive = data.data.placement_drive;

    placementDrives.value.push(newDrive);
    successMessage.value = 'Placement drive created successfully';

    const closeButton = document.querySelector(
      '#createPlacementDriveModal [data-bs-dismiss="modal"]',
    );

    setTimeout(() => {
      closeButton.click();
    }, 1000);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to create placement drive';
  } finally {
    loading.value = false;
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
onMounted(() => {
  loadPlacementDrives();

  const modalElement = document.getElementById('createPlacementDriveModal');

  modalElement.addEventListener('hidden.bs.modal', () => {
    resetForm();
  });
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

    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0"><i class="fas fa-briefcase"></i> Placement Drives</h5>
        <button
          class="btn btn-outline-primary"
          data-bs-toggle="modal"
          data-bs-target="#createPlacementDriveModal"
        >
          <i class="fas fa-plus"></i> Create New Drive
        </button>
      </div>
      <table class="table table-striped table-hover">
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
            <td style="text-transform: uppercase">
              <span
                class="badge"
                :class="{
                  'bg-danger': placementDrive.status === 'declined',
                  'bg-secondary': placementDrive.status === 'pending',
                  'bg-success': placementDrive.status === 'active',
                  'bg-success': placementDrive.status === 'closed',
                }"
              >
                {{ placementDrive.status }}
              </span>
            </td>
            <td>{{ placementDrive.application_ids.length }}</td>
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
                  <button class="dropdown-item">View Details</button>
                </li>
                <li v-if="placementDrive.status !== 'closed'">
                  <button class="dropdown-item text-success" @click="closePlacementDrive()">
                    Close
                  </button>
                </li>
                <li v-if="placementDrive.status === 'closed'">
                  <button class="dropdown-item text-success" @click="reopenPlacementDrive()">
                    Reopen
                  </button>
                </li>
                <li>
                  <button class="dropdown-item text-primary" @click="editPlacementDrive()">
                    Edit
                  </button>
                </li>
                <li>
                  <button class="dropdown-item text-danger" @click="deletePlacementDrive()">
                    Delete
                  </button>
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
      <div
        class="modal fade"
        id="createPlacementDriveModal"
        tabindex="-1"
        aria-labelledby="createPlacementDriveModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <form @submit.prevent="createPlacementDrive">
              <div class="modal-header">
                <h5 class="modal-title" id="createPlacementDriveModalLabel">
                  Create Placement Drive
                </h5>

                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>

              <div class="modal-body">
                <div v-if="successMessage" class="alert alert-success">
                  {{ successMessage }}
                </div>

                <div v-if="errorMessage" class="alert alert-danger">
                  {{ errorMessage }}
                </div>
                <!-- Job Title -->

                <div class="mb-3">
                  <label class="form-label"> Job Title </label>

                  <input v-model="jobTitle" class="form-control" required />
                </div>

                <!-- Description -->

                <div class="mb-3">
                  <label class="form-label"> Job Description </label>

                  <textarea
                    v-model="jobDescription"
                    rows="4"
                    class="form-control"
                    required
                  ></textarea>
                </div>

                <!-- Eligibility -->

                <div class="mb-3">
                  <label class="form-label"> Eligibility Criteria </label>

                  <textarea
                    v-model="eligibilityCriteria"
                    rows="3"
                    class="form-control"
                    required
                  ></textarea>
                </div>

                <!-- Deadline -->

                <div class="mb-3">
                  <label class="form-label"> Application Deadline </label>

                  <input
                    v-model="applicationDeadline"
                    type="datetime-local"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <div class="modal-footer">
                <div>
                  <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                    :disabled="loading"
                  >
                    Cancel
                  </button>

                  <button class="btn btn-primary" type="submit" :disabled="loading">
                    {{ loading ? 'Creating...' : 'Create' }}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
