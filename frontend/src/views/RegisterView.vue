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

const successMessage = ref('');
const errorMessage = ref('');

async function register() {
  successMessage.value = '';
  errorMessage.value = '';

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
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow-lg">
          <div class="card-body p-5">
            <h2>Register</h2>

            <div class="mb-3">
              <label class="form-label">Role</label>

              <select v-model="role" class="form-select">
                <option value="student">Student</option>

                <option value="company">Company</option>
              </select>
            </div>

            <div class="mb-3">
              <input
                v-model="name"
                class="form-control"
                :placeholder="role === 'student' ? 'Student Name' : 'Company Name'"
              />
            </div>

            <div class="mb-3">
              <input v-model="email" class="form-control" placeholder="Email" />
            </div>

            <div class="mb-3">
              <input
                v-model="password"
                type="password"
                class="form-control"
                placeholder="Password"
              />
            </div>

            <div v-if="role === 'student'" class="mb-3">
              <textarea v-model="description" class="form-control" placeholder="Description" />
            </div>

            <template v-else>
              <div class="mb-3">
                <input v-model="hrContact" class="form-control" placeholder="HR Contact" />
              </div>

              <div class="mb-3">
                <input v-model="website" class="form-control" placeholder="Website" />
              </div>
            </template>

            <div v-if="successMessage" class="alert alert-success">
              {{ successMessage }}
            </div>

            <div v-if="errorMessage" class="alert alert-danger">
              {{ errorMessage }}
            </div>

            <button class="btn btn-primary" @click="register">Register</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
