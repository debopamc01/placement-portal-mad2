<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false);

async function login() {
  errorMessage.value = '';
  loading.value = true;

  try {
    await authStore.login(email.value, password.value);

    const role = authStore.user.role;

    // TODO:If authenticated user tries to login, show dashboard

    if (role === 'admin') {
      router.push('/admin');
    } else if (role === 'company') {
      router.push('/company');
    } else {
      router.push('/student');
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="login">
    <div class="container mt-5">
      <h1 class="card-title text-center mb-3">Login to Placement Portal</h1>
      <div class="row justify-content-center">
        <div class="col-12 col-sm-10 col-md-6 col-lg-4">
          <div class="card shadow-lg">
            <div class="card-body p-5">
              <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input
                  v-model="email"
                  type="email"
                  class="form-control"
                  placeholder="Email"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  placeholder="Password"
                  required
                />
              </div>

              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>

              <button class="btn btn-primary mt-3" type="submit" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>

              <div class="mt-3">
                Don't have an account?<router-link to="/register" class="fw-bold">
                  Register</router-link
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>
