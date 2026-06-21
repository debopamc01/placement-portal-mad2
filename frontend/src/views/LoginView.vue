<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const errorMessage = ref('');

async function login() {
  errorMessage.value = '';

  try {
    await authStore.login(email.value, password.value);

    const role = authStore.user.role;

    if (role === 'admin') {
      router.push('/admin');
    } else if (role === 'company') {
      router.push('/company');
    } else {
      router.push('/student');
    }
  } catch (error) {
    errorMessage.value = error.message;
  }
}
</script>

<template>
  <form @submit.prevent="login">
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-5 col-lg-5">
          <div class="card shadow-lg">
            <div class="card-body p-5">
              <h1 class="card-title text-center mb-3">Login to Placement Portal</h1>

              <div class="mb-3">
                <input v-model="email" class="form-control" placeholder="Email" required />
              </div>

              <div class="mb-3">
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

              <button class="btn btn-primary mt-3" @click="login">Login</button>

              <div class="mt-3">
                Don't have an account?<router-link to="/register"> Sign up </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>
