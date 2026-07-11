<script setup>
import { computed, ref, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/auth';
import StudentDetails from '@/components/StudentDetails.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const props = defineProps({
  mode: {
    type: String,
    default: 'view',
  },
});

const errorMessage = ref('');
const successMessage = ref('');
const loading = ref(false);

const student = ref(null);

const userRole = computed(() => authStore.user?.role?.toLowerCase() ?? '');

const resumePermissions = computed(() => {
  if (userRole.value === 'student') {
    return ['upload', 'download'];
  }

  return ['download'];
});

async function fetchStudent() {
  errorMessage.value = '';

  try {
    let url;

    if (userRole.value === 'student') {
      url = '/api/student/profile';
    } else if (userRole.value === 'admin') {
      url = `/api/${userRole.value}/students/${route.params.id}`;
    } else {
      errorMessage.value = 'You do not have access to this page';
      return;
    }

    const response = await fetch(url, {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    student.value = data.data.student;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load student profile';
  }
}

async function saveStudent(updatedStudent) {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/student/profile', {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedStudent),
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    student.value = data.data.student;
    successMessage.value = 'Profile updated successfully.';
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to update profile.';
  }
}

async function uploadResume(file) {
  errorMessage.value = '';

  try {
    const formData = new FormData();
    formData.append('resume', file);

    const response = await fetch('/api/student/resume', {
      method: 'POST',
      credentials: 'include',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    student.value.resume_filename = data.data.resume_filename;

    successMessage.value = 'Resume uploaded successfully.';
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to upload resume.';
  }
}

async function downloadResume() {
  errorMessage.value = '';

  try {
    let url;

    if (userRole.value === 'student') {
      url = '/api/student/resume';
    } else {
      url = `/api/${userRole.value}/students/${student.value.id}/resume`;
    }

    const response = await fetch(url, {
      credentials: 'include',
    });

    if (!response.ok) {
      errorMessage.value = 'Unable to download resume.';
      return;
    }

    const blob = await response.blob();

    const objectUrl = URL.createObjectURL(blob);

    window.open(objectUrl, '_blank');

    setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to download resume.';
  }
}

function goBack() {
  router.back();
}

watchEffect(async () => {
  loading.value = true;

  await authStore.loadUser();
  await fetchStudent();

  loading.value = false;
});
</script>

<template>
  <h2 class="text-center mt-3">Student Profile</h2>

  <div v-if="successMessage" class="alert alert-success">
    {{ successMessage }}
  </div>

  <div v-if="errorMessage" class="alert alert-danger">
    {{ errorMessage }}
  </div>

  <StudentDetails
    v-if="student"
    :student="student"
    :mode="mode"
    :resume-permissions="resumePermissions"
    @save="saveStudent"
    @back="goBack"
    @uploadResume="uploadResume"
    @downloadResume="downloadResume"
  />

  <div v-else-if="loading" class="text-center mt-5">Loading...</div>
</template>
