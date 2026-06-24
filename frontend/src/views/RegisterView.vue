<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const role = ref('student');

const name = ref('');
const email = ref('');
const password = ref('');

const description = ref('');

const hrContact = ref('');
const website = ref('');

const loading = ref(false);

const successMessage = ref('');
const errorMessage = ref('');

async function register() {
  successMessage.value = '';
  errorMessage.value = '';
  loading.value = true;

  try {
    let url = '';
    let payload = {};

    if (role.value === 'student') {
      url = 'http://127.0.0.1:5000/api/auth/register/student';

      payload = {
        name: name.value,
        email: email.value,
        password: password.value,
        description: description.value,
      };
    } else {
      url = 'http://127.0.0.1:5000/api/auth/register/company';

      payload = {
        name: name.value,
        email: email.value,
        password: password.value,
        hr_contact: hrContact.value,
        website: website.value,
      };
    }

    const response = await fetch(url, {
      method: 'POST',
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

    if (role.value === 'student') {
      successMessage.value = 'Student registered successfully';
    } else {
      successMessage.value = 'Company registered successfully and awaiting approval';
    }

    setTimeout(() => {
      router.push('/login');
    }, 1500);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to contact server';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="register">
    <div class="container mt-5">
      <h1 class="card-title text-center mb-3">Register</h1>
      <div class="row justify-content-center">
        <div class="col-12 col-sm-10 col-md-6 col-lg-4">
          <div class="card shadow-lg">
            <div class="card-body p-5">
              <div class="mb-3">
                <label class="form-label">Role</label>

                <select v-model="role" class="form-select">
                  <option value="student">Student</option>

                  <option value="company">Company</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Name</label>
                <input
                  v-model="name"
                  class="form-control"
                  :placeholder="role === 'student' ? 'Student Name' : 'Company Name'"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input
                  v-model="email"
                  class="form-control"
                  placeholder="user@example.com"
                  type="email"
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

              <div v-if="role === 'student'" class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="description" class="form-control" placeholder="Description" />
              </div>

              <template v-else>
                <div class="mb-3">
                  <label class="form-label">HR Contact</label>
                  <input
                    v-model="hrContact"
                    class="form-control"
                    placeholder="+910000000000"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label">Website</label>
                  <input
                    v-model="website"
                    class="form-control"
                    placeholder="www.example.com"
                    required
                  />
                </div>
              </template>

              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>

              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>

              <button class="btn btn-primary" type="submit" :disabled="loading">
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
              <div class="mt-3">
                Already have an account?
                <router-link to="/login" class="fw-bold">Login</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>
