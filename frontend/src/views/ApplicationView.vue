<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRoute } from 'vue-router';
import StatusBadge from '@/components/StatusBadges.vue';
import StudentDetails from '@/components/StudentDetails.vue';

const application = ref(null);
const errorMessage = ref('');

const route = useRoute();
const authStore = useAuthStore();

async function fetchApplication(applicationId) {
  errorMessage.value = '';
  try {
    const userRole = authStore.user.role.toLowerCase();
    const url = `/api/${userRole}/applications/${applicationId}`;
    const response = await fetch(url, {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    application.value = data.data.application;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Error fetching application';
  }
}

onMounted(async () => {
  await authStore.loadUser();
  await fetchApplication(route.params.id);
});
</script>
<template>
  <div v-if="errorMessage" class="alert alert-danger">
    {{ errorMessage }}
  </div>

  <div v-else-if="!application" class="text-center mt-5">Loading...</div>

  <template v-else>
    <div class="container py-4">
      <div class="card shadow-sm mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h3 class="mb-0">Application Details</h3>

          <StatusBadge :status="application.status" />
        </div>

        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <label class="form-label fw-semibold"> Placement Drive </label>

              <div class="form-control-plaintext">
                {{ application.placement_drive.job_title }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold"> Applied On </label>

              <div class="form-control-plaintext">
                {{ new Date(application.application_date).toLocaleString() }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <StudentDetails :student="application.student" mode="view" />
    </div>
  </template>
</template>
